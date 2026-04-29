# 📚 文档导航索引

欢迎来到 **Panda Pick & Place LLM 闭环控制系统** 的完整文档中心！  
👇 选择下面的链接快速找到你需要的信息

---

## 🚀 我想立即开始

### ⚡ 5分钟快速启动
1. 📖 [快速参考卡片](QUICK_REFERENCE.md) - 30秒快速开始
2. 🔧 运行命令：`./run_openrouter.sh 50`
3. ✅ 观察机械臂工作

**所需时间**: 5分钟  
**需要 API Key**: ✅ 是  
**适合**: 想立即看到效果的用户

---

## 📖 我想全面了解项目

### 📘 完整项目指南
👉 **[PROJECT_GUIDE.md](PROJECT_GUIDE.md)** - 8000+ 字完整教程

涵盖内容：
- 项目概述和创新点
- 系统架构和分层设计
- 完整的工作原理讲解
- API 集成细节
- 故障排查和最佳实践
- 扩展应用指导

**所需时间**: 30-40分钟  
**适合**: 想深入理解项目的开发者

### 📋 项目完成清单
👉 **[COMPLETION_CHECKLIST.md](COMPLETION_CHECKLIST.md)** - 项目全景图

涵盖内容：
- 项目结构和文件说明
- 安装和运行清单
- 功能完整性检查
- 测试结果统计
- 性能数据和已知限制
- 未来改进方向

**所需时间**: 10-15分钟  
**适合**: 想了解项目整体状况的人

---

## 🔗 我想快速查阅

### 📌 快速参考卡片
👉 **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - 速查手册

快速答案：
- Common commands（常用命令）
- Architecture diagram（架构图）
- Workspace bounds（工作空间）
- Tool functions（工具函数）
- Troubleshooting（故障排查）

**查阅时间**: 2-5分钟  
**适合**: 需要快速答案的用户

---

## 🎯 我有具体问题

### ❓ 常见问题类型

#### **"我想运行项目"**
1. 📖 阅读 [README_USAGE.md](README_USAGE.md)
2. ⚙️ 设置环境变量
3. 🚀 运行 `./run_openrouter.sh 50`

#### **"我想选择 LLM 模型"**
1. 🔍 运行 `python diagnose_openrouter.py` 查看可用模型
2. 📚 参考 [OPENROUTER_MODELS.md](OPENROUTER_MODELS.md) 选择模型
3. 🔧 `export LLM_MODEL="deepseek/deepseek-chat"` 并运行

