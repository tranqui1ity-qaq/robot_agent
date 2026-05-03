# 🔧 系统架构设计

系统整体架构、模块设计和数据流说明。

---

## 系统整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    LLM 控制系统                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐         ┌──────────────┐              │
│  │   OpenAI /   │◄───────►│  LLM API     │              │
│  │ OpenRouter   │         │  (GPT/远程)  │              │
│  └──────────────┘         └──────────────┘              │
│         △                                                │
│         │ API Calls                                      │
│         │                                                │
│  ┌──────┴──────────────────────────────────────┐         │
│  │         main.py（决策循环）                  │         │
│  │  ┌─────────────────────────────────────┐   │         │
│  │  │  Perception → Decision → Execution  │   │         │
│  │  │  感知    → 推理    → 执行          │   │         │
│  │  └─────────────────────────────────────┘   │         │
│  ├──────────────────────────────────────────┤         │
│  │      skills.py（工具函数）                 │         │
│  │  ┌───────────────────────────────────┐  │         │
│  │  │ perceive_environment()            │  │         │
│  │  │ move_arm_to(x, y, z)             │  │         │
│  │  │ grasp()                          │  │         │
│  │  │ release()                        │  │         │
│  │  └───────────────────────────────────┘  │         │
│  └──────────────────────────────────────┤         │
│         │                                             │
│         │ 高层指令                                    │
│         │                                             │
│  ┌──────▼──────────────────────────────┐    │         │
│  │  env_wrapper.py（低层控制）           │   │         │
│  │  ┌────────────────────────────────┐ │   │         │
│  │  │ RobotArmController             │ │   │         │
│  │  │  • 逆运动学 (IK)               │ │   │         │
│  │  │  • 关节控制                     │ │   │         │
│  │  │  • 碰撞检测                     │ │   │         │
│  │  └────────────────────────────────┘ │   │         │
│  └──────────────────────────────────────┘   │         │
│         │                                             │
│         │ 低层控制信号                              │
│         │                                             │
│  ┌──────▼──────────────────────────────┐    │         │
│  │  panda_gym（仿真环境）               │   │         │
│  │  ├─ PyBullet                        │   │         │
│  │  ├─ Franka Panda 机械臂             │   │         │
│  │  ├─ 工作空间和碰撞检测              │   │         │
│  │  └─ 物体和目标位置                  │   │         │
│  └──────────────────────────────────────┘   │         │
│                                              │         │
└──────────────────────────────────────────────┘         │
                                                          │
         ┌──────────────────────────────┐                │
         │   record_video.py（录制）     │                │
         │   ├─ 捕获仿真画面            │                │
         │   ├─ 编码为 MP4              │                │
         │   └─ 保存到 videos/          │                │
         └──────────────────────────────┘                │
```

---

## 数据流

### 单步执行流程

```
1. 感知阶段 (Perception)
   ├─ env.render() → RGB 图像
   ├─ 机械臂位置
   ├─ 物体位置
   ├─ 目标位置
   └─ 构建 scene_state dict

2. LLM 决策阶段 (Decision)
   ├─ 输入：scene_state + system_prompt + 历史消息
   ├─ LLM 推理
   ├─ 解析 tool_call (function_calling)
   └─ 输出：工具名 + 参数

3. 执行阶段 (Execution)
   ├─ skills.{move_arm_to/grasp/release}()
   ├─ env_wrapper.RobotArmController
   ├─ PyBullet 仿真
   └─ 返回执行结果

4. 反馈阶段 (Feedback)
   ├─ 工具执行结果
   ├─ 新的 scene_state
   └─ 添加到消息历史

5. 循环或终止
   ├─ success? → 终止
   ├─ max_steps? → 终止
   └─ 否则 → 回到步骤 1
```

---

## 模块详解

### 1. env_wrapper.py

**职责：** 低层机械臂控制和仿真环境管理

**核心类：** `RobotArmController`

```python
class RobotArmController:
    def __init__(render_mode="rgb_array"):
        self.env = PandaReachEnv()
        self.render_mode = render_mode
    
    def get_state() -> Dict:
        # 获取当前状态（位置、速度等）
        
    def move_arm(target_pos) -> bool:
        # 使用逆运动学计算关节角度
        # 发送控制信号到仿真环境
        
    def grasp() -> bool:
        # 关闭夹手
        
    def release() -> bool:
        # 打开夹手
```

**特点：**
- 逆运动学求解
- 工作空间保护
- 碰撞检测
- 实时渲染选项

---

### 2. skills.py

**职责：** 高层工具函数（给 LLM 调用）

**导出的工具：**

```python
perceive_environment() -> str
    # 返回自然语言环境描述
    # 用于 LLM 感知当前状态

move_arm_to(x: float, y: float, z: float) -> str
    # 移动机械臂末端到目标位置
    # 返回执行结果

grasp() -> str
    # 关闭夹手，抓取物体

release() -> str
    # 打开夹手，释放物体
