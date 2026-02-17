> **語言**: [English](README.md) | [繁體中文](README.zh-TW.md)

# AgentMem - Agent Memory System

一個為 AI Agent 設計的高效記憶管理系統，支持向量嵌入、語義搜索、協作共享和用戶友善的 Web UI 儀表板。

## 版本

**0.4.0** - 增強易用性，提供一鍵安裝和交互式設置
**最新發佈版**：v0.3.0（生產就緒）

## 特性

### ✨ 核心功能
- **記憶管理**：創建、更新、刪除、查詢記憶
- **向量嵌入**：自動生成文本嵌入（支持本地和 OpenAI API）
- **語義搜索**：基於向量相似度的智能搜索
- **協作共享**：在 Agent 之間安全地共享記憶
- **細粒度權限**：讀、寫、共享三級權限控制
- **高性能搜索**：100 個記憶 <200ms，1000 個記憶 <500ms

### 🖥️ 用戶界面
- **Web UI 儀表板**：專業的 Streamlit Web 界面，面向非技術用戶
  - 視覺化的創建、搜索、管理和共享記憶
  - 實時統計和性能指標
  - 響應式和直觀的設計
- **Python SDK**：面向開發者的簡潔 API
  - 面向對象的接口
  - 完善的錯誤處理
  - 完整的功能支持
- **命令行界面 (CLI)**：面向進階用戶的終端工具
  - 配置管理
  - 批量操作
  - 豐富的格式化輸出

### 📚 完整文檔
- **5 分鐘快速開始指南**（英文 + 繁體中文）
- **詳細使用指南**（英文 + 繁體中文）
- **10 個代碼示例**（英文 + 繁體中文）
- **完整 API 參考**（英文 + 繁體中文）
- **故障排除指南**（英文 + 繁體中文）
- 所有文檔都配有語言切換器

### 🔒 安全特性
- Bearer Token 認證
- 權限驗證系統
- 訪問控制列表（ACL）
- 記憶可見性級別（private/shared/public）

## 快速開始

### 前置要求
- Python 3.8+
- PostgreSQL（開發環境可使用 SQLite）
- 4GB+ RAM（用於模型加載）

### 安裝和運行

#### ⚡ 快速安裝（推薦）

**macOS / Linux：**
```bash
bash <(curl -s https://raw.githubusercontent.com/Hayatelin/agent-memory-mvp/main/setup.sh)
```

**Windows：**
- 雙擊 `setup.bat` 或下載後運行

這將自動執行：
- 檢查系統要求
- 克隆倉庫
- 安裝依賴
- 啟動交互式設置嚮導

#### 手動安裝

1. **克隆項目**
   ```bash
   git clone https://github.com/Hayatelin/agent-memory-mvp.git
   cd agent-memory-mvp
   ```

2. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

3. **運行設置嚮導（可選）**
   ```bash
   python init_wizard.py
   ```

4. **啟動後端服務器**
   ```bash
   python -m src.main
   ```
   - 服務器運行在：http://localhost:8000
   - 健康檢查：http://localhost:8000/health

### 選擇您的界面

#### 🌐 Web UI（推薦新手）
```bash
streamlit run ui/app.py
```
- 訪問地址：http://localhost:8501
- 直觀的視覺化界面
- 非常適合非技術用戶

#### 🐍 Python SDK（面向開發者）
```python
from src.client import AgentMemClient

client = AgentMemClient(
    api_url="http://localhost:8000",
    agent_id="your-agent-id"
)

memory = client.create_memory(
    content="您的記憶內容",
    type="knowledge",
    category="ai"
)

results = client.search("搜索查詢")
```

#### 💻 命令行界面（面向進階用戶）
```bash
# 初始化 CLI
python -m src.cli.main init

# 創建記憶
python -m src.cli.main create "您的記憶內容"

# 搜索
python -m src.cli.main search "查詢"

# 查看統計
python -m src.cli.main stats
```

### 文檔
- 🚀 [5 分鐘快速開始](docs/QUICKSTART.zh-TW.md)
- 📖 [詳細使用指南](docs/USAGE_GUIDE.zh-TW.md)
- 💻 [代碼示例](docs/EXAMPLES.zh-TW.md)
- 🔌 [API 參考](docs/API_REFERENCE.zh-TW.md)
- 🛠️ [故障排除](docs/TROUBLESHOOTING.zh-TW.md)

## API 端點

### 記憶 API
| 方法 | 路由 | 描述 |
|------|------|------|
| POST | /memories | 創建記憶 |
| GET | /memories | 列出記憶 |
| GET | /memories/{id} | 獲取記憶 |
| PUT | /memories/{id} | 更新記憶 |
| DELETE | /memories/{id} | 刪除記憶 |

