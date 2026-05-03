# 📖 项目讲解指南

详细的源代码讲解和实现说明。

---

## 快速导航

- [核心模块](#核心模块)
- [主控制循环](#主控制循环)
- [工具函数](#工具函数)
- [LLM 集成](#llm-集成)
- [常见任务](#常见任务)

---

## 核心模块

### env_wrapper.py - 环境和机械臂控制

**目的：** 提供低层的机械臂控制接口

**关键类：`RobotArmController`**

```python
class RobotArmController:
    def __init__(self, render_mode="rgb_array"):
        """初始化仿真环境"""
        self.env = PandaReachEnv(render_mode=render_mode)
        self.render_mode = render_mode
    
    def get_state(self) -> dict:
        """获取当前环境状态
        
        Returns:
            {
                'ee_pos': [x, y, z],           # 末端执行器位置
                'ee_orn': [qx, qy, qz, qw],   # 末端执行器方向（四元数）
                'object_pos': [x, y, z],      # 物体位置
                'target_pos': [x, y, z],      # 目标位置
                'achieved_goal': [...],        # 实际目标
                'is_success': bool,            # 是否成功
            }
        """
        obs, _ = self.env.reset()
        return {
            'ee_pos': obs['observation'][:3],
            'object_pos': obs['observation'][3:6],
            'target_pos': obs['desired_goal'],
        }
    
    def move_arm(self, target_pos: List[float], speed=1.0) -> bool:
        """使用逆运动学移动机械臂
        
        Args:
            target_pos: 目标位置 [x, y, z]
            speed: 移动速度倍数
        
        Returns:
            是否成功到达目标
        
        实现过程：
        1. 使用 IK 求解器计算关节角度
        2. 规划路径
        3. 发送控制命令到 PyBullet
        4. 通过多步模拟最终到达目标
        """
        # 调用 panda_gym 的 IK 求解器
        joint_angles = self.env.compute_ik(target_pos)
        
        # 发送到控制器
        self.env.set_joint_angles(joint_angles)
        
        # 执行多步仿真直到到达
        for _ in range(100):  # 最多 100 步
            self.env.step(action)
            
            if self.is_at_target(target_pos):
                return True
        
        return False
    
    def grasp(self) -> bool:
        """关闭夹手，抓取物体"""
        # 设置夹手宽度为 0
        self.env.set_gripper_width(0.0)
        return True
    
    def release(self) -> bool:
        """打开夹手，释放物体"""
        # 设置夹手宽度为最大
        self.env.set_gripper_width(0.04)
        return True
```

**关键属性：**

- `self.env` - panda_gym 环境实例
- `self.render_mode` - 渲染模式（"rgb_array" 或 "human"）

---

### skills.py - 工具函数接口

**目的：** 向 LLM 提供高层工具函数

**导出的工具：**

#### 1. `perceive_environment() -> str`

```python
def perceive_environment() -> str:
    """观察场景并返回自然语言描述
    
    Returns:
        例如："
        机械臂末端执行器位置: x=0.2, y=0.0, z=0.5
        绿色物体位置: x=-0.5, y=0.2, z=0.0
        目标放置位置: x=-0.2, y=0.3, z=0.1
        夹手状态: 打开
        "
    
    这个信息被 LLM 用来决定下一步行动。
    """
    controller = _ensure_initialized()
    state = controller.get_state()
    
    description = f"""
    End-effector: x={state['ee_pos'][0]:.2f}, y={state['ee_pos'][1]:.2f}, z={state['ee_pos'][2]:.2f}
    Object: x={state['object_pos'][0]:.2f}, y={state['object_pos'][1]:.2f}, z={state['object_pos'][2]:.2f}
    Target: x={state['target_pos'][0]:.2f}, y={state['target_pos'][1]:.2f}, z={state['target_pos'][2]:.2f}
    Gripper: {"Open" if state['gripper_open'] else "Closed"}
    """
    
    return description
```

#### 2. `move_arm_to(x: float, y: float, z: float) -> str`

```python
def move_arm_to(x: float, y: float, z: float) -> str:
    """移动末端执行器到指定位置
    
    Args:
        x, y, z: 目标位置（米）
    
    Returns:
        执行结果描述
    
    验证逻辑：
    1. 检查坐标是否在工作空间内
    2. 调用低层运动控制
    3. 返回成功或失败
    """
    controller = _ensure_initialized()
    
    # 工作空间检查
    if not (-1.0 <= x <= 0.2 and -0.6 <= y <= 0.6 and 0.0 <= z <= 1.2):
        return f"❌ Target position ({x}, {y}, {z}) is out of workspace bounds"
    
    # 执行移动
    success = controller.move_arm([x, y, z])
    
    if success:
        current_state = perceive_environment()
        return f"✓ Moved to ({x:.2f}, {y:.2f}, {z:.2f})\n{current_state}"
    else:
        return f"❌ Failed to move to ({x:.2f}, {y:.2f}, {z:.2f})"
```

#### 3. `grasp() -> str` 和 `release() -> str`

```python
def grasp() -> str:
    """关闭夹手抓取前方物体"""
    controller = _ensure_initialized()
    controller.grasp()
    return "✓ Gripper closed"

def release() -> str:
    """打开夹手释放物体"""
    controller = _ensure_initialized()
    controller.release()
    return "✓ Gripper opened"
```

---

### main.py - 决策循环

**目的：** 实现 LLM 闭环控制

**主要类和函数：**

#### 1. `_current_state() -> Dict`

```python
def _current_state() -> Dict[str, Union[List[float], float, bool]]:
    """获取当前环境状态（不通过自然语言）
    
    Returns:
        {
            'ee_pos': [x, y, z],
            'object_pos': [x, y, z],
            'target_pos': [x, y, z],
            'success': bool,
            'step': int,
        }
    """
    controller = _ensure_initialized()
    state = controller.get_state()
    
    # 检查是否成功
    success = np.linalg.norm(
        np.array(state['object_pos']) - np.array(state['target_pos'])
    ) < 0.05  # 5cm 以内视为成功
    
    return {
        'ee_pos': state['ee_pos'],
        'object_pos': state['object_pos'],
        'target_pos': state['target_pos'],
        'success': success,
    }
```

#### 2. `_build_tools() -> List[Dict]`

```python
def _build_tools() -> List[Dict[str, Union[str, Dict]]]:
    """构建 LLM 可调用的工具定义（OpenAI function_calling 格式）
    
    Returns:
        用于 LLM API 的工具定义列表
        
    格式示例：
    [
        {
            "type": "function",
            "function": {
                "name": "move_arm_to",
                "description": "Move robot end-effector to target position",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "x": {"type": "number", "description": "X position in meters"},
                        "y": {"type": "number", "description": "Y position in meters"},
                        "z": {"type": "number", "description": "Z position in meters"},
                    },
                    "required": ["x", "y", "z"],
                }
            }
        },
        ...
    ]
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "perceive_environment",
                "description": "Observe the scene and get current positions",
                "parameters": {"type": "object", "properties": {}, "required": []}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "move_arm_to",
                "description": "Move end-effector to target position (x, y, z)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "x": {"type": "number", "description": "X in meters"},
                        "y": {"type": "number", "description": "Y in meters"},
                        "z": {"type": "number", "description": "Z in meters"},
                    },
                    "required": ["x", "y", "z"],
                }
            }
        },
        # grasp 和 release 定义...
    ]
```

#### 3. `_TOOL_MAP` - 工具映射

```python
_TOOL_MAP: Dict[str, Callable] = {
    "perceive_environment": perceive_environment,
    "move_arm_to": move_arm_to,
    "grasp": grasp,
    "release": release,
}
```

这个映射用来执行 LLM 调用的工具。

#### 4. `run_llm_mode(max_steps, provider, render)`

```python
def run_llm_mode(max_steps: int, provider: str, render: bool):
    """运行 LLM 驱动的控制循环
    
    Args:
        max_steps: 最大推理步数
        provider: "openrouter" 或 "openai"
        render: 是否显示渲染
    
    流程：
    1. 初始化 LLM 客户端
    2. 构建系统提示词
    3. 主循环（每步执行一次）
    4. 清理资源
    """
    
    # 步骤 1：初始化客户端
    api_key = os.environ.get(
        "OPENROUTER_API_KEY" if provider == "openrouter" else "OPENAI_API_KEY"
    )
    
    if provider == "openrouter":
        client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    else:
        client = OpenAI(api_key=api_key)
    
    # 步骤 2：系统提示词
    system_prompt = """
    You are a robotic manipulation planner for a Franka Panda arm.
    Goal: Pick up a green cube and place it at the target location.
    
    RULES:
    - Make EXACTLY ONE tool call per response
    - Follow this sequence:
      1. perceive_environment() first
      2. release() to open gripper
      3. move_arm_to() above cube
      4. move_arm_to() to grasp
      5. grasp() to hold
      6. move_arm_to() lift
      7. move_arm_to() over target
      8. move_arm_to() to place
      9. release() to drop
      10. perceive_environment() to verify
    """
    
    # 步骤 3：消息历史（用于 multi-turn 对话）
    messages = [{"role": "system", "content": system_prompt}]
    
    # 步骤 4：主循环
    for step in range(max_steps):
        # 调用 LLM
        response = client.chat.completions.create(
            model=os.environ.get("LLM_MODEL", "default"),
            messages=messages,
            tools=_build_tools(),
            tool_choice="auto",
            temperature=0.0,
        )
        
        message = response.choices[0].message
        messages.append(message.model_dump())
        
        # 检查是否有工具调用
        if not message.tool_calls:
            print(f"[Step {step}] LLM: {message.content}")
            if "done" in (message.content or "").lower():
                break
            continue
        
        # 执行工具调用
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            raw_args = tool_call.function.arguments or "{}"
            args = json.loads(raw_args)
            
            print(f"[Step {step}] Calling {func_name}({args})")
            
            # 执行对应的工具
            tool_func = _TOOL_MAP[func_name]
            result = tool_func(**args)
            
            # 添加工具结果到消息历史
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": func_name,
                "content": result,
            })
        
        # 检查是否成功
        if _current_state().get("success", False):
            print("✓ Task success!")
            break
    
    # 步骤 5：清理
    close_skills()
```

---

## 主控制循环

### 接收 LLM 响应的格式

```python
response = {
    "id": "chatcmpl-...",
    "object": "chat.completion",
    "created": 1234567890,
    "model": "gpt-4",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": None,  # 有工具调用时为 None
                "tool_calls": [
                    {
                        "id": "call_...",
                        "type": "function",
                        "function": {
                            "name": "move_arm_to",
                            "arguments": '{"x": -0.5, "y": 0.2, "z": 0.12}'
                        }
                    }
                ]
            }
        }
    ]
}
```

### 工具调用执行流程

```
LLM Response
    ↓
Parse tool_calls
    ↓
For each tool_call:
    - 提取 name 和 arguments
    - 查找 _TOOL_MAP[name]
    - 解析 JSON arguments
    - 执行函数
    - 获取返回值
    - 构建 tool message
    - 添加到 messages
    ↓
发回 LLM（包含工具结果）
    ↓
LLM 根据结果继续推理
```

---

## 常见任务

### 添加新的工具函数

1. **在 skills.py 中定义：**

```python
def new_tool(param1: float, param2: str) -> str:
    """工具描述"""
    controller = _ensure_initialized()
    # 实现逻辑
    return "结果"
```

2. **在 main.py 中注册：**

```python
# 在 _build_tools() 中添加定义
{
    "type": "function",
    "function": {
        "name": "new_tool",
        "description": "描述",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {"type": "number"},
                "param2": {"type": "string"},
            },
            "required": ["param1", "param2"],
        }
    }
}

# 在 _TOOL_MAP 中添加映射
"new_tool": new_tool
```

### 修改控制策略

**方向 1：修改 system_prompt**

编辑 main.py 中的 `system_prompt`，改变 LLM 的指令。

**方向 2：修改演示模式**

编辑 `demo_policy()` 函数中的状态机。

### 使用不同的环境

panda_gym 支持多个环境。修改 env_wrapper.py：

```python
# 从
self.env = PandaReachEnv(render_mode=render_mode)

# 改为
self.env = PandaPushEnv(render_mode=render_mode)  # 推物体任务
# 或
self.env = PandaSlideEnv(render_mode=render_mode)  # 滑动任务
```

---

## 调试技巧

### 检查当前状态

```python
from main import _current_state
state = _current_state()
print(state)
```

### 单步执行

```python
from skills import perceive_environment, move_arm_to, grasp, release

# 手动执行步骤
print(perceive_environment())
print(move_arm_to(-0.5, 0.2, 0.1))
print(grasp())
```

### 查看 LLM 消息

在 `run_llm_mode` 中添加：

```python
print("Messages:", json.dumps(messages, indent=2))
```

---

## 性能优化

### 减少 LLM API 调用

- 增加 `system_prompt` 的详细度
- 减少 max-steps
- 使用更快的模型

### 加快运动学计算

- 使用更好的 IK 求解器
- 减少仿真步数
- 预计算常用位置

---

## 下一步

- 📚 [架构设计](ARCHITECTURE.md) - 系统整体设计
- 🐛 [故障排查](TROUBLESHOOTING.md) - 问题诊断
- ⚡ [快速参考](QUICK_REFERENCE.md) - 命令速查
