# AgentMem - 快速設置指南 / Quick Setup Guide

> **Choose your language:** [English](#english) | [繁體中文](#繁體中文)

---

## English

### ⚡ One-Command Installation

#### macOS / Linux

```bash
bash <(curl -s https://raw.githubusercontent.com/Hayatelin/agent-memory-mvp/main/setup.sh)
```

Or locally:

```bash
bash setup.sh
```

#### Windows

Double-click on `setup.bat` or run in Command Prompt:

```cmd
setup.bat
```

---

### 📋 What the Setup Script Does

The setup script automates:
1. ✅ Checks Python 3.8+ installation
2. ✅ Checks Git installation
3. ✅ Clones the repository
4. ✅ Installs all dependencies
5. ✅ Runs interactive initialization wizard
6. ✅ Displays next steps

---

### 🧙 Interactive Setup Wizard

The `init_wizard.py` will guide you through:

**Step 1: Language Selection**
- Choose English or 繁體中文

**Step 2: Environment Check**
- Verifies Python, pip, and Git versions
- Checks system compatibility

**Step 3: Database Selection**
- **SQLite** (Recommended for beginners)
  - No configuration needed
  - Perfect for learning
  - Data stored locally

- **PostgreSQL** (Production)
  - More powerful
  - Better for teams
  - Enter connection details

**Step 4: Agent Identity Setup**
- Set your Agent name
- Auto-generate unique Agent ID (UUID)
- Or use custom Agent ID

**Step 5: Startup Options**
- Enable Web UI Dashboard (Streamlit)
- Enable REST API Server
- Enable Command-line Interface

---

### 🚀 Starting AgentMem After Setup

#### **Terminal 1: Start Backend Server**
```bash
cd agent-memory-mvp
python -m src.main
```

Output will show:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

#### **Terminal 2: Start Web UI (Optional)**
```bash
cd agent-memory-mvp
streamlit run ui/app.py
```

Browser will open to: `http://localhost:8501`

#### **Access Points:**
- Web UI: http://localhost:8501
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

---

### 🎯 First-Time Usage Tips

#### Option 1: Web UI (Easiest)
1. Open http://localhost:8501
2. Click "Create Memory"
3. Enter your first memory
4. Try searching for it

#### Option 2: Python SDK
```python
from src.client import AgentMemClient

# Initialize client with your Agent ID from config
client = AgentMemClient(api_url="http://localhost:8000")

# Create a memory
memory = client.create_memory(
    content="My first AgentMem memory!",
    type="knowledge",
    category="getting-started"
)

# Search for it
results = client.search("first memory")
print(results)
```

#### Option 3: Command Line
```bash
# See all available commands
python -m src.cli.main --help

# Initialize CLI (one-time)
python -m src.cli.main init

# Create your first memory
python -m src.cli.main create "My first memory with AgentMem!"

# List all memories
python -m src.cli.main list

# Search
python -m src.cli.main search "memory"
```

---

### 🛠️ Configuration Files

After setup, you'll have:

**~/.agentmem/config.json**
```json
{
  "agent_name": "Your-Agent-Name",
  "agent_id": "uuid-here",
  "api_url": "http://localhost:8000",
  "database": {
    "type": "sqlite",
    "url": "sqlite:///./agentmem.db"
  }
}
```

**.env** (in project directory)
```
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite:///./agentmem.db
API_HOST=0.0.0.0
API_PORT=8000
EMBEDDING_SERVICE=local
DEBUG=false
```

---

### 📚 Next Steps

- 📖 [Quick Start Guide](docs/QUICKSTART.md) - 5-minute introduction
- 💡 [Usage Guide](docs/USAGE_GUIDE.md) - Detailed instructions
- 💻 [Code Examples](docs/EXAMPLES.md) - 10 practical examples
- 🔌 [API Reference](docs/API_REFERENCE.md) - Complete API documentation
- 🛠️ [Troubleshooting](docs/TROUBLESHOOTING.md) - Solutions to common issues

---

### ❓ Troubleshooting

#### "Command not found: python3"
- Install Python 3.8+ from https://www.python.org/downloads/

#### "pip: command not found"
- Run: `python -m pip install --upgrade pip`

#### "Permission denied: setup.sh"
- Run: `chmod +x setup.sh && ./setup.sh`

#### "Port 8000 already in use"
- Change port in `.env`: `API_PORT=8001`
- Run: `python -m src.main`

#### "ModuleNotFoundError"
- Ensure you're in the project directory
- Reinstall: `pip install -r requirements.txt`

---

### 📞 Need Help?

- 🐛 Report bugs: https://github.com/Hayatelin/agent-memory-mvp/issues
- 💬 Discussions: https://github.com/Hayatelin/agent-memory-mvp/discussions
- 📖 Full documentation: https://github.com/Hayatelin/agent-memory-mvp#readme

---

## 繁體中文

### ⚡ 一鍵安裝

#### macOS / Linux

```bash
bash <(curl -s https://raw.githubusercontent.com/Hayatelin/agent-memory-mvp/main/setup.sh)
```

或本地執行：

```bash
bash setup.sh
```

#### Windows

雙擊 `setup.bat` 或在命令提示符中執行：

```cmd
setup.bat
```

---

### 📋 設置腳本做了什麼

設置腳本自動化以下步驟：
1. ✅ 檢查 Python 3.8+ 安裝
2. ✅ 檢查 Git 安裝
3. ✅ 複製倉庫
4. ✅ 安裝所有依賴項
5. ✅ 運行交互式初始化向導
6. ✅ 顯示後續步驟

---

### 🧙 交互式設置嚮導

`init_wizard.py` 將引導你完成：

**步驟 1：選擇語言**
- 選擇英文或繁體中文

**步驟 2：環境檢查**
- 驗證 Python、pip 和 Git 版本
- 檢查系統兼容性

**步驟 3：數據庫選擇**
- **SQLite**（推薦初學者）
  - 無需配置
  - 完美用於學習
  - 數據本地存儲

- **PostgreSQL**（生產環境）
  - 更強大
  - 適合團隊
  - 輸入連接詳情

**步驟 4：Agent 身份設置**
- 設置 Agent 名稱
- 自動生成唯一的 Agent ID (UUID)
- 或使用自定義 Agent ID

**步驟 5：啟動選項**
- 啟用 Web UI 儀表板 (Streamlit)
- 啟用 REST API 服務器
- 啟用命令行界面

---

### 🚀 設置後啟動 AgentMem

#### **終端 1：啟動後端服務器**
```bash
cd agent-memory-mvp
python -m src.main
```

輸出將顯示：
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

#### **終端 2：啟動 Web UI（可選）**
```bash
cd agent-memory-mvp
streamlit run ui/app.py
```

瀏覽器將打開：`http://localhost:8501`

#### **訪問地址：**
- Web UI: http://localhost:8501
- API: http://localhost:8000
- API 文檔: http://localhost:8000/docs

---

### 🎯 首次使用小貼士

#### 方式 1：Web UI（最簡單）
1. 打開 http://localhost:8501
2. 點擊"創建記憶"
3. 輸入你的第一個記憶
4. 嘗試搜索它

#### 方式 2：Python SDK
```python
from src.client import AgentMemClient

# 使用配置中的 Agent ID 初始化客戶端
client = AgentMemClient(api_url="http://localhost:8000")

# 創建記憶
memory = client.create_memory(
    content="我的第一個 AgentMem 記憶！",
    type="knowledge",
    category="getting-started"
)

# 搜索它
results = client.search("第一個")
print(results)
```

#### 方式 3：命令行
```bash
# 查看所有可用命令
python -m src.cli.main --help

# 初始化 CLI（一次性）
python -m src.cli.main init

# 創建你的第一個記憶
python -m src.cli.main create "我用 AgentMem 創建的第一個記憶！"

# 列出所有記憶
python -m src.cli.main list

# 搜索
python -m src.cli.main search "記憶"
```

---

### 🛠️ 配置文件

設置後，你將擁有：

**~/.agentmem/config.json**
```json
{
  "agent_name": "你的-Agent-名稱",
  "agent_id": "uuid-在此",
  "api_url": "http://localhost:8000",
  "database": {
    "type": "sqlite",
    "url": "sqlite:///./agentmem.db"
  }
}
```

**.env**（在項目目錄中）
```
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite:///./agentmem.db
API_HOST=0.0.0.0
API_PORT=8000
EMBEDDING_SERVICE=local
DEBUG=false
```

---

### 📚 後續步驟

- 📖 [快速開始指南](docs/QUICKSTART.zh-TW.md) - 5 分鐘介紹
- 💡 [使用指南](docs/USAGE_GUIDE.zh-TW.md) - 詳細說明
- 💻 [代碼示例](docs/EXAMPLES.zh-TW.md) - 10 個實用例子
- 🔌 [API 參考](docs/API_REFERENCE.zh-TW.md) - 完整 API 文檔
- 🛠️ [故障排除](docs/TROUBLESHOOTING.zh-TW.md) - 常見問題解決方案

---

### ❓ 故障排除

#### "找不到命令: python3"
- 從 https://www.python.org/downloads/ 安裝 Python 3.8+

#### "找不到 pip"
- 運行：`python -m pip install --upgrade pip`

#### "權限被拒絕: setup.sh"
- 運行：`chmod +x setup.sh && ./setup.sh`

#### "端口 8000 已被使用"
- 在 `.env` 中更改端口：`API_PORT=8001`
- 運行：`python -m src.main`

#### "ModuleNotFoundError"
- 確保你在項目目錄中
- 重新安裝：`pip install -r requirements.txt`

---

### 📞 需要幫助？

- 🐛 報告錯誤：https://github.com/Hayatelin/agent-memory-mvp/issues
- 💬 討論：https://github.com/Hayatelin/agent-memory-mvp/discussions
- 📖 完整文檔：https://github.com/Hayatelin/agent-memory-mvp#readme

---

**Last Updated:** 2026-02-17
**Version:** 0.3.0
**Status:** ✅ Production Ready
