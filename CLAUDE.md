# 项目上下文：基于大模型（OpenClaw）的机械臂闭环控制 Demo

本项目旨在构建一个“感知-决策-控制”闭环系统。我们使用大语言模型（通过 OpenClaw 框架）作为高级决策大脑，来控制 `panda-gym` 仿真环境中的 Franka Panda 机械臂完成简单的“抓取与放置”（Pick and Place）任务。

## 技术栈
- **仿真环境**: `panda-gym` (基于 PyBullet)
- **智能体框架**: OpenClaw (依赖工具/技能调用)
- **语言**: Python 3.10+

## 核心设计理念 (重要)
大模型无法像传统 RL 算法那样以 100Hz 的频率输出连续的微小关节控制量。因此，**必须将连续环境离散化、高级化**。
- **动作空间改造**: 大模型不输出 `[dx, dy, dz]`，而是输出绝对坐标指令或宏动作，例如 `move_to(x, y, z)`。底层代码需要自动计算插值并在 `panda-gym` 中循环 `step()` 直到抵达目标点。
- **步进式执行**: 环境在等待大模型推理时应保持静止（阻塞），大模型下达指令后，环境执行该宏动作，然后再次暂停并返回最新状态。

## 模块划分与开发任务

请按照以下三个阶段进行代码编写：

### 阶段 1：环境与底层控制封装 (`env_wrapper.py`)
- 实例化 `panda-gym` 的 `PandaPickAndPlace-v3` (或类似) 环境。
- 编写一个包裹类 `RobotArmController`：
  - 包含 `step_to_position(target_x, target_y, target_z)` 方法：将绝对坐标转化为环境所需的动作向量，并在内部循环执行 `env.step()` 直到末端执行器到达目标位置（允许一定误差）。
  - 包含 `control_gripper(open: bool)` 方法：控制夹爪开合。
  - 包含 `get_observation()` 方法：返回一个包含关键信息的字典或格式化字符串（机械臂末端坐标、目标物体坐标、夹爪开合状态）。

### 阶段 2：OpenClaw 技能/工具定义 (`skills.py`)
为 OpenClaw 编写可以直接调用的 Python 函数（必须包含清晰的 Google Style Docstrings，以便 LLM 理解如何调用）：
1. `perceive_environment()`: 调用底层的 `get_observation()`，向大模型返回当前场景的文字/JSON 描述。
2. `move_arm_to(x: float, y: float, z: float)`: 移动机械臂末端到指定坐标。
3. `grasp()`: 闭合夹爪。
4. `release()`: 张开夹爪。
*(提示：这些函数内部需调用 `env_wrapper.py` 中的实例)*

### 阶段 3：主循环与闭环集成 (`main.py`)
- 初始化环境和 OpenClaw Agent。
- 编写主循环 (Perception -> Decision -> Action loop)：
  1. 智能体调用 `perceive_environment()` 获取初始状态。
  2. 智能体推理出下一步动作，并调用对应的控制工具（如 `move_arm_to`）。
  3. 执行完毕后，环境更新，智能体再次感知，直到物体被成功放置到目标位置。

## 代码规范要求
- 所有函数必须使用 **Type Hints (类型提示)**。
- 对于 `panda-gym` 的坐标计算，统一使用 `numpy`。
- 在 `main.py` 运行时，需开启环境的渲染 (render)，以便用户能直观看到机械臂的运动过程。
- 做好异常处理：例如大模型给出了超出机械臂工作空间（Workspace）的坐标时，工具函数应捕获错误并返回带有提示信息的字符串给大模型，让大模型自我纠正，而不是直接让程序崩溃。