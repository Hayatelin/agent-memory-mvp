# AgentMem 代碼示例

> **語言**: [English](EXAMPLES.md) | [繁體中文](EXAMPLES.zh-TW.md)

## 示例 1：基本的記憶管理

### Python SDK 示例

```python
from src.client import AgentMemClient
import uuid

# 初始化客戶端
client = AgentMemClient(
    api_url="http://localhost:8000",
    agent_id=str(uuid.uuid4())
)

# 創建幾條不同類型的記憶
memories = [
    {
        "content": "Python 是一門通用編程語言，廣泛用於 Web 開發、數據分析和 AI",
        "type": "knowledge",
        "category": "programming"
    },
    {
        "content": "今天學習了 FastAPI 框架的基本用法，非常高效",
        "type": "experience",
        "category": "learning"
    },
    {
        "content": "想要開發一個基於向量數據庫的搜索引擎",
        "type": "idea",
        "category": "project"
    }
]

memory_ids = []
for mem in memories:
    memory = client.create_memory(**mem)
    memory_ids.append(memory.id)
    print(f"Created: {memory.id}")

# 搜索相關記憶
results = client.search("Python 編程", limit=5)
print(f"\nFound {len(results.results)} memories:")
for result in results.results:
    print(f"  [{result.similarity_score:.1%}] {result.content[:50]}...")
```

## 示例 2：高級搜索

### 多查詢搜索

```python
from src.client import AgentMemClient

client = AgentMemClient(
    api_url="http://localhost:8000",
    agent_id="user-001"
)

# 不同搜索場景
searches = [
    {"query": "機器學習", "threshold": 0.5, "limit": 10},
    {"query": "Python 開發", "threshold": 0.3, "limit": 20},
    {"query": "數據庫設計", "threshold": 0.7, "limit": 5}
]

for search in searches:
    results = client.search(
        query=search["query"],
        limit=search["limit"],
        similarity_threshold=search["threshold"]
    )

    print(f"\nSearching: {search['query']}")
    print(f"Found: {len(results.results)} results")
    print(f"Query time: {results.query_embedding_time_ms}ms")
    print(f"Search time: {results.search_time_ms}ms")

    for i, result in enumerate(results.results[:3], 1):
        print(f"  {i}. [{result.similarity_score:.1%}] {result.content[:60]}...")
```

## 示例 3：批量操作

### 從檔案批量導入

```python
from src.client import AgentMemClient
import json

client = AgentMemClient()

# 從 JSON 檔案中讀取記憶
with open("memories.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 批量創建
created_count = 0
failed_count = 0

for item in data:
    try:
        memory = client.create_memory(
            content=item["content"],
            type=item.get("type", "knowledge"),
            category=item.get("category", "general")
        )
        created_count += 1
        print(f"✓ Created: {memory.id}")
    except Exception as e:
        failed_count += 1
        print(f"✗ Failed: {item['content'][:30]}... - {e}")

print(f"\nSummary: {created_count} created, {failed_count} failed")
```

### 記憶檔案格式 (memories.json)

```json
[
    {
        "content": "FastAPI 是一個現代的高性能 Web 框架",
        "type": "knowledge",
        "category": "web-framework"
    },
    {
        "content": "向量數據庫適合大規模相似度搜索",
        "type": "knowledge",
        "category": "database"
    },
    {
        "content": "成功部署了第一個 Docker 容器",
        "type": "experience",
        "category": "devops"
    }
]
```

## 示例 4：記憶共享

### 多用戶場景

```python
from src.client import AgentMemClient
import uuid

# 創建多個 Agent
agent1_id = str(uuid.uuid4())
agent2_id = str(uuid.uuid4())
agent3_id = str(uuid.uuid4())

client1 = AgentMemClient(api_url="http://localhost:8000", agent_id=agent1_id)
client2 = AgentMemClient(api_url="http://localhost:8000", agent_id=agent2_id)
client3 = AgentMemClient(api_url="http://localhost:8000", agent_id=agent3_id)

# Agent 1 創建記憶
memory = client1.create_memory(
    content="高效的 Python 性能優化技巧",
    type="knowledge",
    category="performance"
)

print(f"Agent 1 created memory: {memory.id}")

# Agent 1 與 Agent 2 和 3 共享
client1.share_memory(memory.id, agent2_id)
client1.share_memory(memory.id, agent3_id)
print(f"Shared with {agent2_id[:8]}... and {agent3_id[:8]}...")

# 驗證共享
shared_with = client1.get_shared_with(memory.id)
print(f"Total shares: {len(shared_with)}")

# Agent 2 可以搜索共享的記憶
results = client2.search("性能優化", limit=10)
print(f"\nAgent 2 search results: {len(results.results)}")

# Agent 1 撤銷與 Agent 3 的共享
client1.revoke_sharing(memory.id, agent3_id)
print(f"\nRevoked sharing with {agent3_id[:8]}...")

# 驗證撤銷
shared_with = client1.get_shared_with(memory.id)
print(f"Remaining shares: {len(shared_with)}")
```

