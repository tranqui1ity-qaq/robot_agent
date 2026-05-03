# 🐛 故障排查指南

遇到问题？这里有常见问题的解决方案。

---

## 环境和安装问题

### ❌ ModuleNotFoundError: No module named 'panda_gym'

**原因：** 依赖未安装

**解决方案：**
```bash
# 重新安装依赖
pip install -r requirements.txt

# 或单独安装
pip install panda-gym gymnasium[classic_control] opencv-python
```

### ❌ Python version X.Y is not supported

**原因：** Python 版本低于 3.10

**解决方案：**
```bash
# 检查 Python 版本
python --version

# 升级 Python（macOS）
brew install python@3.10
python3.10 -m venv venv

# 升级 Python（Linux）
sudo apt install python3.10
python3.10 -m venv venv

# 获取 Python 3.10+（Windows）
# 访问 https://www.python.org 下载安装
```

### ❌ Permission denied when installing

**原因：** pip 权限不足

**解决方案：** 使用虚拟环境（不要用 sudo pip）
```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
# venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

---

## API 和认证问题

### ❌ OPENROUTER_API_KEY is not set

**原因：** 环境变量未设置

**解决方案：**
```bash
# 检查是否设置
echo $OPENROUTER_API_KEY

# 设置环境变量（临时）
export OPENROUTER_API_KEY="sk_your_key_here"

# 设置环境变量（永久，Linux/macOS）
echo 'export OPENROUTER_API_KEY="sk_..."' >> ~/.bashrc
source ~/.bashrc

# 设置环境变量（Windows）
# 1. Win + X → 系统设置
# 2. 高级系统设置 → 环境变量 → 新建
# 3. OPENROUTER_API_KEY = sk_...
```

### ❌ 401 Unauthorized - Invalid API Key

**原因：** API Key 无效或过期

**解决方案：**
```bash
# 1. 验证 API Key 是否正确
echo $OPENROUTER_API_KEY

# 2. 生成新的 API Key
# 访问 https://openrouter.ai/keys

# 3. 更新环境变量
export OPENROUTER_API_KEY="sk_new_key"
```

### ❌ 404 Not Found - Model not available

**原因：** 模型在 OpenRouter 上不可用

**解决方案：**
```bash
# 查看可用模型列表
# 访问 https://openrouter.ai/models

# 或使用推荐模型
export LLM_MODEL="google/gemini-3-flash-preview"
export LLM_MODEL="anthropic/claude-3.5-sonnet"

# 重试
python main.py --mode llm --max-steps 50
```

### ❌ Rate limit exceeded

**原因：** API 配额已用尽

**解决方案：**
```bash
# 减少请求频率
sleep 60
python main.py --mode llm --max-steps 10

# 或使用不同的模型（可能有独立的限额）
export LLM_MODEL="mistralai/mistral-large"
```

---

## PyBullet 和渲染问题

### ❌ RuntimeError: No OpenGL context found

**原因：** 缺少 OpenGL 库

**解决方案（Linux）：**
```bash
# 安装图形库
sudo apt-get install libgl1-mesa-glx libglib2.0-0

# 如果仍然失败，禁用渲染
python main.py --render false
```

**解决方案（macOS）：**
```bash
# 通常不需要，但如果出现问题：
brew install glfw3 glew
```

**解决方案（Windows）：**
```bash
# 通常不需要，但如果失败：
# 1. 更新显卡驱动
# 2. 运行在兼容模式下
```

### ❌ Cannot connect to display

**原因：** 无显示屏或无 GUI 环境

**解决方案：**
```bash
# 禁用显示
python main.py --render false

# 或后台运行
nohup python main.py --mode llm > robot.log 2>&1 &
```

### ❌ Segmentation fault

**原因：** 通常是 PyBullet 的已知问题

**解决方案：**
```bash
# 重新安装 panda-gym
pip install --force-reinstall panda-gym

# 或更新依赖
pip install --upgrade panda-gym gymnasium

# 尝试录制模式（可能更稳定）
bash record_video.sh
```

---

## LLM 推理问题

### ❌ Timeout waiting for LLM response

**原因：** LLM 响应太慢或网络不稳定

**解决方案：**
```bash
# 使用更快的模型
export LLM_MODEL="google/gemini-3-flash-preview"

# 减少 max-steps
python main.py --mode llm --max-steps 20

