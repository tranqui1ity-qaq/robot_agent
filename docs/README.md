# 📚 补充文档

本目录包含项目的深度文档和参考资料。

## 📖 文档导航

### 🚀 [快速参考](QUICK_REFERENCE.md)
快速命令速查表和常见问题解答
- ⚡ 必要命令集合
- 🐛 故障排查 Top 10
- 💡 常用技巧

**推荐首先阅读**

---

### 🏗️ [项目架构指南](PROJECT_GUIDE.md)
完整的项目设计、实现和工作原理讲解
- 📐 系统架构设计
- 🔄 闭环控制流程
- 🛠️ 核心模块详解
- 🧠 LLM 集成原理

**深入理解项目时阅读**

---

### 🔧 [架构重构总结](REFACTOR_SUMMARY.md)
项目从演示模式到 LLM 驱动的重构过程
- 🔀 设计模式的演变
- 📝 重构前后对比
- ✨ 新特性说明
- 🎯 优化改进

**了解项目演进历史时阅读**

---

### 🤖 [LLM 模型参考](OPENROUTER_MODELS.md)
支持的大语言模型列表和对比
- 📊 模型性能对比
- 💰 价格和成本
- ⚡ 速度和精度
- 📈 推荐使用模型

**选择 LLM 模型时参考**

---

## 🎯 快速导航

| 我想... | 查看文档 |
|--------|--------|
| 快速上手 | [README.md](../README.md) |
| 查询命令 | [快速参考](QUICK_REFERENCE.md) |
| 深入理解 | [项目指南](PROJECT_GUIDE.md) |
| 了解历史 | [架构总结](REFACTOR_SUMMARY.md) |
| 选择模型 | [模型参考](OPENROUTER_MODELS.md) |

---

## 📂 项目结构

```
robot_agent/
├── README.md                    # ⭐ 主文档（从这里开始）
├── requirements.txt             # 依赖列表
├── LICENSE                      # 开源协议
│
├── 核心代码
├── env_wrapper.py              # 低层机械臂控制
├── skills.py                   # LLM 工具函数
├── main.py                     # 主循环
│
├── 工具脚本
├── run_openrouter.sh           # 一键启动脚本
├── diagnose_openrouter.py      # 模型诊断工具
│
└── 📚 docs/                    # 补充文档（本目录）
    ├── README.md               # 本文件
    ├── QUICK_REFERENCE.md      # 快速参考卡片
    ├── PROJECT_GUIDE.md        # 完整项目指南
    ├── REFACTOR_SUMMARY.md     # 架构重构说明
    └── OPENROUTER_MODELS.md    # LLM 模型列表
```

---

## 🌟 阅读建议

### 刚开始使用？
1. 📖 [主 README](../README.md) — 5 分钟了解项目和快速开始
2. ⚡ [快速参考](QUICK_REFERENCE.md) — 10 分钟学会常用命令

### 想深入理解？
1. 🏗️ [项目指南](PROJECT_GUIDE.md) — 30 分钟深入学习架构
2. 🔧 [架构总结](REFACTOR_SUMMARY.md) — 15 分钟了解演进历史

### 需要选择 LLM？
1. 🤖 [模型参考](OPENROUTER_MODELS.md) — 5 分钟选择合适的模型

---

## ⏱️ 总阅读时间指南

| 级别 | 文档 | 时间 |
|------|------|------|
| 初级 | README + 快速参考 | 15 分钟 |
| 中级 | 加上项目指南 | 45 分钟 |
| 高级 | 全部文档 | 60 分钟 |

---

## 💾 离线使用

所有文档都是 Markdown 格式，可以：
- 使用任意 Markdown 查看器打开
- 导出为 PDF 或其他格式
- 在 GitHub 上直接查看（自动渲染）
- 使用 `cat` 命令在终端查看（Linux/macOS）

```bash
# 在终端查看
cat QUICK_REFERENCE.md
cat PROJECT_GUIDE.md
```

---

## 🔗 相关资源

- **GitHub 仓库**: [tranqui1ity-qaq/robot_agent](https://github.com/tranqui1ity-qaq/robot_agent)
- **OpenRouter API**: [https://openrouter.ai](https://openrouter.ai)
- **Panda Gym**: [https://github.com/alexis-duong/panda-gym](https://github.com/alexis-duong/panda-gym)

---

## 📝 文档维护

最后更新：2026 年 4 月 29 日

需要更新或有建议？提交 [Issue](https://github.com/tranqui1ity-qaq/robot_agent/issues)