## 示例 5：錯誤處理和重試

### 健壯的客戶端實現

```python
from src.client import (
    AgentMemClient,
    ConnectionError,
    ValidationError,
    ServerError
)
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobustClient:
    def __init__(self, api_url, agent_id, max_retries=3):
        self.api_url = api_url
        self.agent_id = agent_id
        self.max_retries = max_retries
        self.client = None
        self._connect()

    def _connect(self):
        """建立連接"""
        for attempt in range(self.max_retries):
            try:
                self.client = AgentMemClient(
                    api_url=self.api_url,
                    agent_id=self.agent_id
                )
                if self.client.health_check():
                    logger.info("Connected successfully")
                    return
            except Exception as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)

        raise RuntimeError("Could not connect after retries")

    def create_memory_safe(self, content, **kwargs):
        """安全的創建記憶"""
        for attempt in range(self.max_retries):
            try:
                return self.client.create_memory(content=content, **kwargs)
            except ValidationError as e:
                logger.error(f"Validation error: {e}")
                raise
            except ServerError as e:
                logger.warning(f"Server error (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise
            except ConnectionError as e:
                logger.warning(f"Connection error (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise

# 使用
try:
    robust_client = RobustClient(
        api_url="http://localhost:8000",
        agent_id="robust-agent"
    )

    memory = robust_client.create_memory_safe(
        content="重要的記憶",
        type="knowledge"
    )
    print(f"Created: {memory.id}")

except Exception as e:
    logger.error(f"Failed to create memory: {e}")
```

## 示例 6：統計分析

### 記憶分析

```python
from src.client import AgentMemClient
from collections import defaultdict

client = AgentMemClient()

# 獲取統計信息
stats = client.get_search_stats()
print(f"Total memories: {stats.total_memories}")
print(f"Searchable memories: {stats.searchable_memories}")
print(f"Embedding coverage: {stats.embedding_coverage:.1%}")

# 分析記憶分佈
print("\n=== Memory Analysis ===")

# 按分類分組
all_memories = client.list_memories(limit=1000)

type_count = defaultdict(int)
category_count = defaultdict(int)
visibility_count = defaultdict(int)

for memory in all_memories:
    type_count[memory.type] += 1
    category_count[memory.category] += 1
    visibility_count[memory.visibility] += 1

print("\nBy Type:")
for mem_type, count in sorted(type_count.items(), key=lambda x: x[1], reverse=True):
    print(f"  {mem_type}: {count}")

print("\nBy Category:")
for category, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {category}: {count}")

print("\nBy Visibility:")
for visibility, count in visibility_count.items():
    print(f"  {visibility}: {count}")
```

## 示例 7：CLI 腳本

### 自動化腳本

```bash
#!/bin/bash

# 配置 API
API_URL="http://localhost:8000"
AGENT_ID="automation-agent"

# 配置 CLI
export AGENTMEM_API_URL=$API_URL
export AGENTMEM_AGENT_ID=$AGENT_ID

echo "=== AgentMem Automation ==="

# 檢查健康狀態
echo "Checking server health..."
python -m src.cli.main health

# 創建記憶
echo -e "\nCreating memories..."
python -m src.cli.main create "批處理記憶 1"
python -m src.cli.main create "批處理記憶 2"
python -m src.cli.main create "批處理記憶 3"

# 搜索
echo -e "\nSearching memories..."
python -m src.cli.main search "批處理" --limit 5

# 查看統計
echo -e "\nStatistics:"
python -m src.cli.main stats

# 列出記憶
echo -e "\nMemory list:"
python -m src.cli.main list --limit 10
```

## 示例 8：Web UI 集成

### 在 Streamlit 應用中使用