### 搜索 API
| 方法 | 路由 | 描述 |
|------|------|------|
| POST | /memories/search | 語義搜索 |
| GET | /memories/search/stats | 搜索統計 |

### 共享 API
| 方法 | 路由 | 描述 |
|------|------|------|
| POST | /memories/{id}/share | 共享記憶 |
| GET | /memories/{id}/shared-with | 查詢共享 |
| DELETE | /memories/{id}/share/{agent_id} | 撤銷共享 |

## 示例用法

### 認證
```bash
# 使用 Bearer Token 認證
Authorization: Bearer <agent-uuid>
```

### 創建記憶
```bash
curl -X POST http://localhost:8000/memories \
  -H "Authorization: Bearer <agent-uuid>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "knowledge",
    "category": "ai",
    "content": "機器學習是人工智能的重要分支",
    "visibility": "private"
  }'
```

### 搜索記憶
```bash
curl -X POST http://localhost:8000/memories/search \
  -H "Authorization: Bearer <agent-uuid>" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "人工智能",
    "limit": 10,
    "similarity_threshold": 0.3
  }'
```

## 項目結構

```
agent-memory-mvp/
├── src/
│   ├── api/                 # REST API 路由
│   │   ├── memories.py      # 記憶 CRUD API
│   │   ├── search.py        # 搜索 API
│   │   └── sharing.py       # 共享 API
│   ├── client/              # Python SDK
│   │   ├── client.py        # 主客戶端類
│   │   ├── models.py        # 數據模型
│   │   └── exceptions.py    # 異常處理
│   ├── cli/                 # 命令行界面
│   │   ├── main.py          # CLI 入口點
│   │   ├── commands.py      # CLI 命令
│   │   ├── config.py        # 配置管理
│   │   └── formatter.py     # 輸出格式化
│   ├── services/            # 業務服務
│   │   ├── embedding_service.py
│   │   └── search_service.py
│   ├── core/                # 核心邏輯
│   │   └── permissions.py
│   ├── models/              # 數據模型
│   │   └── models.py
│   ├── db/                  # 數據庫
│   │   └── database.py
│   ├── utils/               # 工具函數
│   │   ├── auth.py
│   │   └── embedding.py
│   └── main.py              # FastAPI 應用
├── ui/                      # Web UI 儀表板 (Streamlit)
│   ├── app.py               # 主 Streamlit 應用
│   └── features/            # UI 特性模塊
│       ├── create.py        # 創建記憶頁面
│       ├── search.py        # 搜索記憶頁面
│       ├── manage.py        # 管理記憶頁面
│       └── share.py         # 共享記憶頁面
├── docs/                    # 文檔（雙語）
│   ├── QUICKSTART.md        # 5 分鐘快速開始
│   ├── USAGE_GUIDE.md       # 詳細使用指南
│   ├── EXAMPLES.md          # 代碼示例
│   ├── API_REFERENCE.md     # API 文檔
│   └── TROUBLESHOOTING.md   # 故障排除
├── examples/                # 示例腳本
│   └── quick_start.py       # 快速開始示例
├── tests/                   # 測試
│   ├── test_embeddings.py
│   ├── test_search.py
│   ├── test_permissions.py
│   ├── test_integration.py
│   └── test_performance.py
├── requirements.txt         # Python 依賴項
├── Makefile                 # 構建自動化
└── README.md                # 項目 README
```

## 測試

### 運行所有測試
```bash
pytest tests/ -v
```

### 運行特定測試
```bash
pytest tests/test_embeddings.py -v
pytest tests/test_search.py -v
pytest tests/test_permissions.py -v
pytest tests/test_integration.py -v
pytest tests/test_performance.py -v
```

### 生成覆蓋率報告
```bash
pytest --cov=src tests/
```

## 性能基準

使用 all-MiniLM-L6-v2 模型測試：

| 操作 | 規模 | 時間 |
|------|------|------|
| 嵌入生成 | 100 文本 | ~1s |
| 搜索 | 100 記憶 | <200ms |
| 搜索 | 1000 記憶 | <500ms |
| 相似度計算 | 1000 向量 | <100ms |

## 環境變量

```bash
# 數據庫配置
DATABASE_URL=sqlite:///./test.db  # 開發環境
DATABASE_URL=postgresql://user:password@localhost/agentmem  # 生產環境

# Redis（可選）
REDIS_URL=redis://localhost:6379

# OpenAI API（可選）
OPENAI_API_KEY=sk-...
```

## 開發指南

### 添加新的 API 端點
1. 在 `src/api/` 中創建新的路由模塊
2. 在 `src/main.py` 中包含路由
3. 在 `tests/` 中添加測試

### 添加新的服務
1. 在 `src/services/` 中實現服務類
2. 添加相應的測試
3. 在 API 中使用該服務

