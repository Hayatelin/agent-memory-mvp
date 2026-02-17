# AgentMem 範例

本目錄包含 AgentMem 的各種使用範例，幫助你快速上手。

## 快速開始腳本

### 1. 簡潔版 (推薦新手)

**文件**: `simple_quick_start.py`

適合初次使用者快速了解基本功能。

```bash
python examples/simple_quick_start.py
```

**展示功能**:
- 初始化客户端
- 檢查服務器連接
- 創建記憶
- 列出記憶
- 搜索記憶
- 獲取統計
- 共享記憶
- 更新記憶
- 刪除記憶

**預期輸出**:
```
============================================================
AgentMem 快速開始
============================================================

初始化客户端...
✓ 客户端已初始化
  Agent ID: 550e8400-e29b-41d4-a716-446655440000

檢查服務器連接...
✓ 服務器在線

[1] 創建記憶...
✓ 記憶已創建: 123e4567-e89b-12d3-a456-426614174000
...
```

### 2. 詳細版 (功能全面)

**文件**: `quick_start.py`

包含更詳細的演示和錯誤處理。

```bash
python examples/quick_start.py
```

**額外功能**:
- 詳細的進度報告
- 完整的錯誤處理
- 多條記憶的創建
- 共享和撤銷共享
- 搜索統計分析

## CLI 範例

### 使用命令行工具

**文件**: `cli_examples.sh`

展示如何使用 CLI 工具進行各項操作。

```bash
bash examples/cli_examples.sh
```

**包含的命令**:
- 健康檢查
- 初始化 CLI
- 查看配置
- 創建記憶
- 列出記憶
- 搜索記憶
- 查看統計

## 前置要求

1. **啟動服務器**
   ```bash
   make docker-up
   ```

2. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

3. **確保 Python 版本**
   ```bash
   python --version  # 需要 3.11+
   ```

## 運行順序建議

### 對於新手

1. 先啟動服務器
   ```bash
   make docker-up
   ```

2. 運行簡潔版快速開始
   ```bash
   python examples/simple_quick_start.py
   ```

3. 根據輸出了解基本功能

4. 嘗試 CLI 工具
   ```bash
   python -m src.cli.main --help
   ```

### 對於開發者

1. 查看 SDK 文檔
   ```
   docs/SDK_GUIDE.md
   ```

2. 運行完整版快速開始
   ```bash
   python examples/quick_start.py
   ```

3. 在自己的項目中集成 SDK
   ```python
   from src.client import AgentMemClient
   
   client = AgentMemClient()
   # 開始使用
   ```

## 常見問題

### Q: 無法連接到服務器？
A: 確保已運行 `make docker-up` 啟動服務器。

### Q: 導入錯誤？
A: 確保你在項目根目錄運行腳本。

### Q: 想要看更多範例？
A: 查看 `docs/SDK_GUIDE.md` 的高級用法部分。

## 下一步

- 📖 [SDK 完整文檔](../docs/SDK_GUIDE.md)
- 📋 [CLI 完整文檔](../docs/CLI_GUIDE.md)
- 🔧 [貢獻指南](../CONTRIBUTING.md)
- 📝 [API 參考](../README.md#api-端點)

---

祝你使用愉快！有任何問題，歡迎提交 Issue。
