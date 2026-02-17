> **語言**: [English](README.md) | [繁體中文](README.zh-TW.md)

# AgentMem - Agent Memory System

一個為 AI Agent 設計的高效記憶管理系統，支持向量嵌入、語義搜索和協作共享。

## 版本

**0.2.0** - Week 2-3 增強版本

## 特性

### ✨ 核心功能
- **記憶管理**：創建、更新、刪除、查詢記憶
- **向量嵌入**：自動生成文本嵌入（支持本地和 OpenAI API）
- **語義搜索**：基於向量相似度的智能搜索
- **協作共享**：在 Agent 之間安全地共享記憶
- **細粒度權限**：讀、寫、共享三級權限控制
- **高性能搜索**：100 個記憶 <200ms，1000 個記憶 <500ms

### 🔒 安全特性
- Bearer Token 認證
- 權限驗證系統
- 訪問控制列表（ACL）
- 記憶可見性級別（private/shared/public）

## 快速開始

### 前置要求
- Python 3.11+
- Docker & Docker Compose
- 4GB+ RAM（用於模型加載）

### 安裝和運行

1. **克隆項目**
   ```bash
   git clone <repository-url>
   cd agent-memory-mvp
   ```

2. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

3. **啟動 Docker 容器**
   ```bash
   make docker-up
   ```

4. **運行測試**
   ```bash
   make test
   ```

5. **訪問 API**
   - API 文檔：http://localhost:8000/docs
   - ReDoc：http://localhost:8000/redoc
   - 健康檢查：http://localhost:8000/health

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
│   ├── api/                 # API 路由
│   │   ├── memories.py      # 記憶 CRUD API
│   │   ├── search.py        # 搜索 API
│   │   └── sharing.py       # 共享 API
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
├── tests/                   # 測試
│   ├── test_embeddings.py
│   ├── test_search.py
│   ├── test_permissions.py
│   ├── test_integration.py
│   └── test_performance.py
├── docs/                    # 文檔
│   └── WEEK2_UPDATES.md
├── requirements.txt         # 依賴項
├── docker-compose.yml       # Docker 配置
├── Dockerfile
├── Makefile
└── README.md
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

---

**最後更新**：2026 年 2 月 17 日
**版本**：0.2.0
**狀態**：✅ 生產就緒
