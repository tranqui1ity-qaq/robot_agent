# 🎥 录制机械臂演示视频

这个工具能将LLM驱动的机械臂操作过程录制为高质量MP4视频。

## 快速开始

### 使用 OpenRouter（推荐）

```bash
export OPENROUTER_API_KEY="你的API密钥"
bash record_video.sh
```

### 使用 OpenAI

```bash
export OPENAI_API_KEY="你的API密钥"
bash record_video.sh demo.mp4 50 20 openai
```

## 命令参数说明

```bash
bash record_video.sh [输出文件] [最大步数] [每步帧数] [供应商] [FPS]
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 输出文件 | `robot_demo.mp4` | MP4输出文件名 |
| 最大步数 | `50` | LLM决策的最大步数 |
| 每步帧数 | `20` | 每个工具执行后捕获的帧数（更多=更流畅） |
| 供应商 | `openrouter` | `openrouter` 或 `openai` |
| FPS | `60` | 视频帧率 |

## 使用示例

### 基础用法（所有参数采用默认值）
```bash
bash record_video.sh
```

### 自定义输出文件名
```bash
bash record_video.sh my_demo.mp4
```

### 高质量视频（更多帧，更高FPS）
```bash
bash record_video.sh demo.mp4 50 50 openrouter 60
```
**结果**: 约 $\frac{50 \times 50}{60} \approx 42$ 秒的视频

### 快速演示（少量帧）
```bash
bash record_video.sh quick.mp4 30 10 openrouter 30
```

### 使用不同的LLM模型
```bash
export LLM_MODEL="deepseek/deepseek-chat"
bash record_video.sh demo.mp4 50 20 openrouter
```

## 高级选项

### 直接使用Python脚本

```bash
# OpenRouter
python record_video.py \
    --output demo.mp4 \
    --max-steps 50 \
    --frames-per-step 20 \
    --provider openrouter \
    --fps 60

# OpenAI
python record_video.py \
    --output demo.mp4 \
    --max-steps 50 \
    --frames-per-step 20 \
    --provider openai \
    --fps 60
```

## 性能指南

**视频大小估算**：
$$\text{时长} = \frac{\text{总帧数}}{FPS} = \frac{\text{最大步数} \times \text{每步帧数}}{FPS}$$

### 推荐配置

| 场景 | 参数 | 时长 | 文件大小 |
|------|------|------|---------|
| 快速网络演示 | 30步, 10帧/步, 30 FPS | ~10秒 | ~5 MB |
| 标准演示 | 50步, 20帧/步, 60 FPS | ~17秒 | ~20 MB |
| 高质量 | 50步, 50帧/步, 60 FPS | ~42秒 | ~50 MB |
| 超高质量 | 50步, 50帧/步, 120 FPS | ~21秒 | ~100 MB |

## 视频自检清单

录制完成后，检查以下几点：

- ✅ 动作流畅（FPS足够高）
- ✅ 能清楚看到抓取和放置动作
- ✅ 没有帧跳跃或卡顿
- ✅ 颜色准确，无码率问题

## 常见问题

### Q: 录出来的视频太卡顿
**A**: 增加 `--frames-per-step` 或 `--fps`
```bash
bash record_video.sh demo.mp4 50 30 openrouter 60
```

### Q: 视频文件太大
**A**: 降低 `--frames-per-step` 或 `--fps`
```bash
bash record_video.sh demo.mp4 50 10 openrouter 30
```

### Q: API超时
**A**: 减少 `--max-steps`，或设置环境变量增加超时时间
```bash
bash record_video.sh demo.mp4 30 20 openrouter
```

### Q: 没有看到视频输出
**A**: 检查 `videos/` 目录是否存在
```bash
ls -lh videos/
```

## 环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `OPENROUTER_API_KEY` | OpenRouter API密钥 | `sk_live_...` |
| `OPENAI_API_KEY` | OpenAI API密钥 | `sk-...` |
| `LLM_MODEL` | 要使用的模型 | `mistralai/mistral-large` |

## 完整工作流

```bash
# 1. 设置API密钥
export OPENROUTER_API_KEY="sk_live_..."
export LLM_MODEL="mistralai/mistral-large"

# 2. 录制标准质量视频
bash record_video.sh demo_standard.mp4 50 20 openrouter 60

# 3. 查看生成的视频
ffplay videos/demo_standard.mp4
# 或
vlc videos/demo_standard.mp4
```

## 输出文件

所有生成的视频保存到 `videos/` 目录：
```
videos/
├── robot_demo.mp4
├── demo_standard.mp4
└── quick_demo.mp4
```

## 获取API密钥

- **OpenRouter**: https://openrouter.ai/ → 复制 API Key
- **OpenAI**: https://platform.openai.com/account/api-keys → 创建新的 Secret Key
