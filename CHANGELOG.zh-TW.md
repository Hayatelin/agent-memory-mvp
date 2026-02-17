> **語言**: [English](CHANGELOG.md) | [繁體中文](CHANGELOG.zh-TW.md)

# Changelog

所有本項目的重要改動都會被記錄在此文件中。

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-TW/) 規則，
版本號遵循 [Semantic Versioning](https://semver.org/lang/zh-TW/)。

## [0.2.0] - 2026-02-17

### 新增 (Added)

- **向量嵌入系統**
  - EmbeddingService 支持本地模型和 OpenAI API
  - 批量嵌入處理功能
  - 自動嵌入驗證和規範化
  - 嵌入工具函數（embedding.py）

- **語義搜索引擎**
  - SearchService 實現語義搜索
  - 余弦相似度計算
  - 相似度閾值過濾
  - 搜索結果排序

- **記憶管理 API**
  - POST /memories - 創建記憶
  - GET /memories - 列表查詢
  - GET /memories/{id} - 詳情查詢
  - PUT /memories/{id} - 更新記憶
  - DELETE /memories/{id} - 刪除記憶

- **搜索 API**
  - POST /memories/search - 語義搜索
  - GET /memories/search/stats - 搜索統計

- **共享管理 API**
  - POST /memories/{id}/share - 共享記憶
  - GET /memories/{id}/shared-with - 查詢共享
  - DELETE /memories/{id}/share/{agent_id} - 撤銷共享

- **權限管理系統**
  - PermissionManager 細粒度權限控制
  - 讀取、編輯、共享權限驗證
  - 訪問控制列表（ACL）支持
  - 記憶可見性級別（private/shared/public）

- **認證系統**
  - Bearer Token 認證
  - Agent 身份驗證
  - 請求級別授權驗證

- **測試套件**
  - 嵌入服務測試 (7 個測試)
  - 搜索服務測試 (6 個測試)
  - 權限管理測試 (8 個測試)
  - 端到端集成測試 (4 個測試)
  - 性能基準測試 (5 個測試)

- **文檔**
  - 完整的 README.md
  - 功能更新指南 (WEEK2_UPDATES.md)
  - 整合報告 (INTEGRATION_REPORT.md)
  - 貢獻指南 (CONTRIBUTING.md)

- **開發工具**
  - Docker & Docker Compose 配置
  - GitHub Actions CI/CD 工作流
  - Pytest 測試框架配置
  - Git 工作流配置

### 改動 (Changed)

- 數據庫模型添加嵌入相關欄位
  - embeddings: JSON 字段存儲向量
  - embedding_model: 使用的模型名稱
  - embedding_updated_at: 最後更新時間

- 應用程序版本更新到 0.2.0

### 固定 (Fixed)

- 修復 UUID 類型在 SQLite 中的兼容性問題
- 修復 Windows 平台的 CRLF 行尾問題

### 已知問題 (Known Issues)

- 嵌入存儲使用 JSON 格式（未來計劃升級至向量數據庫）
- 認證使用簡單 UUID Token（未來計劃升級至 JWT）
- 無內置緩存層（可選集成 Redis）

## [0.1.0] - 未發布

初始項目設置和規劃。

---

## 版本發布流程

### 語義版本控制

- MAJOR 版本：不兼容的 API 改動
- MINOR 版本：向後兼容的新功能
- PATCH 版本：向後兼容的錯誤修復

### 發布檢查清單

在發布新版本前：

- [ ] 所有測試通過
- [ ] 代碼覆蓋率 >85%
- [ ] 文檔更新完成
- [ ] CHANGELOG.md 已更新
- [ ] README.md 已更新（如需要）
- [ ] 版本號已更新（src/main.py）
- [ ] 創建 git tag
- [ ] 更新 GitHub Release

### 發布命令

```bash
# 1. 更新版本號
# 編輯 src/main.py 中的 version="x.y.z"

# 2. 更新 CHANGELOG.md
# 添加新版本信息

# 3. 提交改動
git add CHANGELOG.md src/main.py
git commit -m "chore: Bump version to x.y.z"

# 4. 創建 tag
git tag -a vx.y.z -m "Release version x.y.z"

# 5. 推送
git push origin main
git push origin vx.y.z

# 6. GitHub 會自動執行部署
```

---

## 貢獻者

感謝以下人員對本項目的貢獻：

- Claude Code (claude@anthropic.com) - 初始開發

---

## 許可證

本項目使用 MIT 許可證。詳見 LICENSE 文件。