#### **"我想改进 LLM 推理"**
1. 📖 阅读《项目指南》的 [API 集成](PROJECT_GUIDE.md#api-集成) 章节
2. 修改 `main.py` 中的 `system_prompt`
3. 测试效果

#### **"我想添加新工具"**
1. 📖 阅读《项目指南》的 [扩展应用](PROJECT_GUIDE.md#扩展应用) 章节
2. 在 `skills.py` 中添加新函数
3. 在 `main.py` 的 `_build_tools()` 中注册

#### **"项目出错了"**
1. 📖 阅读《项目指南》的 [故障排查](PROJECT_GUIDE.md#故障排查) 章节
2. 运行 `python diagnose_openrouter.py` 诊断问题
3. 查看《快速参考》的 [故障排查](QUICK_REFERENCE.md#-常见故障排查) 表格

#### **"我想了解架构"**
1. 📖 阅读《完成清单》的 [项目结构](COMPLETION_CHECKLIST.md#项目结构) 部分
2. 深入阅读《重构总结》的 [架构说明](REFACTOR_SUMMARY.md)
3. 查看《项目指南》的 [系统架构](PROJECT_GUIDE.md#系统架构) 章节

---

## 📚 文档完整列表

### 核心文档（必读）

| 文档 | 长度 | 阅读时间 | 重要性 | 推荐指数 |
|------|------|--------|--------|----------|
| **PROJECT_GUIDE.md** | 📖 长 | 30-40分 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **QUICK_REFERENCE.md** | 🔗 中等 | 5-10分 | ⭐⭐ | ⭐⭐⭐⭐ |
| **COMPLETION_CHECKLIST.md** | 📋 中等 | 10-15分 | ⭐⭐⭐ | ⭐⭐⭐⭐ |

### 参考文档（备查）

| 文档 | 内容 | 人群 |
|------|------|------|
| **README_USAGE.md** | 基础使用指南 | 初学者 |
| **REFACTOR_SUMMARY.md** | 架构细节和代码重构 | 开发者 |
| **OPENROUTER_MODELS.md** | LLM 模型列表和对比 | 提示工程师 |
| **CLAUDE.md** | 初始项目要求文档 | 项目经理 |

---

## 🎓 按学习阶段

### 🟢 初级（刚开始）
**目标**: 让项目跑起来

**阅读顺序**:
1. ⚡ [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 时间：5分钟
2. 🚀 `./run_openrouter.sh 10` - 时间：5-10分钟
3. 📖 [README_USAGE.md](README_USAGE.md) - 时间：10分钟

**总投入**: 20-30分钟

**成果**:
✅ 项目成功运行  
✅ 理解基本操作  
✅ 看到机械臂工作

---

### 🟡 中级（深入理解）
**目标**: 理解整个系统

**阅读顺序**:
1. 📘 [PROJECT_GUIDE.md](PROJECT_GUIDE.md) - 时间：30分钟
2. 读懂源码理解细节 - 时间：30分钟
3. 🔧 尝试修改 `system_prompt` - 时间：15分钟

**总投入**: 1.5小时

**成果**:
✅ 理解架构设计  
✅ 掌握工作原理  
✅ 能改进 Prompt  

---

### 🔴 高级（扩展定制）
**目标**: 自定义和扩展

**阅读顺序**:
1. 📕 [REFACTOR_SUMMARY.md](REFACTOR_SUMMARY.md) - 时间：20分钟
2. 📖 [PROJECT_GUIDE.md](PROJECT_GUIDE.md#扩展应用) 中的扩展章节 - 时间：20分钟
3. 💻 实现自己的功能 - 时间：1-2小时

**总投入**: 2-3小时

**成果**:
✅ 添加新工具  
✅ 支持多任务  
✅ 自定义控制  

---

## 🛠️ 按工作任务

### 📋 任务 1: "激活项目"
**需要做的**:
- [ ] 获取 OPENROUTER_API_KEY
- [ ] 设置环境变量
- [ ] 运行诊断工具
- [ ] 成功运行一次

**相关文档**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)  
**预计时间**: 10分钟

---

### 📋 任务 2: "选择最佳模型"
**需要做的**:
- [ ] 运行诊断脚本
- [ ] 查看可用模型列表
- [ ] 参考模型对比表
- [ ] 测试 2-3 个模型

**相关文档**: [OPENROUTER_MODELS.md](OPENROUTER_MODELS.md)  
**预计时间**: 20分钟

---

### 📋 任务 3: "改进 LLM 推理"
**需要做的**:
- [ ] 理解 system_prompt 的作用
- [ ] 阅读项目指南中的 API 集成章节
- [ ] 修改 Prompt 中的约束
- [ ] 测试效果

**相关文档**: [PROJECT_GUIDE.md#api-集成](PROJECT_GUIDE.md#api-集成)  
**预计时间**: 30分钟

---

### 📋 任务 4: "添加新工具函数"
**需要做的**:
- [ ] 了解工具定义结构
- [ ] 在 skills.py 中编写函数
- [ ] 在 main.py 中注册工具
- [ ] 测试新工具

**相关文档**: [PROJECT_GUIDE.md#扩展应用](PROJECT_GUIDE.md#扩展应用)  
**预计时间**: 1小时

---

### 📋 任务 5: "故障排查"
**需要做的**:
- [ ] 运行诊断工具
- [ ] 查看错误日志
- [ ] 参考故障排查指南
- [ ] 尝试解决方案

**相关文档**: [PROJECT_GUIDE.md#故障排查](PROJECT_GUIDE.md#故障排查)  
**预计时间**: 15-30分钟

---

## 🎯 场景导航

### 场景 A：学生/研究者
**目标**: 理解 LLM 在机器人中的应用

**读这些**:
1. [PROJECT_GUIDE.md](PROJECT_GUIDE.md) - 完整理论
2. [REFACTOR_SUMMARY.md](REFACTOR_SUMMARY.md) - 架构深度
3. 对比 demo 和 llm 模式学习

**投入时间**: 2小时

---

### 场景 B：工程师
**目标**: 把这套系统用于生产

**读这些**:
1. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 快速上手
2. [PROJECT_GUIDE.md#api-集成](PROJECT_GUIDE.md#api-集成) - API 细节
3. [PROJECT_GUIDE.md#故障排查](PROJECT_GUIDE.md#故障排查) - 生产注意

**投入时间**: 1.5小时

---

### 场景 C：AI/ML 工程师
**目标**: 改进和优化 LLM 性能

**读这些**:
1. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 快速了解
2. [OPENROUTER_MODELS.md](OPENROUTER_MODELS.md) - 模型选择
3. [PROJECT_GUIDE.md#工作原理](PROJECT_GUIDE.md#工作原理) - 决策流程
4. 修改 system_prompt 做 prompt engineering

**投入时间**: 2小时

---

## 🔍 按功能快速导航

### 我想了解...

#### **工作原理**
📖 [PROJECT_GUIDE.md#工作原理](PROJECT_GUIDE.md#工作原理)  
🔗 [QUICK_REFERENCE.md#-执行流程](QUICK_REFERENCE.md#-执行流程)

#### **架构设计**
📖 [PROJECT_GUIDE.md#系统架构](PROJECT_GUIDE.md#系统架构)  
📕 [REFACTOR_SUMMARY.md](REFACTOR_SUMMARY.md)

#### **运行方式**
🔗 [QUICK_REFERENCE.md#-快速开始](QUICK_REFERENCE.md#-快速开始)  
📘 [README_USAGE.md](README_USAGE.md)

#### **LLM 集成**
📖 [PROJECT_GUIDE.md#api-集成](PROJECT_GUIDE.md#api-集成)  
📙 [OPENROUTER_MODELS.md](OPENROUTER_MODELS.md)

#### **故障排查**
📖 [PROJECT_GUIDE.md#故障排查](PROJECT_GUIDE.md#故障排查)  
🔗 [QUICK_REFERENCE.md#-常见故障排查](QUICK_REFERENCE.md#-常见故障排查)

#### **代码扩展**
📖 [PROJECT_GUIDE.md#扩展应用](PROJECT_GUIDE.md#扩展应用)  
📕 [REFACTOR_SUMMARY.md#扩展建议](REFACTOR_SUMMARY.md#扩展建议)

#### **性能指标**
📋 [COMPLETION_CHECKLIST.md#性能数据](COMPLETION_CHECKLIST.md#性能数据)  
📖 [PROJECT_GUIDE.md#性能指标](PROJECT_GUIDE.md#性能指标)

---

## 💡 文档使用技巧

### 💻 快速搜索
在各个 Markdown 文件中使用 Ctrl+F：
- 找命令？搜 `bash`
- 找错误？搜 `Error` 或 `❌`
- 找代码？搜 `def ` 或 ` ```

### 📌 收藏重要页面
1. [PROJECT_GUIDE.md](PROJECT_GUIDE.md) - 日常参考
2. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 快速查阅
3. [OPENROUTER_MODELS.md](OPENROUTER_MODELS.md) - 模型选择

### 🔖 创建书签
在浏览器中书签常用的：
- 快速参考卡片
- 故障排查章节
- API 集成细节

---

## ✅ 文档完整性

| 方面 | 覆盖度 | 质量 |
|------|--------|------|
| 快速启动 | ✅ 100% | ⭐⭐⭐⭐⭐ |
| 功能说明 | ✅ 100% | ⭐⭐⭐⭐⭐ |
| 架构深度 | ✅ 100% | ⭐⭐⭐⭐⭐ |
| API 细节 | ✅ 95% | ⭐⭐⭐⭐ |
| 故障排查 | ✅ 95% | ⭐⭐⭐⭐ |
| 扩展指南 | ✅ 90% | ⭐⭐⭐⭐ |
| 示例代码 | ✅ 85% | ⭐⭐⭐⭐ |

---

## 🚀 现在就开始！

### 选择你的路线：

**⏱️ 5分钟快速上手** → [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

**📚 30分钟全面了解** → [PROJECT_GUIDE.md](PROJECT_GUIDE.md)

**📋 全景项目概览** → [COMPLETION_CHECKLIST.md](COMPLETION_CHECKLIST.md)

**🔧 立即运行** → `./run_openrouter.sh 50`

---

## 📞 需要帮助？

1. **快速问题** → 查阅 [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. **深入理解** → 阅读 [PROJECT_GUIDE.md](PROJECT_GUIDE.md)
3. **诊断问题** → 运行 `python diagnose_openrouter.py`
4. **查找文件** → 回到本文档找相关链接

---

**🎉 开始你的 LLM 机械臂之旅！**

*最后更新：2026-04-29*
