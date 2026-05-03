# ⚡ 快速开始指南

5 分钟快速上手项目。

## 前置条件

- Python 3.10+
- API Key（[OpenRouter](https://openrouter.ai) 或 [OpenAI](https://platform.openai.com)）

## 第 1 步：克隆和安装

```bash
git clone https://github.com/tranqui1ity-qaq/robot_agent.git
cd robot_agent
pip install -r requirements.txt
```

## 第 2 步：设置 API Key

```bash
# OpenRouter（推荐）
export OPENROUTER_API_KEY="sk_your_key_here"

# 或 OpenAI
export OPENAI_API_KEY="sk_your_key_here"
```

## 第 3 步：运行演示

### 方式 A：演示模式（无需 API Key）

```bash
python main.py --mode demo --max-steps 50
```

### 方式 B：LLM 模式（需要 API Key）

```bash
python main.py --mode llm --max-steps 50 --provider openrouter
```

### 方式 C：使用启动脚本

```bash
./run_openrouter.sh 50
```

### 方式 D：录制视频（新功能）

```bash
bash record_video.sh demo.mp4 50 20 openrouter 60
```

---

## 常用命令

```bash
# 查看帮助
python main.py --help

# 使用不同的 LLM 模型
export LLM_MODEL="anthropic/claude-3.5-sonnet"
python main.py --mode llm --max-steps 50

# 运行更多步数
python main.py --mode llm --max-steps 100

# 后台运行
nohup python main.py --mode llm > robot.log 2>&1 &
```

---

## 环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `OPENROUTER_API_KEY` | OpenRouter API Key | `sk_live_...` |
| `OPENAI_API_KEY` | OpenAI API Key | `sk-...` |
| `LLM_MODEL` | 使用的模型 | `mistralai/mistral-large` |

---

## 下一步

- ✅ 运行了演示，想要更详细的说明？→ [📚 项目指南](PROJECT_GUIDE.md)
- ✅ 想要录制视频？→ [🎥 视频录制指南](VIDEO_RECORDING_GUIDE.md)
- ✅ 遇到问题？→ [🐛 故障排查](TROUBLESHOOTING.md)
- ✅ 需要快速参考？→ [⚡ 快速参考](QUICK_REFERENCE.md)

---

## 获取帮助

- 文档：[📚 文档中心](README.md)
- Issues：[GitHub Issues](https://github.com/tranqui1ity-qaq/robot_agent/issues)