```

**特点：**
- 抽象了底层复杂性
- 返回人类可读的反馈
- LLM 友好的接口

---

### 3. main.py

**职责：** 决策循环和 LLM 集成

**核心流程：**

```python
def run_llm_mode(max_steps, provider, model):
    # 1. 初始化 LLM 客户端
    client = OpenAI(...)
    
    # 2. 构建工具列表（给 LLM）
    tools = _build_tools()
    
    # 3. 系统提示词
    system_prompt = "You are a robot arm control agent..."
    
    # 4. 循环
    for step in range(max_steps):
        # 感知 → 决策 → 执行 → 反馈
        
    # 5. 清理
    close_skills()
```

**关键函数：**

- `_current_state()` - 获取当前状态
- `_build_tools()` - 构建 function_calling 工具定义
- `_TOOL_MAP` - 工具名到函数的映射
- `demo_policy()` - 演示模式的硬编码策略

---

### 4. record_video.py

**职责：** 录制仿真运行为 MP4 视频

**核心流程：**

```python
def record_llm_video(output, max_steps, fps, frames_per_step, provider):
    # 1. 初始化环境
    controller = _ensure_initialized()
    
    # 2. 运行 LLM 循环
    for step in range(max_steps):
        # LLM 决策
        response = client.chat.completions.create(...)
        
        # 执行工具
        tool_func(**args)
        
        # 捕获帧
        for _ in range(frames_per_step):
            rgb = controller.env.render()
            frames.append(rgb)
    
    # 3. 编码为 MP4
    out = cv2.VideoWriter(output_path, ...)
    for frame in frames:
        out.write(frame)
    out.release()
```

---

## 工作流程详解

### LLM 闭环控制过程

```
Step 1: 感知 - Read Current State
  ↓
  env → perceive_environment() → 场景描述
  例："机械臂在 x=0.2, y=0.0, z=0.5. 
       绿色物体在 x=-0.5, y=0.2, z=0.0. 
       目标位置在 x=-0.2, y=0.3, z=0.1"
  ↓
Step 2: 推理 - LLM Decision
  ↓
  LLM 根据 system_prompt 和当前状态进行推理
  调用工具函数
  例："我需要向绿色物体移动。先向上方移动..."
  调用 move_arm_to(x=-0.5, y=0.2, z=0.12)
  ↓
Step 3: 执行 - Execute Tool
  ↓
  skill → IK 计算 → 关节控制 → PyBullet 仿真
  ↓
Step 4: 反馈 - Get Result
  ↓
  "已移动到目标位置。"
  ↓
Step 5: 添加到历史 & 重复
  ↓
  检查是否完成任务
  否 → 回到 Step 1
  是 → 完成
```

---

## 设计模式

### 1. 单例模式

```python
# env_wrapper.py
_controller: RobotArmController | None = None

def _ensure_initialized() -> RobotArmController:
    global _controller
    if _controller is None:
        _controller = RobotArmController()
    return _controller
```

**优点：** 共享环境状态，节省资源

### 2. 依赖注入

```python
# skills.py 依赖 env_wrapper
from env_wrapper import _ensure_initialized

def perceive_environment():
    controller = _ensure_initialized()
    # 使用 controller
```

**优点：** 解耦合，易于测试

### 3. 适配器模式

```python
# OpenRouter API 兼容 OpenAI SDK
client = OpenAI(
    api_key=key,
    base_url="https://openrouter.ai/api/v1"
)
```

**优点：** 统一不同 API 的接口

---

## 扩展点

### 添加新的工具函数

1. 在 `skills.py` 中实现函数
2. 在 `main.py` 的 `_build_tools()` 中添加定义
3. 在 `_TOOL_MAP` 中注册

### 支持新的 LLM 提供商

1. 在 `main.py` 中增加 `provider` 判断
2. 初始化相应的 OpenAI 兼容客户端
3. 测试工具调用

### 自定义控制策略

1. 修改 `demo_policy()` 的状态机
2. 或修改 LLM 的 `system_prompt`

---

## 性能考虑

| 组件 | 平均耗时 | 瓶颈 |
|------|--------|------|
| 初始化 | 2-3s | PyBullet 初始化 |
| 单步推理 | 2-5s | LLM API 延迟 |
| IK 计算 | 10-50ms | 复杂工作空间 |
| 渲染 | 1-2s/秒 | GPU 吞吐量 |

---

## 安全考虑

### 工作空间保护

```python
# env_wrapper.py
WORKSPACE_BOUNDS = {
    'x': (-1.0, 0.2),
    'y': (-0.6, 0.6),
    'z': (0.0, 1.2)
}

# 在 move_arm_to 中验证
assert x_min < x < x_max
```

### 碰撞检测

```python
# panda_gym 自带碰撞检测
# 如果触发碰撞，任务失败
```

---

## 下一步

- 📖 [项目讲解](PROJECT_GUIDE.md) - 源代码详解
- ⚡ [快速参考](QUICK_REFERENCE.md) - 命令速查
- 🐛 [故障排查](TROUBLESHOOTING.md) - 调试技巧
