# Panda Pick & Place 闭环控制 - 使用指南

## 项目概览
这是一个基于大语言模型（LLM）的机械臂自主控制系统。使用 Franka Panda 机械臂在 `panda-gym` 仿真环境中完成 **Pick & Place**（夹取、移动、放置）任务。

## 架构
- **env_wrapper.py**: 底层环境控制模块
  - `RobotArmController`: 高级宏动作控制器
  - 提供 `step_to_position()`, `control_gripper()`, `get_observation()` 等方法

- **skills.py**: OpenClaw 兼容的技能接口
  - `perceive_environment()`: 获取场景状态
  - `move_arm_to(x, y, z)`: 移动末端执行器
  - `grasp()`: 闭合夹爪
  - `release()`: 张开夹爪

- **main.py**: 感知-决策-行动主循环
  - 支持两种模式：`demo`（硬编码状态机）和 `llm`（大模型驱动）
  - 支持 OpenAI 和 OpenRouter 两种 API 提供商

## 安装依赖

### 1. 基础环境依赖
```bash
pip install gymnasium panda-gym numpy
```

### 2. LLM API 依赖
```bash
pip install openai
```

## 使用方法

### 模式 A：演示模式（无需 API Key）
硬编码的有限状态机策略，相当于预编程的控制流程。

```bash
python main.py --mode demo --max-steps 50
```

### 模式 B：LLM 模式 + OpenRouter API（推荐）

