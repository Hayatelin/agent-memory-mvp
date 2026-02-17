# AgentMem 常見問題解決

> **語言**: [English](TROUBLESHOOTING.md) | [繁體中文](TROUBLESHOOTING.zh-TW.md)

## 常見問題

### 1. 無法連接到服務器

#### 症狀
- Web UI 顯示「未連接」
- Python SDK 拋出 `ConnectionError`
- CLI 命令失敗

#### 可能原因
1. 服務器未啟動
2. API URL 不正確
3. 防火牆阻止連接
4. 服務器崩潰

#### 解決方案

**第一步：檢查服務器是否運行**

```bash
# 檢查服務器進程
ps aux | grep "python -m src.main"

# 如果沒有運行，啟動服務器
python -m src.main
```

**第二步：驗證 API URL**

```bash
# 測試連接
curl http://localhost:8000/health

# 應該返回：
# {"status": "healthy"}
```

**第三步：檢查防火牆**

```bash
# 在 Linux/Mac 上
lsof -i :8000

# 在 Windows 上（使用 PowerShell）
Get-NetTCPConnection -LocalPort 8000
```

**第四步：檢查服務器日誌**

```bash
# 查看最後 50 行日誌
tail -50 server.log

# 查看所有錯誤
grep ERROR server.log
```

### 2. 記憶搜索返回空結果

#### 症狀
- 搜索查詢返回 0 結果，但記憶存在

#### 可能原因
1. 相似度閾值太高
2. 記憶嵌入還未生成
3. 查詢與記憶不相關

#### 解決方案

**降低相似度閾值**

```python
# 使用更低的閾值
results = client.search(
    query="機器學習",
    limit=10,
    similarity_threshold=0.2  # 從 0.3 改為 0.2
)
```

**檢查嵌入覆蓋率**

```python
stats = client.get_search_stats()
print(f"覆蓋率: {stats.embedding_coverage:.1%}")

# 如果覆蓋率低於 80%，等待嵌入生成
```

**使用不同的查詢**

```python
# 嘗試更簡單的查詢
results = client.search(query="AI")  # 而不是 "人工智能機器學習深度學習"

# 或使用更詳細的查詢
results = client.search(query="機器學習算法")
```

### 3. 記憶創建失敗

#### 症狀
- 創建記憶時拋出異常
- 消息指示驗證錯誤

#### 常見錯誤信息

**「Content is required」**
```python
# 錯誤：內容為空
memory = client.create_memory(content="")

# 正確：提供內容
memory = client.create_memory(content="有效內容")
```

**「Invalid memory type」**
```python
# 錯誤：類型不正確
memory = client.create_memory(content="...", type="article")

# 正確：使用允許的類型
memory = client.create_memory(content="...", type="knowledge")
```

**「Category too long」**
```python
# 錯誤：分類過長
memory = client.create_memory(content="...", category="a" * 1000)

# 正確：使用合理長度
memory = client.create_memory(content="...", category="programming")
```

### 4. Web UI 無法啟動

#### 症狀
- Streamlit 啟動時出錯
- 頁面無法載入

#### 解決方案

**檢查 Python 版本**

```bash
python --version
# 需要 Python 3.8+
```

**安裝依賴項**

```bash
pip install -r requirements.txt --upgrade
```

**清除 Streamlit 緩存**

```bash
# 在 Linux/Mac
rm -rf ~/.streamlit/cache

# 在 Windows
Remove-Item -Recurse $env:USERPROFILE\.streamlit\cache
```

**以調試模式運行**

```bash
streamlit run ui/app.py --logger.level=debug
```

### 5. 記憶共享不起作用

#### 症狀
- 共享後，目標 Agent 無法看到記憶

#### 可能原因
1. 目標 Agent ID 不存在
2. 記憶不存在
3. 權限設置錯誤

#### 解決方案

**驗證 Agent ID**

```python
# 確保 Agent ID 有效
other_agent_id = "550e8400-e29b-41d4-a716-446655440000"  # 有效格式

# 共享
client.share_memory(memory_id, other_agent_id)
```

**檢查共享列表**

```python
# 驗證共享是否成功
shared_with = client.get_shared_with(memory_id)
print(f"已共享給: {shared_with}")
```

**檢查記憶可見性**

```python
# 確保記憶不是私有的
memory = client.get_memory(memory_id)
print(f"可見性: {memory.visibility}")

# 如果是 private，需要先更新
if memory.visibility == "private":
    client.update_memory(
        memory_id,
        visibility="shared"
    )
```

### 6. 數據庫連接失敗

#### 症狀
- 服務器無法啟動
- 日誌顯示「Connection refused」

#### 解決方案

**檢查 PostgreSQL 服務**

```bash
# 在 Linux/Mac
brew services list | grep postgres

# 在 Windows
Get-Service PostgreSQL*

# 如果未運行，啟動它
brew services start postgresql
```

