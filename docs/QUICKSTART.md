# AgentMem 5 分鐘快速開始

> **語言**: [English](QUICKSTART.md) | [繁體中文](QUICKSTART.zh-TW.md)

## 簡介

本指南將在 5 分鐘內讓您了解 AgentMem 的基本使用方式。

## 前置要求

- Python 3.8+
- AgentMem 服務器正在運行（`python -m src.main`）
- 已安裝依賴項（`pip install -r requirements.txt`）

## 方式 1：Web UI（推薦新手）

### 1. 啟動 Web UI（1 分鐘）

```bash
streamlit run ui/app.py
```

應用會在 `http://localhost:8501` 自動打開。

### 2. 連接服務器（1 分鐘）

1. 在左側邊欄找到「API 配置」
2. 確認 API URL 是 `http://localhost:8000`
3. 點擊「連接服務器」按鈕
4. 看到 🟢 已連接 表示成功

### 3. 創建第一條記憶（1 分鐘）

1. 點擊主頁面的「➕ 創建記憶」
2. 選擇類型（例如：knowledge）
3. 輸入分類（例如：AI）
4. 在文本框中輸入記憶內容
5. 點擊「創建記憶」

### 4. 搜索記憶（1 分鐘）

1. 點擊「🔍 搜索記憶」
2. 輸入搜索關鍵詞（例如：機器學習）
3. 點擊「搜索」按鈕
4. 查看搜索結果和相似度分數

### 5. 管理記憶（1 分鐘）

1. 點擊「📋 管理記憶」
2. 在「查看記憶」標籤中查看所有記憶
3. 在「更新記憶」中修改記憶內容
4. 在「刪除記憶」中刪除不需要的記憶

## 方式 2：Python SDK（推薦開發者）

### 1. 安裝 SDK

```python
from src.client import AgentMemClient
import uuid
```

### 2. 初始化客戶端

```python
client = AgentMemClient(
    api_url="http://localhost:8000",
    agent_id=str(uuid.uuid4())  # 或使用已有的 ID
)
```

### 3. 創建記憶

```python
memory = client.create_memory(
    content="Machine learning 是人工智能的重要分支",
    type="knowledge",
    category="ai"
)
print(f"記憶 ID: {memory.id}")
```

### 4. 搜索記憶

```python
results = client.search(
    query="人工智能",
    limit=10,
    similarity_threshold=0.3
)

for result in results.results:
    print(f"[{result.similarity_score:.1%}] {result.content}")
```

### 5. 更新和刪除

```python
# 更新
client.update_memory(
    memory.id,
    content="更新後的內容"
)

# 刪除
client.delete_memory(memory.id)
```

## 方式 3：命令行 CLI（推薦進階用戶）

### 1. 初始化 CLI

```bash
python -m src.cli.main init
```

### 2. 創建記憶

```bash
python -m src.cli.main create "我的第一條記憶"
```

### 3. 搜索記憶

```bash
python -m src.cli.main search "機器學習"
```

### 4. 查看所有記憶

```bash
python -m src.cli.main list --limit 20
```

### 5. 獲取統計信息

```bash
python -m src.cli.main stats
```

## 常見任務

### 任務 1：分享記憶給其他 Agent

**Web UI:**
1. 點擊「👥 共享記憶」
2. 輸入記憶 ID 和目標 Agent ID
3. 點擊「共享」

**Python SDK:**
```python
client.share_memory("memory-id", "other-agent-id")
```

**CLI:**
```bash
python -m src.cli.main share "memory-id" "other-agent-id"
```

### 任務 2：查看搜索統計

**Web UI:**
1. 進入「🔍 搜索記憶」
2. 勾選「顯示搜索統計」

**Python SDK:**
```python
stats = client.get_search_stats()
print(f"總記憶數: {stats.total_memories}")
print(f"覆蓋率: {stats.embedding_coverage:.1%}")
```

**CLI:**
```bash
python -m src.cli.main stats
```

### 任務 3：檢查服務器健康狀態

**Web UI:** 自動在邊欄顯示

**Python SDK:**
```python
if client.health_check():
    print("服務器正常")
```

**CLI:**
```bash
python -m src.cli.main health -v
```

## 下一步

完成快速開始後，建議查看：

- [詳細使用指南](USAGE_GUIDE.md) - 深入瞭解所有功能
- [代碼示例](EXAMPLES.md) - 更多使用案例
- [API 參考](API_REFERENCE.md) - 完整 API 文檔
- [常見問題解決](TROUBLESHOOTING.md) - 解決問題

## 需要幫助？

- 📖 查看完整 [文檔](../README.md)
- 🐛 報告問題：[GitHub Issues](https://github.com/yourusername/agentmem/issues)
- 💬 提出建議：[GitHub Discussions](https://github.com/yourusername/agentmem/discussions)

---

**提示**: 不同的方式各有優勢：
- **Web UI**: 最容易上手，適合非技術用戶
- **Python SDK**: 最靈活，適合集成到其他應用
- **CLI**: 最便捷，適合腳本和自動化
