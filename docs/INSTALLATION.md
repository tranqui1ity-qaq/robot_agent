# 📥 详细安装指南

支持 macOS、Linux、Windows 和 Docker。

## 前提条件

- Python 3.10 或更高版本
- 4GB+ 内存
- 网络连接（用于 API 调用）

---

## macOS 安装

### 步骤 1：安装 Python

```bash
# 使用 Homebrew
brew install python@3.10
python3.10 --version
```

### 步骤 2：克隆项目

```bash
git clone https://github.com/tranqui1ity-qaq/robot_agent.git
cd robot_agent
```

### 步骤 3：创建虚拟环境

```bash
python3.10 -m venv venv
source venv/bin/activate
```

### 步骤 4：安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 步骤 5：配置 API Key

```bash
export OPENROUTER_API_KEY="sk_your_key_here"
```

### 步骤 6：验证安装

```bash
python main.py --help
```

---

## Linux 安装（Ubuntu/Debian）

### 步骤 1：更新系统

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 步骤 2：安装系统依赖

```bash
sudo apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    git \
    libgl1-mesa-glx \
    libglib2.0-0
```

### 步骤 3：克隆项目

```bash
git clone https://github.com/tranqui1ity-qaq/robot_agent.git
cd robot_agent
```

### 步骤 4：创建虚拟环境

```bash
python3.10 -m venv venv
source venv/bin/activate
```

### 步骤 5：安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 步骤 6：配置 API Key

```bash
echo 'export OPENROUTER_API_KEY="sk_your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### 步骤 7：验证安装

```bash
python main.py --help
```

---

## Windows 安装

### 步骤 1：下载 Python

访问 [python.org](https://www.python.org) 下载 Python 3.10+

**安装时勾选：** "Add Python to PATH"

### 步骤 2：克隆项目

```powershell
git clone https://github.com/tranqui1ity-qaq/robot_agent.git
cd robot_agent
```

### 步骤 3：创建虚拟环境

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 步骤 4：安装依赖

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 步骤 5：配置 API Key（方法 A：临时）

```powershell
$env:OPENROUTER_API_KEY = "sk_your_key_here"
```

### 步骤 5b：配置 API Key（方法 B：永久）

1. 按 `Win + X` → 选择"系统"
2. 左侧点击"高级系统设置"
3. 点击"环境变量"
4. 新建变量：
   - 变量名：`OPENROUTER_API_KEY`
   - 变量值：`sk_your_key_here`
5. 点击确定

### 步骤 6：验证安装

```powershell
python main.py --help
```

---

## Docker 安装

### 步骤 1：创建 Dockerfile

在项目根目录创建 `Dockerfile`：

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制项目
COPY . /app

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV OPENROUTER_API_KEY=""

# 运行
CMD ["python", "main.py", "--mode", "llm", "--max-steps", "50"]
```

### 步骤 2：构建镜像

```bash
docker build -t robot-agent .
```

### 步骤 3：运行容器

```bash
# 方法 A：传入 API Key（推荐）
docker run -e OPENROUTER_API_KEY="sk_your_key" robot-agent

# 方法 B：交互模式
docker run -it -e OPENROUTER_API_KEY="sk_your_key" robot-agent bash

# 方法 C：保存视频
docker run \
  -e OPENROUTER_API_KEY="sk_your_key" \
  -v $(pwd)/videos:/app/videos \
  robot-agent
```

---

## Conda 安装

### 步骤 1：创建 Conda 环境

```bash
conda create -n robot-agent python=3.10
conda activate robot-agent
```

### 步骤 2：克隆项目

```bash
git clone https://github.com/tranqui1ity-qaq/robot_agent.git
cd robot_agent
```

### 步骤 3：安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 4：配置 API Key

```bash
export OPENROUTER_API_KEY="sk_your_key_here"
```

### 步骤 5：运行

```bash
python main.py --mode llm --max-steps 50
```

---

## 验证安装

### 快速测试

```bash
# 测试 Python
python --version         # 应该是 3.10+

# 测试依赖
python -c "import panda_gym; print('✓ panda_gym installed')"
python -c "import cv2; print('✓ opencv installed')"
python -c "import openai; print('✓ openai installed')"

# 测试演示模式（无需 API Key）
python main.py --mode demo --max-steps 10
```

### 测试 LLM 模式

```bash
export OPENROUTER_API_KEY="sk_your_key"
python main.py --mode llm --max-steps 5
```

---

## 常见安装问题

### 问题 1：Python 版本不支持

```
Error: Python 3.8 is not supported
```

**解决方案：**
```bash
# 安装 Python 3.10+
brew install python@3.10          # macOS
sudo apt install python3.10        # Linux
# 或访问 python.org 下载（Windows）

# 使用正确的 Python 版本
python3.10 -m venv venv
```

### 问题 2：pip 权限错误（Linux 用户）

```
ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied
```

**解决方案：**
```bash
# 不要使用 sudo pip，而是用虚拟环境
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 问题 3：OpenGL 错误（Linux）

```
RuntimeError: No OpenGL context found
```

**解决方案：**
```bash
# 安装 OpenGL 库
sudo apt-get install libgl1-mesa-glx libglib2.0-0

# 或禁用渲染
python main.py --render false
```

### 问题 4：依赖冲突

```
ERROR: pip's dependency resolver does not currently take into account
```

**解决方案：**
```bash
# 清理并重新安装
pip install --upgrade --force-reinstall -r requirements.txt
```

---

## 下一步

- 🚀 [快速开始](QUICK_START.md) — 运行您的第一个演示
- 📖 [项目讲解](PROJECT_GUIDE.md) — 深入理解项目
- 🎥 [视频录制](VIDEO_RECORDING_GUIDE.md) — 录制演示视频