### 更新數據模型
1. 修改 `src/models/models.py`
2. 創建和運行數據庫遷移
3. 更新相關的測試

## 故障排除

### 模型下載失敗
```bash
# 手動下載模型
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### 數據庫連接錯誤
```bash
# 檢查 Docker 狀態
docker-compose ps

# 重啟服務
make docker-restart
```

### 認證失敗
確保在請求頭中包含有效的 Bearer Token：
```bash
Authorization: Bearer <valid-uuid>
```

## 貢獻

歡迎提交 Pull Request 和 Issue。

## 許可證

MIT License

## 聯系方式

- 項目主頁：https://github.com/...
- 文檔：http://localhost:8000/docs

## 版本歷史

### v0.4.0（開發中）- 增強易用性
**發佈日期**：2026 年 2 月 17 日

✨ **新功能：**
- 🚀 一鍵安裝腳本（macOS/Linux 的 setup.sh）
- 🪟 一鍵安裝腳本（Windows 的 setup.bat）
- 🧙 交互式設置嚮導（init_wizard.py），5 步配置流程
- 📋 快速設置指南（QUICK_SETUP.md），雙語支持
- ✅ 自動環境檢查和驗證
- 🎯 自動配置文件生成
- 📊 支持 SQLite 和 PostgreSQL 數據庫選擇

🎯 **改進：**
- 大幅減少設置時間（從 15-30 分鐘到 3-5 分鐘）
- 無需技術知識即可安裝
- 自動依賴安裝和驗證
- 清晰的錯誤消息和恢復選項
- 跨平台支持（Windows、macOS、Linux）
- 多語言設置嚮導（English + 繁體中文）

**關鍵文件：**
- setup.sh - Unix 系統的 Bash 腳本
- setup.bat - Windows 的批處理腳本
- init_wizard.py - 交互式 Python 配置嚮導
- QUICK_SETUP.md - 完整雙語設置指南

---

### v0.3.0（當前發佈版）- 完整實現
**發佈日期**：2026 年 2 月 17 日

✨ **新功能：**
- 🖥️ 專業 Web UI 儀表板（Streamlit），5 個特性頁面
- 🐍 完整的 Python SDK，包含 11 個核心方法
- 💻 命令行界面 (CLI)，包含 11 個命令
- 📚 完整的雙語文檔（英文 + 繁體中文）
- 📖 10 個實用代碼示例
- 🧪 功能性測試腳本

🎯 **改進：**
- 為非技術用戶設計的簡潔用戶界面
- 易於集成的 Pythonic SDK
- 面向進階用戶的 CLI 工具
- 包含 5 個使用指南的完整文檔
- 改進的錯誤處理和用戶反饋
- GitHub 發佈自動化工具
- 完整的發佈說明和指南

**統計數據：**
- 5 個 Web UI 特性頁面
- 11 個 SDK 方法
- 11 個 CLI 命令
- 10 個雙語文檔文件
- 10 個代碼示例
- 生產就緒狀態

---

### v0.2.0 - 初始發佈
**發佈日期**：2026 年 2 月上旬

✨ **功能特性：**
- 核心記憶管理系統
- REST API，包含 11 個端點
- 向量嵌入支持（本地和 OpenAI）
- 語義搜索功能
- 協作共享系統
- 細粒度權限控制（讀、寫、共享）
- 三級訪問控制（private、shared、public）
- Bearer Token 認證
- SQLite 和 PostgreSQL 支持

🎯 **核心組件：**
- FastAPI 後端服務器
- 基礎 CLI 界面
- SDK 和 Web UI 的基礎
- 文檔框架

**性能指標：**
- 100 個記憶搜索 <200ms
- 1000 個記憶搜索 <500ms

---

### v0.1.0 - 基礎
**發佈日期**：2026 年 1 月底

✨ **初始功能：**
- 基本 Agent 記憶系統設計
- 記憶 CRUD 操作
- 簡單語義搜索
- 數據庫抽象層
- 初始 API 結構
- 認證系統基礎

🎯 **概念驗證：**
- 演示了核心記憶功能
- 建立了項目架構
- 為未來功能創建了基礎

---

## 升級路徑

| 版本 | 重點 | 狀態 |
|------|------|------|
| v0.1.0 | 基礎 | ✅ 已完成 |
| v0.2.0 | 核心功能 | ✅ 已完成 |
| v0.3.0 | 多個界面 | ✅ 已發佈 |
| v0.4.0 | 易用性 | 🚀 開發中 |
| v0.5.0+ | 高級功能 | 📋 計劃中 |

---

**最後更新**：2026 年 2 月 17 日
**當前版本**：0.3.0（生產就緒）
**開發版本**：0.4.0（開發中）
**狀態**：✅ 生產就緒（v0.3.0）
**界面**：Web UI • SDK • CLI
**文檔**：英文 • 繁體中文
