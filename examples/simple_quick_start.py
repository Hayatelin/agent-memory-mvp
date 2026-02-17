"""
AgentMem 快速開始 - 簡潔版本

這個腳本展示如何使用 AgentMem Python 客户端庫的基本功能。
適合快速上手和理解核心概念。

運行方式:
    python examples/simple_quick_start.py
"""
from src.client import AgentMemClient


def main():
    print("=" * 60)
    print("AgentMem 快速開始")
    print("=" * 60)

    # 初始化客户端
    print("\n初始化客户端...")
    client = AgentMemClient(api_url="http://localhost:8000")
    print(f"✓ 客户端已初始化")
    print(f"  Agent ID: {client.agent_id}")

    # 檢查服務器連接
    print("\n檢查服務器連接...")
    if not client.health_check():
        print("✗ 無法連接到服務器，請確保已啟動")
        print("  啟動方式: make docker-up")
        return
    print("✓ 服務器在線")

    # 示例 1: 創建記憶
    print("\n[1] 創建記憶...")
    memory = client.create_memory(
        content="Python 是用於機器學習的最佳語言",
        type="knowledge",
        category="programming"
    )
    print(f"✓ 記憶已創建: {memory.id}")
    print(f"  內容: {memory.content[:50]}...")

    # 示例 2: 創建更多記憶用於搜索
    print("\n[2] 創建更多記憶...")
    memory2 = client.create_memory(
        content="機器學習涉及算法和統計模型的開發",
        type="knowledge",
        category="ai"
    )
    memory3 = client.create_memory(
        content="深度學習使用神經網絡進行複雜計算",
        type="knowledge",
        category="ai"
    )
    print(f"✓ 創建了 2 條新記憶")

    # 示例 3: 列出記憶
    print("\n[3] 列出所有記憶...")
    memories = client.list_memories(limit=10)
    print(f"✓ 共有 {len(memories)} 條記憶")
    for mem in memories[:3]:
        print(f"  - {mem.type}/{mem.category}: {mem.content[:40]}...")

    # 示例 4: 搜索記憶
    print("\n[4] 搜索記憶...")
    query = "機器學習"
    results = client.search(query, limit=5, similarity_threshold=0.3)
    print(f"✓ 搜索 '{query}' 找到 {len(results.results)} 條相關記憶")
    for i, result in enumerate(results.results, 1):
        score = result.similarity_score
        print(f"  {i}. [{score:.1%}] {result.content[:50]}...")

    # 示例 5: 獲取搜索統計
    print("\n[5] 獲取搜索統計...")
    stats = client.get_search_stats()
    print(f"✓ 總記憶數: {stats.total_memories}")
    print(f"✓ 可搜索記憶數: {stats.searchable_memories}")
    print(f"✓ 嵌入覆蓋率: {stats.embedding_coverage:.1%}")

    # 示例 6: 共享記憶
    print("\n[6] 共享記憶...")
    other_agent_id = "other-agent-uuid-12345"
    client.share_memory(memory.id, other_agent_id)
    print(f"✓ 已與 Agent {other_agent_id[:12]}... 共享")

    # 示例 7: 更新記憶
    print("\n[7] 更新記憶...")
    updated = client.update_memory(
        memory.id,
        content="Python 是用於機器學習的最佳語言。它有強大的庫支持。"
    )
    print(f"✓ 記憶已更新")
    print(f"  新內容: {updated.content[:50]}...")

    # 示例 8: 刪除記憶
    print("\n[8] 刪除記憶...")
    client.delete_memory(memory3.id)
    print(f"✓ 記憶已刪除")

    print("\n" + "=" * 60)
    print("✓ 快速開始完成！")
    print("=" * 60)
    print("\n接下來可以:")
    print("  - 查看 SDK 文檔: docs/SDK_GUIDE.md")
    print("  - 試用 CLI 工具: python -m src.cli.main --help")
    print("  - 閱讀完整範例: examples/quick_start.py")


if __name__ == "__main__":
    main()
