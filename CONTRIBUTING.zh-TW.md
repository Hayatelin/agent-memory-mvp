> **語言**: [English](CONTRIBUTING.md) | [繁體中文](CONTRIBUTING.zh-TW.md)

# 貢獻指南

感謝你對 AgentMem 項目的興趣！本文檔將幫助你開始貢獻。

## 行為準則

本項目採納了貢獻者公約。參與者應遵守以下基本原則：

- 尊重所有貢獻者
- 接受建設性批評
- 注重項目和社區的最大利益
- 展示同情心對待社區成員

## 如何貢獻

### 報告錯誤

在報告錯誤時，請：

1. 確認該錯誤尚未被報告
2. 使用描述性標題
3. 提供詳細的重現步驟
4. 說明實際行為與預期行為
5. 包含環境信息（OS、Python 版本等）

### 提議功能

在提議新功能時，請：

1. 使用描述性標題
2. 提供詳細的用途描述
3. 列出可能的實現方式
4. 說明預期的好處

### 提交改動

1. **Fork 倉庫**
   ```bash
   git clone https://github.com/your-username/agent-memory-mvp.git
   cd agent-memory-mvp
   ```

2. **創建開發分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

3. **進行改動**
   - 遵循 PEP 8 代碼風格
   - 添加類型提示
   - 編寫 docstring
   - 添加相應的測試

4. **提交代碼**
   ```bash
   git add .
   git commit -m "簡短描述改動"
   ```

5. **推送到遠程**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **創建 Pull Request**
   - 使用提供的 PR 模板
   - 清楚描述改動
   - 鏈接相關 Issue

## 開發設置

### 必要工具

- Python 3.11+
- Docker & Docker Compose
- Git

### 本地開發

1. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

2. **運行測試**
   ```bash
   pytest tests/ -v
   ```

3. **代碼質量檢查**
   ```bash
   black src tests
   isort src tests
   flake8 src tests
   mypy src
   ```

4. **啟動應用**
   ```bash
   python -m uvicorn src.main:app --reload
   ```

## 代碼風格

### Python 代碼風格

遵循 PEP 8：
- 行長度：最多 120 個字符
- 縮進：4 個空格
- 命名：snake_case for functions/variables, PascalCase for classes

### 類型提示

所有函數都應該有類型提示：

```python
async def get_embeddings(
    text: str,
    model_name: Optional[str] = None
) -> List[float]:
    """獲取文本的嵌入向量。

    Args:
        text: 輸入文本
        model_name: 模型名稱（可選）

    Returns:
        嵌入向量列表

    Raises:
        ValueError: 如果文本為空
    """
```

### Docstring

使用 Google 風格的 docstring：

```python
def function_name(param1: str, param2: int) -> bool:
    """簡短的描述。

    更詳細的描述（如果需要）。

    Args:
        param1: 參數 1 的描述
        param2: 參數 2 的描述

    Returns:
        返回值的描述

    Raises:
        ExceptionType: 異常的描述

    Example:
        >>> function_name("test", 42)
        True
    """
```

## 測試

### 編寫測試

- 使用 pytest 框架
- 一個測試文件對應一個源文件
- 命名：test_*.py 或 *_test.py
- 測試函數命名：test_*

### 運行測試

```bash
# 運行所有測試
pytest tests/ -v

# 運行特定文件
pytest tests/test_embeddings.py -v

# 運行特定測試
pytest tests/test_embeddings.py::test_embedding_service_basic -v

# 生成覆蓋率報告
pytest tests/ --cov=src --cov-report=html
```

## 提交消息

遵循以下格式：

```
[TYPE] Brief description

Detailed explanation (optional)

Related issues: #123
```

類型包括：
- **feat**: 新功能
- **fix**: 錯誤修復
- **docs**: 文檔更新
- **refactor**: 代碼重構
- **test**: 測試相關
- **perf**: 性能優化
- **chore**: 構建、依賴等

示例：
```
feat: Add support for multiple embedding models

- Add model selection parameter to EmbeddingService
- Implement model caching mechanism
- Update tests to cover new functionality

Related issues: #42
```

## Pull Request 流程

1. **本地測試**
   - 運行所有測試
   - 檢查代碼質量
   - 驗證文檔

2. **提交 PR**
   - 使用模板填寫信息
   - 清楚描述改動
   - 鏈接相關 Issue

3. **代碼審查**
   - 維護者會審查你的代碼
   - 可能會請求修改
   - 通過後會被合併

4. **合併**
   - PR 被合併到 main 分支
   - 你的名字會被添加到貢獻者列表

## 構建和部署

### 本地 Docker 構建

```bash
docker build -t agent-memory-mvp:local .
docker-compose up -d
```

### 版本發布

發布版本時：
1. 更新版本號（src/main.py）
2. 更新 CHANGELOG.md
3. 創建 git tag
4. GitHub Actions 會自動部署

## 文檔

- 更新 README.md 如果改動了用法
- 添加 docstring 到新函數
- 更新 WEEK2_UPDATES.md 如果有重要改動
- 保持文檔同步

## 許可證

通過提交代碼，你同意在 MIT 許可證下發布你的代碼。

## 問題和討論

- 使用 Issues 報告錯誤和功能請求
- 使用 Discussions 進行一般討論
- 直接聯繫維護者以獲取安全相關問題

---

感謝你的貢獻！ 🎉
