# AgentMem API 參考

> **語言**: [English](API_REFERENCE.md) | [繁體中文](API_REFERENCE.zh-TW.md)

## 概述

AgentMem API 是基於 REST 的 HTTP API，用於記憶管理和搜索。所有請求和響應都使用 JSON 格式。

### 基本信息

- **基礎 URL**: `http://localhost:8000`
- **認證**: 使用 Agent ID 識別用戶
- **內容類型**: `application/json`

## 認證

所有 API 請求都必須包含 `X-Agent-ID` 頭：

```bash
curl -H "X-Agent-ID: your-agent-id" \
     http://localhost:8000/api/v1/memories
```

## 端點

### 1. 健康檢查

檢查服務器狀態。

```
GET /health
```

#### 響應

```json
{
  "status": "healthy",
  "timestamp": "2025-02-17T10:30:00Z"
}
```

#### 示例

```bash
curl http://localhost:8000/health
```

### 2. 創建記憶

創建新記憶。

```
POST /api/v1/memories
```

#### 請求體

```json
{
  "content": "記憶內容",
  "type": "knowledge",
  "category": "ai",
  "visibility": "private"
}
```

#### 參數

| 參數 | 類型 | 必需 | 說明 |
|------|------|------|------|
| content | string | 是 | 記憶內容 |
| type | string | 否 | 類型：knowledge, note, experience, idea |
| category | string | 否 | 分類標籤 |
| visibility | string | 否 | 可見性：private, shared, public |

#### 響應

```json
{
  "id": "memory-uuid",
  "content": "記憶內容",
  "type": "knowledge",
  "category": "ai",
  "visibility": "private",
  "agent_id": "agent-uuid",
  "created_at": "2025-02-17T10:30:00Z",
  "updated_at": "2025-02-17T10:30:00Z"
}
```

#### 示例

```bash
curl -X POST http://localhost:8000/api/v1/memories \
  -H "X-Agent-ID: agent-123" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Python 是一門強大的編程語言",
    "type": "knowledge",
    "category": "programming"
  }'
```

### 3. 獲取記憶

獲取單個記憶的詳細信息。

```
GET /api/v1/memories/{memory_id}
```

#### 參數

| 參數 | 類型 | 說明 |
|------|------|------|
| memory_id | string | 記憶 ID |

#### 響應

```json
{
  "id": "memory-uuid",
  "content": "記憶內容",
  "type": "knowledge",
  "category": "ai",
  "visibility": "private",
  "agent_id": "agent-uuid",
  "created_at": "2025-02-17T10:30:00Z",
  "updated_at": "2025-02-17T10:30:00Z"
}
```

### 4. 列表記憶

列出用戶的所有記憶。

```
GET /api/v1/memories?limit=20&offset=0
```

#### 查詢參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| limit | integer | 20 | 返回結果數量 |
| offset | integer | 0 | 分頁偏移量 |

#### 響應