# 尝试重新连接
python main.py --mode llm --max-steps 50  # 再试一次
```

### ❌ ValueError: Tool call parsing failed

**原因：** LLM 返回的工具调用格式错误

**解决方案：**
```bash
# 更换模型（某些模型更稳定）
export LLM_MODEL="anthropic/claude-3.5-sonnet"

# 或使用更详细的 system_prompt
# 编辑 main.py 中的 system_prompt
```

### ❌ Connection refused - Connect timeout

**原因：** 网络连接问题或 API 服务故障

**解决方案：**
```bash
# 检查网络连接
ping openrouter.ai

# 检查防火墙
# Windows: 检查防火墙是否阻止 Python
# Linux: sudo ufw status

# 使用代理（如果需要）
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"

# 尝试其他模型或提供商
export OPENAI_API_KEY="sk_..."
python main.py --mode llm --provider openai
```

---

## 视频录制问题

### ❌ No module named 'cv2'

**原因：** opencv 未安装

**解决方案：**
```bash
pip install opencv-python
```

### ❌ No frames captured

**原因：** 渲染失败或 frames 缓冲区为空

**解决方案：**
```bash
# 增加每步帧数
bash record_video.sh demo.mp4 50 30 openrouter 60

# 检查 PyBullet 是否正常工作
python main.py --mode demo --max-steps 10
```

### ❌ Video file is corrupted

**原因：** 编码错误或中途中断

**解决方案：**
```bash
# 删除旧的不完整文件
rm videos/*.mp4

# 重新录制
bash record_video.sh demo.mp4 30 20 openrouter 60
```

---

## 性能问题

### ❌ Out of memory (OOM)

**原因：** 内存不足

**解决方案：**
```bash
# 减少 max-steps
python main.py --mode llm --max-steps 20

# 减少录视频的帧数
bash record_video.sh demo.mp4 30 10 openrouter 30

# 关闭其他应用
# 或增加系统虚拟内存
```

### ❌ Slow response from LLM

**原因：** 使用了较大的模型或网络慢

**解决方案：**
```bash
# 使用更快的模型
export LLM_MODEL="google/gemini-3-flash-preview"

# 减少 max-steps
python main.py --mode llm --max-steps 30

# 检查网络
ping openrouter.ai
```

---

## 调试技巧

### 启用详细日志

```bash
# Python 调试模式
python -u main.py --mode llm --max-steps 10 2>&1 | tee debug.log

# 查看完整错误
python main.py --mode llm --max-steps 10 2>&1 | tail -50
```

### 测试各个组件

```bash
# 测试 PyBullet
python -c "from panda_gym import make; print(make('PandaReach-v3'))"

# 测试 OpenAI SDK
python -c "from openai import OpenAI; print('✓ OK')"

# 测试 OpenCV
python -c "import cv2; print(f'OpenCV {cv2.__version__}')"
```

### 后台运行并监控

```bash
# 启动后台任务
nohup python main.py --mode llm > robot.log 2>&1 &

# 实时查看日志
tail -f robot.log

# 查看进程
ps aux | grep python

# 杀死进程
kill <PID>
```

---

## 获取帮助

1. 📖 查看 [快速参考](QUICK_REFERENCE.md)
2. 🔍 搜索 [GitHub Issues](https://github.com/tranqui1ity-qaq/robot_agent/issues)
3. 💬 提交新 Issue
4. 📧 联系维护者

---

## 常见问题 FAQ

**Q: 为什么机械臂没有移动？**
A: 检查是否是演示模式。使用 `--mode llm` 时需要设置 API Key。

**Q: 如何选择最便宜的模型？**
A: 使用 `google/gemini-3-flash-preview`，成本约 $0.01/任务。

**Q: 可以录制没有 LLM 推理的视频吗？**
A: 录制脚本目前仅支持 LLM 模式。

**Q: 如何在无显示屏的服务器上运行？**
A: 使用 `--render false` 或直接录视频（视频录制会自动禁用显示）。

**Q: 支持 GPU 加速吗？**
A: 仿真部分可以使用 GPU（需要 CUDA），但主要瓶颈是 LLM API 延迟。

---

<div align="center">

**还是有问题？** [提交 Issue](https://github.com/tranqui1ity-qaq/robot_agent/issues) 💬

</div>