#### 第1步：获取 OpenRouter API Key
1. 访问 [https://openrouter.ai/](https://openrouter.ai/)
2. 注册账户并获取 API Key

#### 第2步：设置环境变量
```bash
export OPENROUTER_API_KEY="your-openrouter-api-key-here"
```

#### 第3步：运行程序
```bash
python main.py --mode llm --provider openrouter --max-steps 50
```

**可选**：指定特定模型
```bash
export LLM_MODEL="meta-llama/llama-3-70b-instruct"
python main.py --mode llm --provider openrouter --max-steps 50
```

### 模式 C：LLM 模式 + OpenAI API

#### 第1步：获取 OpenAI API Key
1. 访问 [https://platform.openai.com/](https://platform.openai.com/)
2. 获取 API Key

#### 第2步：设置环境变量
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

#### 第3步：运行程序
```bash
python main.py --mode llm --provider openai --max-steps 50
```

## 执行流程（LLM 模式）

以下是 LLM 驱动的闭环控制流程：

```
┌───────────────────────────────────────────────────────────────┐
│ 1. PERCEPTION（感知）                                          │
│    LLM 调用 perceive_environment()，获取：                     │
│    - 末端执行器位置                                            │
│    - 夹爪宽度                                                  │
│    - 物体位置（绿色方块）                                      │
│    - 目标位置（不可见）                                        │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌───────────────────────────────────────────────────────────────┐
│ 2. DECISION & PLANNING（决策与规划）                           │
│    LLM 根据当前状态推理下一个动作：                            │
│    - 如果还未抓取：计划移动到物体上方                          │
│    - 如果已抓取：计划移动到目标上方                            │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌───────────────────────────────────────────────────────────────┐
│ 3. ACTION EXECUTION（动作执行）                                │
│    LLM 调用工具函数执行决定的动作：                            │
│    - move_arm_to(x, y, z)       # 绝对位置移动                 │
│    - grasp()                     # 闭合夹爪                    │
│    - release()                   # 张开夹爪                    │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌───────────────────────────────────────────────────────────────┐
│ 4. FEEDBACK & LOOP（反馈与循环）                               │
│    - 环境执行该动作（内部循环 step()）                         │
│    - 返回执行结果给 LLM                                        │
│    - LLM 评估并返回步骤 1，继续循环                           │
│    - 当物体放置在目标位置或达到 max_steps 时退出               │
└───────────────────────────────────────────────────────────────┘
```

## 工作空间坐标范围
机械臂末端执行器可到达的工作空间（单位：米）：

| 坐标 | 最小值 | 最大值 |
|------|--------|--------|
| X    | -1.0   | 0.2    |
| Y    | -0.6   | 0.6    |
| Z    | 0.0    | 1.2    |

## 常见问题 (FAQ)

### Q1: 如何选择 OpenRouter 的模型？
```bash
# 查看可用模型列表（OpenRouter 网站）
export LLM_MODEL="meta-llama/llama-3-70b-instruct"
python main.py --mode llm --provider openrouter --max-steps 50
```

### Q2: 程序运行时出现 "Error: target is outside the robot workspace"？
这说明 LLM 给出了超出工作范围的坐标。程序会自动返回错误信息给 LLM，让其自我纠正。

### Q3: 如何调试 LLM 的决策过程？
程序会实时打印每一步的 LLM 推理过程和工具调用：
```
[LLM 0] Calling move_arm_to({'x': -0.2, 'y': 0.1, 'z': 0.15})
[LLM 0] -> End-effector moved to approximately [...] (distance to target: 0.0234 m).
```

### Q4: 演示模式（demo）的运行流程是什么？
演示模式使用硬编码的有限状态机，按照以下步骤执行抓取任务：
1. 打开夹爪
2. 移动到物体上方 10cm
3. 下降到物体表面 3cm
4. 闭合夹爪抓住物体
5. 提升物体 15cm
6. 移动到目标位置上方
7. 下降到目标位置
8. 释放物体

## 环境变量速查表

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `OPENROUTER_API_KEY` | 无 | OpenRouter API 密钥（llm + openrouter 时必需） |
| `OPENAI_API_KEY` | 无 | OpenAI API 密钥（llm + openai 时必需） |
| `LLM_MODEL` | 见下表 | 指定使用的 LLM 模型 |

## 默认模型

| 提供商 | 默认模型 |
|--------|---------|
| OpenRouter | `meta-llama/llama-2-70b-chat` |
| OpenAI | `gpt-4o-mini` |

## 命令行参数

```bash
python main.py --help

usage: main.py [-h] [--mode {demo,llm}] [--provider {openai,openrouter}] 
               [--max-steps MAX_STEPS]

Panda Pick & Place closed-loop demo

options:
  -h, --help         show this help message and exit
  --mode {demo,llm}  Control mode: demo=hard-coded policy, llm=LLM function calling 
                     (default: demo)
  --provider {openai,openrouter}
                     LLM service provider: openai or openrouter (default: openrouter)
  --max-steps MAX_STEPS
                     Maximum number of decision steps (default: 40)
```

## 运行示例

### 例1：快速测试（演示模式）
```bash
python main.py --mode demo --max-steps 30
```

### 例2：使用 OpenRouter 的 Llama2（生产推荐）
```bash
export OPENROUTER_API_KEY="sk_live_..."
python main.py --mode llm --provider openrouter --max-steps 50
```

### 例3：使用 OpenAI GPT-4o
```bash
export OPENAI_API_KEY="sk_..."
python main.py --mode llm --provider openai --max-steps 50
```

## 性能指标

- **决策延迟**: 取决于 LLM API 响应时间（通常 2-10 秒）
- **运动精度**: ±1 cm（末端执行器对目标坐标）
- **任务完成时间**: 演示模式约 10-15 秒；LLM 模式约 30-60 秒

## 渲染模式
当前配置为 `rgb_array`（无图形界面）。如果需要可视化：
- 修改 `env_wrapper.py` 中 `render_mode="human"`
- 需要配置 X11/WSLg 显示驱动

## 许可证与致谢
- 仿真环境: [panda-gym](https://github.com/alexius-huang/panda-gym)
- LLM 工具框架: OpenAI SDK
- API 提供商: OpenAI, OpenRouter

## 联系支持
如有问题，请检查：
1. API Key 是否正确设置
2. 网络连接是否正常
3. 模型名称是否正确
