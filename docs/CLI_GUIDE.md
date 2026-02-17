# AgentMem CLI 使用手冊

## 簡介

AgentMem CLI 是一個命令行工具，讓你可以在終端中輕鬆管理記憶，無需編寫代碼。

## 快速開始

### 1. 初始化 CLI
```bash
python -m src.cli.main init
```

### 2. 檢查服務器連接
```bash
python -m src.cli.main health -v
```

### 3. 創建記憶
```bash
python -m src.cli.main create "這是我的第一條記憶"
```

### 4. 搜索記憶
```bash
python -m src.cli.main search "人工智能"
```

## 完整命令參考

### 配置相關
```bash
python -m src.cli.main config                  # 查看配置
python -m src.cli.main configure --api-url http://localhost:8000
python -m src.cli.main configure --agent-id your-uuid
```

### 記憶管理
```bash
python -m src.cli.main create "記憶內容"      # 創建記憶
python -m src.cli.main list                   # 列出記憶
python -m src.cli.main list --limit 50        # 自定義數量
python -m src.cli.main get <memory-id>        # 獲取詳情
python -m src.cli.main update <id> --content  # 更新記憶
python -m src.cli.main delete <memory-id>     # 刪除記憶
```

### 搜索功能
```bash
python -m src.cli.main search "查詢"          # 基本搜索
python -m src.cli.main search "AI" --limit 20 # 限制結果
python -m src.cli.main search "ML" --threshold 0.5  # 相似度閾值
```

### 共享與統計
```bash
python -m src.cli.main share <id> <agent-id>  # 共享記憶
python -m src.cli.main stats                  # 查看統計
python -m src.cli.main health                 # 健康檢查
```

## 配置文件

配置存儲在：`~/.agentmem/config.json`

環境變量支持：
- AGENTMEM_API_URL
- AGENTMEM_AGENT_ID
- AGENTMEM_TIMEOUT

## 常見問題

Q: 如何重置配置?
A: 刪除 ~/.agentmem/config.json

Q: 如何使用自定義 Agent ID?
A: `python -m src.cli.main configure --agent-id your-id`