```json
{
  "items": [
    {
      "id": "memory-uuid",
      "content": "...",
      "type": "knowledge",
      "category": "ai",
      "created_at": "2025-02-17T10:30:00Z"
    }
  ],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

### 5. 更新記憶

更新現有記憶。

```
PUT /api/v1/memories/{memory_id}
```

#### 請求體

```json
{
  "content": "更新的內容",
  "type": "note",
  "category": "updated"
}
```

#### 響應

```json
{
  "id": "memory-uuid",
  "content": "更新的內容",
  "type": "note",
  "category": "updated",
  "updated_at": "2025-02-17T10:35:00Z"
}
```

### 6. 刪除記憶

刪除記憶。

```
DELETE /api/v1/memories/{memory_id}
```

#### 響應

```json
{
  "success": true,
  "message": "記憶已刪除"
}
```

### 7. 搜索記憶

進行語義相似度搜索。

```
POST /api/v1/memories/search
```

#### 請求體

```json
{
  "query": "機器學習",
  "limit": 10,
  "similarity_threshold": 0.3
}
```

#### 參數

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| query | string | - | 搜索查詢 |
| limit | integer | 10 | 返回結果數量 |
| similarity_threshold | float | 0.3 | 相似度閾值 (0.0-1.0) |

#### 響應

```json
{
  "query": "機器學習",
  "results": [
    {
      "memory_id": "memory-uuid",
      "content": "機器學習是人工智能的重要分支",
      "type": "knowledge",
      "category": "ai",
      "similarity_score": 0.95,
      "rank": 1
    }
  ],
  "total_results": 1,
  "query_embedding_time_ms": 45,
  "search_time_ms": 12
}
```

### 8. 搜索統計

獲取搜索相關的統計信息。

```
GET /api/v1/memories/stats
```

#### 響應

```json
{
  "total_memories": 1000,
  "searchable_memories": 950,
  "embedding_coverage": 0.95,
  "last_embedding_update": "2025-02-17T10:20:00Z"
}
```

### 9. 共享記憶

與另一個 Agent 共享記憶。

```
POST /api/v1/memories/{memory_id}/share
```

#### 請求體

```json
{
  "agent_id": "target-agent-id"
}
```

#### 響應

```json
{
  "success": true,
  "memory_id": "memory-uuid",
  "shared_with": "target-agent-id"
}
```

### 10. 獲取共享列表

查詢記憶已共享給哪些 Agents。

```
GET /api/v1/memories/{memory_id}/shared-with
```

#### 響應

```json
{
  "memory_id": "memory-uuid",
  "shared_with": [
    "agent-uuid-1",
    "agent-uuid-2"
  ],
  "total_shares": 2
}
```

### 11. 撤銷共享

取消與特定 Agent 的共享。

```
DELETE /api/v1/memories/{memory_id}/share/{agent_id}
```

#### 響應

```json
{
  "success": true,
  "message": "共享已撤銷"
}
```

## 錯誤響應

### 錯誤格式

所有錯誤都返回相同的 JSON 格式：

```json
{
  "error": "錯誤代碼",
  "message": "詳細錯誤信息",
  "status_code": 400
}
```

### 常見錯誤

| 狀態碼 | 錯誤代碼 | 說明 |
|--------|---------|------|
| 400 | INVALID_REQUEST | 請求參數無效 |
| 401 | UNAUTHORIZED | 缺少或無效的 Agent ID |
| 404 | NOT_FOUND | 記憶不存在 |
| 409 | ALREADY_EXISTS | 記憶已存在 |
| 422 | VALIDATION_ERROR | 數據驗證失敗 |
| 500 | INTERNAL_ERROR | 服務器內部錯誤 |

## 速率限制

目前沒有實施速率限制，但建議每秒不超過 100 個請求。

## 示例

### 使用 curl

```bash
# 創建記憶
curl -X POST http://localhost:8000/api/v1/memories \
  -H "X-Agent-ID: my-agent" \
  -H "Content-Type: application/json" \
  -d '{"content": "test content", "type": "knowledge"}'

# 搜索
curl -X POST http://localhost:8000/api/v1/memories/search \
  -H "X-Agent-ID: my-agent" \
  -H "Content-Type: application/json" \
  -d '{"query": "機器學習", "limit": 10}'

# 獲取統計
curl http://localhost:8000/api/v1/memories/stats \
  -H "X-Agent-ID: my-agent"
```

### 使用 Python

```python
import requests

headers = {
    "X-Agent-ID": "my-agent",
    "Content-Type": "application/json"
}

# 創建記憶
response = requests.post(
    "http://localhost:8000/api/v1/memories",
    headers=headers,
    json={
        "content": "test content",
        "type": "knowledge"
    }
)

# 搜索
response = requests.post(
    "http://localhost:8000/api/v1/memories/search",
    headers=headers,
    json={
        "query": "機器學習",
        "limit": 10
    }
)
```

## 數據類型

### 記憶類型 (type)

- `knowledge`: 知識條目
- `note`: 筆記
- `experience`: 經驗
- `idea`: 想法

### 可見性 (visibility)

- `private`: 私密（僅所有者可見）
- `shared`: 可共享（所有者和已授權用戶可見）
- `public`: 公開（所有人可見）

## 最佳實踐

1. **錯誤處理**: 總是檢查響應狀態碼
2. **分頁**: 使用 limit 和 offset 進行大規模查詢
3. **超時**: 設置合理的連接超時
4. **幂等性**: 對於創建操作，考慮使用唯一標識符避免重複

---

需要幫助？查看 [使用指南](USAGE_GUIDE.md) 或 [常見問題解決](TROUBLESHOOTING.md)