**檢查數據庫配置**

```bash
# 編輯 .env 檔案
cat .env

# 驗證數據庫 URL
DATABASE_URL=postgresql://user:password@localhost:5432/agentmem
```

**重新創建數據庫**

```bash
# 刪除現有數據庫
dropdb agentmem

# 創建新數據庫
createdb agentmem

# 運行遷移
alembic upgrade head
```

### 7. 記憶嵌入生成緩慢

#### 症狀
- 嵌入覆蓋率進展緩慢
- 搜索延遲

#### 解決方案

**檢查 GPU 可用性**

```python
import torch
print(f"GPU available: {torch.cuda.is_available()}")
print(f"GPU device: {torch.cuda.get_device_name()}")
```

**優化嵌入設置**

在 `.env` 中調整：

```env
# 增加批大小以加快嵌入生成
EMBEDDING_BATCH_SIZE=128

# 增加工作進程
EMBEDDING_WORKERS=4
```

**監控進度**

```bash
# 查看服務器日誌
tail -f server.log | grep embedding

# 或使用 stats 端點
curl http://localhost:8000/api/v1/memories/stats
```

### 8. CLI 命令不工作

#### 症狀
- CLI 命令返回錯誤
- 配置文件問題

#### 常見問題

**配置丟失**

```bash
# 重新初始化 CLI
python -m src.cli.main init

# 重新配置
python -m src.cli.main configure --api-url http://localhost:8000
python -m src.cli.main configure --agent-id your-id
```

**環境變量優先級**

CLI 優先級（從高到低）：
1. 命令行參數
2. 環境變量 (`AGENTMEM_*`)
3. 配置文件 (`~/.agentmem/config.json`)
4. 預設值

```bash
# 使用環境變量
export AGENTMEM_API_URL=http://localhost:8000
export AGENTMEM_AGENT_ID=my-agent

python -m src.cli.main search "query"
```

### 9. 記憶更新不生效

#### 症狀
- 使用 `update_memory` 後，記憶內容未改變

#### 可能原因
1. 記憶 ID 不正確
2. 權限問題
3. 緩存問題

#### 解決方案

**驗證記憶 ID**

```python
# 獲取記憶並檢查
memory = client.get_memory(memory_id)
print(f"Current content: {memory.content}")

# 執行更新
updated = client.update_memory(
    memory_id,
    content="新內容"
)

# 驗證更新
refreshed = client.get_memory(memory_id)
print(f"Updated content: {refreshed.content}")
```

**檢查所有權**

```python
# 確保您是記憶的所有者
memory = client.get_memory(memory_id)
print(f"Owner: {memory.agent_id}")
print(f"Your ID: {client.agent_id}")
```

### 10. 高記憶數量的性能問題

#### 症狀
- 列表操作變慢
- 搜索延遲增加

#### 解決方案

**使用分頁**

```python
# 不好：一次載入所有記憶
all_memories = client.list_memories(limit=10000)

# 好：分頁加載
def get_all_memories_paginated(batch_size=100):
    offset = 0
    while True:
        batch = client.list_memories(limit=batch_size, offset=offset)
        if not batch:
            break
        yield from batch
        offset += batch_size

for memory in get_all_memories_paginated():
    process(memory)
```

**優化搜索查詢**

```python
# 使用更高的閾值
results = client.search(
    query="query",
    limit=10,
    similarity_threshold=0.6  # 更高 = 更快
)
```

**定期清理**

```python
# 刪除舊或不需要的記憶
old_memories = client.list_memories()
for memory in old_memories:
    if should_delete(memory):
        client.delete_memory(memory.id)
```

## 獲取幫助

### 資源

- 📖 [完整文檔](../README.md)
- 🚀 [快速開始](QUICKSTART.md)
- 📚 [使用指南](USAGE_GUIDE.md)
- 💻 [代碼示例](EXAMPLES.md)
- 🔌 [API 參考](API_REFERENCE.md)

### 報告問題

如果您遇到文檔中未列出的問題，請：

1. 查看 [GitHub Issues](https://github.com/yourusername/agentmem/issues)
2. 搜索相同問題
3. 創建新 Issue，包括：
   - 詳細的錯誤消息
   - 複現步驟
   - 系統信息（OS、Python 版本）
   - 日誌輸出

## 性能調整

### 推薦配置

**開發環境**
```env
WORKERS=1
BATCH_SIZE=32
EMBEDDING_CACHE_SIZE=100
```

**生產環境**
```env
WORKERS=4
BATCH_SIZE=128
EMBEDDING_CACHE_SIZE=10000
MAX_POOL_SIZE=20
```

---

還有其他問題？ 歡迎在 [GitHub Discussions](https://github.com/yourusername/agentmem/discussions) 中提問！
