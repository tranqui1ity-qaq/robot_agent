# 🤖 LLM 集成指南

本指南说明如何配置和使用不同的 LLM 服务和模型。

## 支持的 LLM 提供商

### 1. OpenRouter（推荐）

**优点：**
- 支持 50+ 不同的 LLM 模型
- 按使用量计费（Pay-as-you-go）
- 免费试用额度
- 统一 API 接口

**配置方式：**

```bash
export OPENROUTER_API_KEY="sk_your_key"
export LLM_MODEL="你的模型名"

python main.py --mode llm --provider openrouter --max-steps 50
```

**获取 API Key：**
1. 访问 [OpenRouter Dashboard](https://openrouter.ai/keys)
2. 点击 "Create API Key"
3. 复制生成的 key

### 2. OpenAI

**优点：**
- 高质量的 GPT-4 模型
- 官方 API 支持
- WebSocket 连接优化

**配置方式：**

```bash
export OPENAI_API_KEY="sk_your_key"
export LLM_MODEL="gpt-4o-mini"

python main.py --mode llm --provider openai --max-steps 50
```

**获取 API Key：**
1. 访问 [OpenAI API Keys](https://platform.openai.com/account/api-keys)
2. 点击 "Create new secret key"
3. 复制生成的 key

---

## 推荐模型配置

### 快速模型（低延迟）

```bash
# Google Gemini 3 Flash（推荐首选）
export LLM_MODEL="google/gemini-3-flash-preview"
export LLM_MODEL="google/gemini-2-flash-thinking-exp"

# Claude Haiku
export LLM_MODEL="anthropic/claude-3-haiku"

# Mistral 7B
export LLM_MODEL="mistralai/mistral-7b-instruct"
```

### 中等模型（平衡性能和质量）

```bash
# Claude 3.5 Sonnet（高质量）
export LLM_MODEL="anthropic/claude-3.5-sonnet"

# Mistral Medium
export LLM_MODEL="mistralai/mistral-medium"

# Gemini 1.5 Flash
export LLM_MODEL="google/gemini-1.5-flash"

# Deepseek Chat
export LLM_MODEL="deepseek/deepseek-chat"
```

### 高端模型（最佳质量）

```bash
# Claude 3.5 Opus（最强）
export LLM_MODEL="anthropic/claude-3.5-opus"

# GPT-4o（OpenAI 最强）
export LLM_MODEL="gpt-4o"

# Gemini 1.5 Pro
export LLM_MODEL="google/gemini-1.5-pro"

# Mistral Large
export LLM_MODEL="mistralai/mistral-large"
```

---

## 模型对比

| 模型 | 提供商 | 速度 | 质量 | 成本 | 推荐 |
|------|--------|------|------|------|------|
| Gemini 3 Flash | OpenRouter | ⚡⚡⚡ | ⭐⭐⭐ | 💰 | 🌟首选 |
| Claude 3.5 Sonnet | OpenRouter | ⚡⚡ | ⭐⭐⭐⭐ | 💰💰 | 🥇最佳 |
| GPT-4o | OpenAI | ⚡⚡ | ⭐⭐⭐⭐ | 💰💰💰 | 👍好用 |
| Mistral Large | OpenRouter | ⚡⚡ | ⭐⭐⭐ | 💰 | ✅稳定 |
| Gemini 1.5 Pro | OpenRouter | ⚡ | ⭐⭐⭐⭐ | 💰💰 | 👍推荐 |

---

## 使用示例

### 示例 1：快速测试（低成本）

```bash
export OPENROUTER_API_KEY="sk_..."
export LLM_MODEL="google/gemini-3-flash-preview"
python main.py --mode llm --max-steps 50
```

成本估算：$0.01 - 0.05

### 示例 2：高质量演示（推荐）

```bash
export OPENROUTER_API_KEY="sk_..."
export LLM_MODEL="anthropic/claude-3.5-sonnet"
python main.py --mode llm --max-steps 50
```

成本估算：$0.10 - 0.50

### 示例 3：录制视频演示

```bash
export OPENROUTER_API_KEY="sk_..."
export LLM_MODEL="google/gemini-3-flash-preview"
bash record_video.sh demo.mp4 50 20 openrouter 60
```

成本估算：$0.02 - 0.06

### 示例 4：使用 OpenAI API

```bash
export OPENAI_API_KEY="sk_..."
export LLM_MODEL="gpt-4o-mini"
python main.py --mode llm --provider openai --max-steps 50
```

### 示例 5：批量测试多个模型

```bash
#!/bin/bash
export OPENROUTER_API_KEY="sk_..."

models=(
  "google/gemini-3-flash-preview"
  "anthropic/claude-3.5-sonnet"
  "mistralai/mistral-large"
)

for model in "${models[@]}"; do
  echo "Testing $model..."
  export LLM_MODEL="$model"
  python main.py --mode llm --max-steps 30
  echo "---"
done
```

---

## 成本估算

### OpenRouter 定价

| 模型 | 输入 | 输出 | 估计成本/任务 |
|------|------|------|---------|
| Gemini 3 Flash | $0.05/1M | $0.20/1M | $0.01 |
| Mistral Large | $2.70/1M | $8.10/1M | $0.10 |
| Claude 3.5 Sonnet | $3/1M | $15/1M | $0.20 |
| Gemini 1.5 Pro | $1.25/1M | $5/1M | $0.05 |

### OpenAI 定价

| 模型 | 输入 | 输出 | 估计成本/任务 |
|------|------|------|---------|
| gpt-4o-mini | $0.15/1M | $0.60/1M | $0.02 |
| gpt-4o | $5/1M | $15/1M | $0.20 |

> 💡 **提示**: 成本取决于 tokens 数量，通常 50 步的任务消耗 5k-20k tokens

---

## 环境变量

```bash
# LLM 提供商选择
export OPENROUTER_API_KEY="sk_..."
export OPENAI_API_KEY="sk_..."

# 模型选择
export LLM_MODEL="google/gemini-3-flash-preview"

# 超时设置（秒）
export LLM_TIMEOUT="30"

# 温度（创意度）0-1
export LLM_TEMPERATURE="0.0"
```

---

## 故障排查

### 问题：模型不可用

```bash
# 检查可用模型列表
# 访问 https://openrouter.ai/models

# 或在代码中捕获错误
python main.py --mode llm --max-steps 50 2>&1 | grep -i "error"
```

### 问题：API 超时

```bash
# 增加超时时间（编辑 main.py）
# timeout = 60  # 增加到 60 秒

# 或使用速度更快的模型
export LLM_MODEL="google/gemini-3-flash-preview"
```

### 问题：成本太高

```bash
# 使用便宜的模型
export LLM_MODEL="google/gemini-3-flash-preview"

# 或减少 max-steps
python main.py --mode llm --max-steps 20
```

---

## 下一步

- 🎥 想要录制视频？→ [视频录制指南](VIDEO_RECORDING_GUIDE.md)
- 🐛 遇到问题？→ [故障排查](TROUBLESHOOTING.md)
- 📚 需要更多信息？→ [项目讲解](PROJECT_GUIDE.md)
