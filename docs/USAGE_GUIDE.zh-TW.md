# AgentMem 詳細使用指南

> **語言**: [English](USAGE_GUIDE.md) | [繁體中文](USAGE_GUIDE.zh-TW.md)

## 目錄

1. [Web UI 使用](#web-ui-使用)
2. [Python SDK 使用](#python-sdk-使用)
3. [CLI 使用](#cli-使用)
4. [高級功能](#高級功能)
5. [最佳實踐](#最佳實踐)

## Web UI 使用

### 啟動 Web UI

```bash
streamlit run ui/app.py
```

應用會自動在瀏覽器中打開 `http://localhost:8501`

### 側邊欄設置

#### API 配置
- **API URL**: 您的 AgentMem 服務器地址（預設：http://localhost:8000）
- **Agent ID**: 此應用的唯一標識符（可自動生成）

#### 連接狀態
- 綠點 🟢 表示已連接
- 黃點 🟡 表示未連接

#### 快速統計
連接後會自動顯示：
- 總記憶數
- 嵌入覆蓋率

### 創建記憶頁面

#### 欄位說明

| 欄位 | 說明 | 示例 |
|------|------|------|
| 記憶類型 | 記憶的分類類型 | knowledge, note, experience, idea |
| 分類 | 自定義分類標籤 | ai, python, database |
| 可見性 | 訪問權限 | private, shared, public |
| 記憶內容 | 要保存的實際內容 | 詳細的技術知識或經驗 |

#### 創建步驟

1. 選擇記憶類型（4 種可選）
2. 輸入分類（可自由定義）
3. 選擇可見性級別
4. 輸入記憶內容（支持長文本）
5. 點擊「創建記憶」

#### 響應信息

成功創建後會顯示：
- 成功消息
- 分配的記憶 ID
- 記憶的詳細信息（類型、分類、可見性）
- 內容預覽

### 搜索記憶頁面

#### 搜索控件

- **搜索查詢**: 輸入要搜索的關鍵詞
- **結果數量**: 限制返回結果的數量（1-100）
- **相似度閾值**: 調整搜索精度（0.0-1.0）

#### 相似度閾值說明

- **0.0-0.3**: 寬鬆搜索，返回更多結果，可能包含不太相關的記憶
- **0.3-0.6**: 平衡模式，推薦使用，返回相關性較好的結果
- **0.6-1.0**: 嚴格搜索，只返回高度相關的記憶

#### 搜索結果

每個結果顯示：
- 相似度分數（百分比）
- 記憶類型和分類
- 完整內容
- 記憶 ID（用於其他操作）

#### 搜索統計

勾選「顯示搜索統計」可查看：
- **總記憶數**: 系統中的所有記憶
- **可搜索記憶**: 已生成嵌入的記憶數
- **覆蓋率**: 已生成嵌入的比例

### 管理記憶頁面

分為三個標籤：

#### 1. 查看記憶

- 顯示所有記憶的列表
- 支持調整顯示數量
- 點擊記憶可展開查看完整內容
- 顯示記憶的類型、分類、可見性等信息

#### 2. 更新記憶

- 輸入要更新的記憶 ID
- 修改內容、類型或分類
- 提交表單更新記憶

#### 3. 刪除記憶

- 輸入要刪除的記憶 ID
- 確認刪除操作
- 成功刪除後顯示慶祝動畫

### 共享記憶頁面

分為兩個標籤：

#### 1. 共享記憶

- 輸入要共享的記憶 ID
- 輸入目標 Agent ID
- 點擊「共享」完成共享
- 查看此記憶已共享給的所有 Agent

#### 2. 管理共享

- 輸入記憶 ID 查看其共享列表
- 針對每個 Agent 可以點擊「撤銷」取消共享
- 實時更新共享狀態

## Python SDK 使用

### 導入和初始化

```python
from src.client import AgentMemClient
import uuid

# 初始化客戶端
client = AgentMemClient(
    api_url="http://localhost:8000",
    agent_id=str(uuid.uuid4())  # 或使用已有的 ID
)
```

### 核心操作

#### 1. 創建記憶

```python
memory = client.create_memory(
    content="Machine learning 是 AI 的重要分支",
    type="knowledge",
    category="ai",
    visibility="private"  # 可選
)

print(f"記憶 ID: {memory.id}")
print(f"建立時間: {memory.created_at}")
```

#### 2. 獲取記憶

```python
# 獲取單個記憶
memory = client.get_memory("memory-id")
print(memory.content)

# 列出所有記憶
memories = client.list_memories(
    limit=20,
    offset=0  # 用於分頁
)

for memory in memories:
    print(f"[{memory.type}] {memory.content[:50]}...")
```

#### 3. 搜索記憶

```python
# 基本搜索
results = client.search(
    query="機器學習",
    limit=10,
    similarity_threshold=0.3
)

# 處理搜索結果
print(f"找到 {len(results.results)} 條記憶")
print(f"查詢耗時: {results.query_embedding_time_ms}ms")
print(f"搜索耗時: {results.search_time_ms}ms")

for result in results.results:
    print(f"[{result.similarity_score:.1%}] {result.memory_id}")
    print(f"  內容: {result.content}")
    print(f"  類型: {result.type}/{result.category}")
```

#### 4. 更新記憶

```python
updated = client.update_memory(
    memory_id="memory-id",
    content="更新的內容",
    type="note",
    category="updated"
)
```

#### 5. 刪除記憶

```python
success = client.delete_memory("memory-id")
if success:
    print("記憶已刪除")
```

### 共享功能

```python
# 共享記憶
client.share_memory(
    memory_id="memory-id",
    agent_id="other-agent-id"
)

# 查看共享列表
shared_with = client.get_shared_with("memory-id")
for agent_id in shared_with:
    print(f"已共享給: {agent_id}")

# 撤銷共享
client.revoke_sharing(
    memory_id="memory-id",
    agent_id="other-agent-id"
)
```

### 統計和健康檢查

```python
# 獲取搜索統計
stats = client.get_search_stats()
print(f"總記憶數: {stats.total_memories}")
print(f"可搜索: {stats.searchable_memories}")
print(f"覆蓋率: {stats.embedding_coverage:.1%}")

# 健康檢查
if client.health_check():
    print("服務器正常")
else:
    print("無法連接到服務器")
```

### 異常處理

```python
from src.client import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
    ConnectionError,
    ServerError
)

try:
    memory = client.create_memory("content")
except ValidationError as e:
    print(f"驗證失敗: {e}")
except NotFoundError:
    print("記憶不存在")
except AuthenticationError:
    print("認證失敗")
except ConnectionError as e:
    print(f"連接失敗: {e}")
except ServerError:
    print("服務器錯誤")
```

## CLI 使用

### 初始化

```bash
python -m src.cli.main init
```

配置文件將存儲在 `~/.agentmem/config.json`

### 配置命令

```bash
# 查看當前配置
python -m src.cli.main config

# 配置 API URL
python -m src.cli.main configure --api-url http://localhost:8000

# 配置 Agent ID
python -m src.cli.main configure --agent-id your-uuid

# 配置超時時間
python -m src.cli.main configure --timeout 30
```

### 記憶管理

```bash
# 創建記憶
python -m src.cli.main create "這是我的第一條記憶"

# 列出記憶
python -m src.cli.main list
python -m src.cli.main list --limit 50

# 獲取記憶詳情
python -m src.cli.main get <memory-id>

# 更新記憶
python -m src.cli.main update <memory-id> --content "新內容"

# 刪除記憶
python -m src.cli.main delete <memory-id>
```

### 搜索功能

```bash
# 基本搜索
python -m src.cli.main search "人工智能"

# 限制結果數量
python -m src.cli.main search "AI" --limit 20

# 設置相似度閾值
python -m src.cli.main search "ML" --threshold 0.5
```

### 共享功能

```bash
# 共享記憶
python -m src.cli.main share <memory-id> <agent-id>

# 查看共享列表
python -m src.cli.main get-shared <memory-id>

# 撤銷共享
python -m src.cli.main revoke-sharing <memory-id> <agent-id>
```

### 統計和健康

```bash
# 查看統計
python -m src.cli.main stats

# 健康檢查
python -m src.cli.main health
python -m src.cli.main health -v  # 詳細模式
```

## 高級功能

### 批量操作

#### 使用 SDK 批量創建

```python
contents = [
    "第一條記憶",
    "第二條記憶",
    "第三條記憶"
]

memory_ids = []
for content in contents:
    memory = client.create_memory(
        content=content,
        type="knowledge",
        category="batch"
    )
    memory_ids.append(memory.id)

print(f"已建立 {len(memory_ids)} 條記憶")
```

#### 使用 CLI 批量創建

```bash
#!/bin/bash

# 從檔案批量創建
while IFS= read -r line; do
    python -m src.cli.main create "$line"
done < memories.txt
```

### 搜索最佳化

```python
# 場景 1：精確搜索（相似度高）
results = client.search(
    query="Python 裝飾器實現",
    limit=5,
    similarity_threshold=0.8
)

# 場景 2：探索性搜索（更廣泛）
results = client.search(
    query="編程",
    limit=20,
    similarity_threshold=0.3
)

# 場景 3：分類搜索
results = client.search(
    query="算法",
    limit=100,
    similarity_threshold=0.5
)
```

### 權限管理

```python
# 創建私有記憶
private_memory = client.create_memory(
    content="私密信息",
    visibility="private"
)

# 創建可共享的記憶
shared_memory = client.create_memory(
    content="可與他人分享的信息",
    visibility="shared"
)

# 創建公開記憶
public_memory = client.create_memory(
    content="公開信息",
    visibility="public"
)
```

## 最佳實踐

### 1. 命名約定

```python
# 使用有意義的分類
client.create_memory(
    content="...",
    type="knowledge",
    category="machine-learning",  # 使用小寫和連字符
    visibility="shared"
)
```

### 2. 內容組織

```python
# 長內容時使用結構化格式
content = """
## 標題

### 要點 1
具體內容

### 要點 2
具體內容

### 參考
- 參考資料 1
- 參考資料 2
"""

memory = client.create_memory(content=content)
```

### 3. 錯誤處理

```python
def safe_search(query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.search(query=query)
        except ConnectionError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

### 4. 效能考量

```python
# 分頁獲取大量記憶
page_size = 50
offset = 0

while True:
    memories = client.list_memories(
        limit=page_size,
        offset=offset
    )

    if not memories:
        break

    process_batch(memories)
    offset += page_size
```

### 5. 安全性

```python
# 使用環境變量存儲敏感信息
import os

api_url = os.environ.get("AGENTMEM_API_URL")
agent_id = os.environ.get("AGENTMEM_AGENT_ID")

client = AgentMemClient(
    api_url=api_url,
    agent_id=agent_id
)
```

---

需要幫助？查看 [常見問題解決](TROUBLESHOOTING.md) 或 [API 參考](API_REFERENCE.md)
