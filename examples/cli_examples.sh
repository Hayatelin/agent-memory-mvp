#!/bin/bash
# AgentMem CLI 使用示例

echo "========================================"
echo "AgentMem CLI 使用示例"
echo "========================================"

# 1. 檢查服務器健康狀態
echo -e "\n[1] 檢查服務器健康狀態..."
python -m src.cli.main health -v

# 2. 初始化 CLI
echo -e "\n[2] 初始化 CLI..."
python -m src.cli.main init

# 3. 查看配置
echo -e "\n[3] 查看配置..."
python -m src.cli.main config

# 4. 創建記憶
echo -e "\n[4] 創建記憶..."
python -m src.cli.main create "Machine learning 是人工智能的重要分支" --type knowledge --category ai

# 5. 列出記憶
echo -e "\n[5] 列出所有記憶..."
python -m src.cli.main list --limit 10

# 6. 搜索記憶
echo -e "\n[6] 搜索記憶..."
python -m src.cli.main search "人工智能" --limit 5

# 7. 查看統計
echo -e "\n[7] 查看搜索統計..."
python -m src.cli.main stats

echo -e "\n========================================"
echo "✓ 示例執行完成"
echo "========================================"
