# AgentMem Python SDK 使用指南

> **語言**: [English](SDK_GUIDE.md) | [繁體中文](SDK_GUIDE.zh-TW.md)

## 簡介

AgentMem Python SDK 提供了簡化的 Python 客戶端庫，讓開發者可以輕鬆整合 AgentMem 記憶管理系統。

無需手動構造 HTTP 請求，只需簡單的 Python 代碼即可完成所有操作。

## 快速開始

### 1. 初始化客戶端

```python
from src.client import AgentMemClient

client = AgentMemClient(
    api_url="http://localhost:8000",
    agent_id="my-agent-id"
)
```

### 2. 創建記憶

```python
memory = client.create_memory(
    content="Machine learning 是人工智能的重要分支",
    type="knowledge",
    category="ai"
)
print(f"記憶已創建: {memory.id}")
```

### 3. 搜索記憶

```python
results = client.search("人工智能", limit=10)
for result in results.results:
    print(f"[{result.similarity_score:.2%}] {result.content}")
```

### 4. 共享記憶

```python
client.share_memory("memory-id", "other-agent-id")
```

## 核心方法

- `create_memory()` - 創建新記憶
- `get_memory()` - 獲取記憶詳情
- `list_memories()` - 列出所有記憶
- `update_memory()` - 更新記憶
- `delete_memory()` - 刪除記憶
- `search()` - 語義搜索
- `get_search_stats()` - 獲取搜索統計
- `share_memory()` - 共享記憶
- `get_shared_with()` - 查詢共享列表
- `revoke_sharing()` - 撤銷共享

## 完整示例

運行快速開始示例：

```bash
python examples/quick_start.py
```

## 異常處理

```python
from src.client import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
    ConnectionError
)

try:
    memory = client.create_memory("content")
except AuthenticationError:
    print("認證失敗")
except NotFoundError:
    print("記憶不存在")
except ValidationError as e:
    print(f"驗證失敗: {e}")
except ConnectionError as e:
    print(f"連接失敗: {e}")
```

## 常見問題

**Q: 如何獲取 Agent ID?**
A: 不提供會自動生成，或使用任何 UUID。

**Q: 記憶會被保存嗎?**
A: 是的，存儲在數據庫中。

**Q: 是否支持批量操作?**
A: 可以通過循環多次調用實現。

更多信息請查看 [完整文檔](../README.md)