```python
import streamlit as st
from src.client import AgentMemClient
import uuid

# 頁面配置
st.set_page_config(page_title="記憶助手", page_icon="🧠")

# 初始化 Session State
if "client" not in st.session_state:
    st.session_state.client = None

# 側邊欄配置
with st.sidebar:
    st.header("配置")
    api_url = st.text_input("API URL", value="http://localhost:8000")

    if st.button("連接"):
        try:
            client = AgentMemClient(
                api_url=api_url,
                agent_id=str(uuid.uuid4())
            )
            if client.health_check():
                st.session_state.client = client
                st.success("連接成功！")
            else:
                st.error("無法連接")
        except Exception as e:
            st.error(f"連接失敗: {e}")

# 主內容
st.title("🧠 AI 記憶助手")

if not st.session_state.client:
    st.warning("請先在側邊欄連接服務器")
else:
    client = st.session_state.client

    # 標籤頁
    tab1, tab2, tab3 = st.tabs(["創建", "搜索", "統計"])

    with tab1:
        st.subheader("創建記憶")
        content = st.text_area("內容")
        mem_type = st.selectbox("類型", ["knowledge", "note", "experience", "idea"])

        if st.button("創建"):
            try:
                memory = client.create_memory(content=content, type=mem_type)
                st.success(f"Created: {memory.id}")
            except Exception as e:
                st.error(f"Failed: {e}")

    with tab2:
        st.subheader("搜索記憶")
        query = st.text_input("搜索查詢")

        if st.button("搜索"):
            try:
                results = client.search(query, limit=10)
                st.info(f"Found {len(results.results)} results")

                for result in results.results:
                    st.write(f"**[{result.similarity_score:.1%}]** {result.content[:100]}")

            except Exception as e:
                st.error(f"Search failed: {e}")

    with tab3:
        st.subheader("統計信息")
        try:
            stats = client.get_search_stats()
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("總記憶", stats.total_memories)
            with col2:
                st.metric("可搜索", stats.searchable_memories)
            with col3:
                st.metric("覆蓋率", f"{stats.embedding_coverage:.1%}")

        except Exception as e:
            st.error(f"Failed to load stats: {e}")
```

## 示例 9：進階搜索技巧

### 多語言搜索

```python
from src.client import AgentMemClient

client = AgentMemClient()

# 建立多語言記憶
memories = [
    "Python 是一門強大的編程語言",  # 中文
    "Python is a powerful programming language",  # 英文
    "Python 是一個很好的选择",  # 簡體中文
]

ids = []
for content in memories:
    memory = client.create_memory(
        content=content,
        type="knowledge",
        category="multilingual"
    )
    ids.append(memory.id)

# 使用中文搜索
results_cn = client.search("編程語言", limit=10)
print(f"Chinese query results: {len(results_cn.results)}")

# 使用英文搜索
results_en = client.search("programming language", limit=10)
print(f"English query results: {len(results_en.results)}")

# 混合搜索
results_mixed = client.search("Python programming", limit=10)
print(f"Mixed query results: {len(results_mixed.results)}")
```

## 示例 10：完整的應用流程

### 知識管理系統

```python
from src.client import AgentMemClient
from datetime import datetime
import uuid

class KnowledgeManager:
    def __init__(self, api_url="http://localhost:8000"):
        self.client = AgentMemClient(
            api_url=api_url,
            agent_id=f"knowledge-manager-{uuid.uuid4().hex[:8]}"
        )

    def add_article(self, title, content, category, tags):
        """添加文章"""
        memory = self.client.create_memory(
            content=f"標題: {title}\n\n{content}\n\n標籤: {', '.join(tags)}",
            type="knowledge",
            category=category,
            visibility="shared"
        )
        return memory

    def search_by_topic(self, topic, limit=10):
        """按主題搜索"""
        results = self.client.search(
            query=topic,
            limit=limit,
            similarity_threshold=0.4
        )
        return results

    def get_statistics(self):
        """獲取統計"""
        return self.client.get_search_stats()

    def export_memories(self):
        """導出記憶"""
        memories = self.client.list_memories(limit=1000)
        export_data = {
            "export_time": datetime.now().isoformat(),
            "total_count": len(memories),
            "memories": [
                {
                    "id": m.id,
                    "type": m.type,
                    "category": m.category,
                    "content": m.content[:200],
                    "created_at": str(m.created_at)
                }
                for m in memories
            ]
        }
        return export_data

# 使用示例
km = KnowledgeManager()

# 添加文章
article = km.add_article(
    title="機器學習基礎",
    content="機器學習是人工智能的重要領域...",
    category="ai",
    tags=["ml", "ai", "python"]
)

# 搜索
results = km.search_by_topic("機器學習")
for result in results.results[:3]:
    print(f"[{result.similarity_score:.1%}] {result.content[:100]}")

# 統計
stats = km.get_statistics()
print(f"Total: {stats.total_memories}, Coverage: {stats.embedding_coverage:.1%}")

# 導出
export = km.export_memories()
print(f"Exported {export['total_count']} memories")
```

---

需要更多示例？查看 [完整文檔](../README.md) 或 [使用指南](USAGE_GUIDE.md)
