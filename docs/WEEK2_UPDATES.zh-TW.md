> **語言**: [English](WEEK2_UPDATES.md) | [繁體中文](WEEK2_UPDATES.zh-TW.md)

# AgentMem Week 2-3 更新

## 新功能

### 1. 向量嵌入系統
- **支持本地模型和 OpenAI API**：使用 sentence-transformers 進行本地嵌入或連接 OpenAI API
- **批量嵌入處理**：以提高大規模記憶的處理效率
- **自動嵌入生成**：創建和更新記憶時自動生成嵌入

### 2. 語義搜索 API
- **POST /memories/search** - 進行語義搜索
  - 支持相似度閾值設置
  - 支持分頁（limit/offset）
  - 返回相關性分數
- **GET /memories/search/stats** - 獲取搜索統計
  - 總記憶數
  - 可搜索記憶數
  - 嵌入覆蓋率

### 3. 改進的共享與權限系統
- **共享 API**
  - POST /memories/{id}/share - 與 Agent 共享記憶
  - GET /memories/{id}/shared-with - 查詢共享列表
  - DELETE /memories/{id}/share/{agent_id} - 撤銷共享
- **權限管理系統**（PermissionManager）
  - can_read_memory() - 讀取權限驗證
  - can_write_memory() - 編輯權限驗證
  - can_share_memory() - 共享權限驗證
- **權限規則**
  - 所有者可以讀、寫、共享
  - 共享對象可以讀
  - 公開記憶任何人都可以讀

### 4. 記憶 API 完整實現
- **CRUD 操作**
  - POST /memories - 創建記憶
  - GET /memories/{id} - 獲取記憶
  - PUT /memories/{id} - 更新記憶
  - DELETE /memories/{id} - 刪除記憶
  - GET /memories - 列出記憶
- **自動嵌入生成**：記憶創建和更新時自動生成嵌入

## 性能指標

| 指標 | 目標 | 實際 |
|------|------|------|
| 搜索延遲（100 記憶） | <200ms | ✓ |
| 搜索延遲（1000 記憶） | <500ms | ✓ |
| 嵌入生成速度 | >10/秒 | ✓ |
| 余弦相似度計算 | 快速 | ✓ |
| 批量嵌入效率 | 比單個快 | ✓ |

## 技術實現

### 嵌入服務 (EmbeddingService)
- 模型：all-MiniLM-L6-v2（384 維）
- 支持本地模型和 OpenAI API
- 批量處理以優化性能

### 搜索服務 (SearchService)
- 基於余弦相似度
- 支持相似度閾值過濾
- 結果按相關性排序

### 權限管理 (PermissionManager)
- 細粒度權限控制
- 支持多層級訪問控制
- 異步驗證

## API 文檔

詳見 http://localhost:8000/docs

## 測試覆蓋

- 單元測試：embedding、search、permissions
- 集成測試：端到端工作流
- 性能測試：延遲、吞吐量、效率
- API 測試：HTTP 端點驗證

## 代碼質量

- 類型提示：完整的 Python 類型註釋
- 文檔字符串：所有函數均有 docstring
- 代碼風格：PEP 8 兼容
- 測試覆蓋率：>85%

## 部署注意事項

1. **環境變量**
   - DATABASE_URL：數據庫連接字符串
   - REDIS_URL：Redis 連接字符串（可選）

2. **依賴項**
   - sentence-transformers 3.0.0+
   - numpy 1.26.0+
   - fastapi 0.104.1+
   - sqlalchemy 2.0.23+

3. **模型下載**
   - 首次運行時會自動下載 all-MiniLM-L6-v2
   - 約 90MB，需要網絡連接

## 後續改進方向

1. 支持更多嵌入模型
2. 添加向量數據庫支持（FAISS、Pinecone）
3. 實現緩存機制
4. 添加嵌入模型微調支持
5. 支持多語言嵌入
