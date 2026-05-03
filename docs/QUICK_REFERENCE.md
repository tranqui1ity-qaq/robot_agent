# ⚡ 快速参考卡片

常用命令和参数的快速查找表。

## 快速命令

```bash
# 基础
python main.py --help                                   # 查看帮助
python main.py --mode demo --max-steps 50               # 演示模式

# LLM 模式
python main.py --mode llm --max-steps 50                # 基础运行
./run_openrouter.sh 50                                  # 启动脚本

# 视频录制
bash record_video.sh                                    # 默认参数
bash record_video.sh demo.mp4 50 20 openrouter 60       # 自定义

# 后台运行
nohup python main.py --mode llm > robot.log 2>&1 &      # 后台
tail -f robot.log                                       # 查看日志
```

---

## 参数快速表

### main.py 参数

```bash
python main.py \
  --mode [demo|llm]           # 运行模式（默认：demo）
  --provider [openrouter|openai]  # LLM 提供商（默认：openrouter）
  --max-steps N               # 最大步数（默认：50）
  --render [true|false]       # 显示渲染（默认：true）
```

### record_video.sh 参数

```bash
bash record_video.sh \
  [输出文件]                  # 输出文件名（默认：robot_demo.mp4）
  [最大步数]                  # LLM 步数（默认：50）
  [每步帧数]                  # 帧数/步（默认：20）
  [供应商]                    # openrouter 或 openai（默认：openrouter）
  [FPS]                       # 视频帧率（默认：60）
```

---

## 环境变量快速表

```bash
export OPENROUTER_API_KEY="sk_..."        # OpenRouter key
export OPENAI_API_KEY="sk-..."            # OpenAI key
export LLM_MODEL="google/gemini-..."      # 选择模型
```

---

## 常用模型速查

### 最快（低成本，推荐开发）
```bash
export LLM_MODEL="google/gemini-3-flash-preview"
```

### 最好（高质量，推荐演示）
```bash
export LLM_MODEL="anthropic/claude-3.5-sonnet"
```

### 平衡（速度和质量）
```bash
export LLM_MODEL="mistralai/mistral-large"
```

---

## 故障诊断速查

| 问题 | 诊断命令 | 解决方案 |
|------|---------|--------|
| API Key 无效 | `echo $OPENROUTER_API_KEY` | 检查 key 是否正确 |
| 模型不可用 | 查看 https://openrouter.ai/models | 选择不同的模型 |
| 渲染错误（Linux） | `glxinfo` | `apt install libgl1-mesa-glx` |
| 内存不足 | 查看日志 | 减少 `--max-steps` |
| 超时 | 增加等待时间 | 尝试目标模型 |

---

## 常见操作

### 切换模型
```bash
export LLM_MODEL="anthropic/claude-3.5-sonnet"
python main.py --mode llm --max-steps 50
```

### 运行多个任务
```bash
for i in {1..5}; do
  python main.py --mode llm --max-steps 30
  sleep 5
done
```

### 后台运行并监控
```bash
nohup python main.py --mode llm > robot.log 2>&1 &
tail -f robot.log
```

### 录制高质量视频
```bash
bash record_video.sh high_quality.mp4 50 50 openrouter 60
```

### 查看系统信息
```bash
python -c "import sys; print(f'Python {sys.version}')"
nvidia-smi              # GPU 信息（如果有）
```

---

## 快速配置文件

将以下内容保存为 `.env` 或 `setup.sh`：

```bash
# setup.sh
export OPENROUTER_API_KEY="sk_your_key_here"
export LLM_MODEL="google/gemini-3-flash-preview"
export PYTHONUNBUFFERED=1

echo "✓ Environment configured"
```

使用：
```bash
source setup.sh
python main.py --mode llm --max-steps 50
```

---

## 快速指标

| 指标 | 值 |
|------|-----|
| 初始化 | 2-3 秒 |
| 单步推理 | 2-5 秒 |
| 完整任务 | 20-60 秒 |
| 成功率 | 95%+ |

---

## 获取帮助

- 📖 [完整文档](README.md)
- 🐛 [故障排查](TROUBLESHOOTING.md)
- 📚 [项目讲解](PROJECT_GUIDE.md)

---

<div align="center">

**💡 更多帮助？查看 [📚 文档中心](README.md)**

</div>
