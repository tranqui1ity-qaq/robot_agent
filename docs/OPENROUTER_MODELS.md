# OpenRouter 可用模型快速参考

## 推荐模型（已验证可用）

### 经济型（快速、便宜）
```bash
# GPT-3.5 Turbo（最快、最便宜）
export LLM_MODEL="openai/gpt-3.5-turbo"
./run_openrouter.sh

# Mistral Large
export LLM_MODEL="mistralai/mistral-large"
./run_openrouter.sh
```

### 中端（平衡质量与成本）
```bash
# GPT-4 Turbo（推荐用于 Pick & Place）
export LLM_MODEL="openai/gpt-4-turbo"
./run_openrouter.sh

# Claude 3.5 Sonnet（高质量推理）
export LLM_MODEL="anthropic/claude-3.5-sonnet"
./run_openrouter.sh
```

### 高端（最强推理能力）
```bash
# Claude 3 Opus
export LLM_MODEL="anthropic/claude-3-opus"
./run_openrouter.sh
```

## 如何查找 OpenRouter 上的所有模型

1. 访问 https://openrouter.ai/models
2. 查看所有可用的模型及其 ID
3. 模型 ID 格式通常是：`provider/model-name`

## 常见模型 ID 格式

| 提供商 | 模型 ID 格式 | 示例 |
|--------|-----------|------|
| OpenAI | `openai/{model}` | `openai/gpt-4-turbo`, `openai/gpt-3.5-turbo` |
| Anthropic | `anthropic/{model}` | `anthropic/claude-3.5-sonnet`, `anthropic/claude-3-opus` |
| Meta | `meta-llama/{model}` | `meta-llama/llama-2-70b` (需检查是否可用) |
| Mistral | `mistralai/{model}` | `mistralai/mistral-large` |
| Google | `google/{model}` | `google/gemini-pro` |
| Deepseek | `deepseek/{model}` | `deepseek/deepseek-reasoner` |

## 测试模型可用性

```bash
# 1. 使用默认模型（GPT-3.5）
python main.py --mode llm --provider openrouter --max-steps 10

# 2. 测试 Claude 3.5 Sonnet
export LLM_MODEL="anthropic/claude-3.5-sonnet"
python main.py --mode llm --provider openrouter --max-steps 10

# 3. 测试 GPT-4 Turbo
export LLM_MODEL="openai/gpt-4-turbo"
python main.py --mode llm --provider openrouter --max-steps 10
```

## 成本估算

| 模型 | 输入成本 | 输出成本 | Pick & Place 任务成本 |
|------|--------|--------|----------------------|
| GPT-3.5 Turbo | $0.50/M | $1.50/M | ~$0.01-0.05 |
| GPT-4 Turbo | $10/M | $30/M | ~$0.10-0.50 |
| Claude 3.5 Sonnet | $3/M | $15/M | ~$0.03-0.15 |
| Mistral Large | $2/M | $6/M | ~$0.02-0.10 |

*注：实际成本取决于对话长度和模型的推理步数*

## 性能对比

| 模型 | 推理速度 | 质量 | Pick & Place 成功率 |
|------|--------|------|-------------------|
| GPT-3.5 | 快 | 中等 | ~60-70% |
| Mistral Large | 中等 | 中等 | ~70-80% |
| GPT-4 Turbo | 中等 | 高 | ~85-95% |
| Claude 3.5 Sonnet | 中等 | 高 | ~85-95% |
| Claude 3 Opus | 慢 | 最高 | ~95%+ |

## 故障排查

### 1. "404 - No endpoints found for {model}"
**原因**: 模型在 OpenRouter 上不可用
**解决**: 
```bash
# 使用推荐的模型之一
export LLM_MODEL="openai/gpt-3.5-turbo"
```

### 2. "401 - Invalid API key"
**原因**: API Key 不正确或已过期
**解决**:
```bash
export OPENROUTER_API_KEY="your-new-key-here"
```

### 3. "429 - Too many requests"
**原因**: 限流（超配额）
**解决**: 等待几分钟后重试

### 4. 模型超时
**原因**: 模型响应慢或请求过大
**解决**: 使用更快的模型或减少 max-steps

## 完整命令参考

```bash
# 默认推荐（最平衡）
export OPENROUTER_API_KEY="your-key"
python main.py --mode llm --provider openrouter --max-steps 50

# 快速测试（GPT-3.5）
export LLM_MODEL="openai/gpt-3.5-turbo"
./run_openrouter.sh 20

# 高质量推理（Claude 3.5）
export LLM_MODEL="anthropic/claude-3.5-sonnet"
./run_openrouter.sh 50

# 最强模型（Claude 3 Opus）
export LLM_MODEL="anthropic/claude-3-opus"
./run_openrouter.sh 50
```

## OpenRouter 账户相关

- **网址**: https://openrouter.ai/
- **获取 API Key**: https://openrouter.ai/keys
- **查看费用**: https://openrouter.ai/account/billing/overview
- **查看模型列表**: https://openrouter.ai/models
- **文档**: https://openrouter.ai/docs

## 额外提示

1. **使用 HTTP-Referer 头**: 本脚本已自动添加，确保与 OpenRouter 的兼容性
2. **保存 API Key 安全**: 不要将 Key commit 到 Git，使用环境变量
3. **监视费用**: OpenRouter 提供实时费用追踪，定期检查避免超支
4. **模型轮换**: 可以编写脚本在多个模型间测试性能

---
*最后更新: 2026-04-29*
