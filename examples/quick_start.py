"""
AgentMem Python SDK 快速開始

這個腳本展示如何使用 AgentMem Python 客户端庫
"""
import sys
import uuid
sys.path.insert(0, "../")

from src.client import AgentMemClient


def main():
    print("=" * 60)
    print("AgentMem Python SDK 快速開始")
    print("=" * 60)

    # 初始化客户端
    # 如果没有传入 agent_id，会自动生成一个 UUID
    client = AgentMemClient(
        api_url="http://localhost:8000",
        agent_id=str(uuid.uuid4())
    )
    print(f"\n✓ 客户端已初始化")
    print(f"  Agent ID: {client.agent_id}")
    print(f"  API URL: {client.api_url}")

    # 检查服务器健康状态
    print(f"\n[1] 检查服务器状态...")
    if client.health_check():
        print("✓ 服务器在线")
    else:
        print("✗ 无法连接到服务器，请确保服务器已启动")
        return

    # 创建记忆
    print(f"\n[2] 创建记忆...")
    try:
        memory1 = client.create_memory(
            content="Machine learning 是人工智能的重要分支，涉及算法和统计模型",
            type="knowledge",
            category="ai",
            visibility="private"
        )
        print(f"✓ 记忆已创建")
        print(f"  ID: {memory1.id}")
        print(f"  类型: {memory1.type}")
        print(f"  分类: {memory1.category}")
    except Exception as e:
        print(f"✗ 创建失败: {e}")
        return

    # 创建更多记忆用于演示
    print(f"\n[3] 创建更多记忆...")
    memory2 = client.create_memory(
        content="深度学习使用神经网络来处理大规模数据",
        type="knowledge",
        category="ai"
    )
    memory3 = client.create_memory(
        content="Python 是数据科学和机器学习的首选编程语言",
        type="knowledge",
        category="programming"
    )
    print(f"✓ 创建了 2 条新记忆")

    # 列出所有记忆
    print(f"\n[4] 列出所有记忆...")
    memories = client.list_memories(limit=10)
    print(f"✓ 共有 {len(memories)} 条记忆")
    for mem in memories[:3]:
        print(f"  - {mem.type}/{mem.category}: {mem.content[:40]}...")

    # 搜索记忆
    print(f"\n[5] 语义搜索...")
    query = "人工智能和机器学习"
    results = client.search(query, limit=5, similarity_threshold=0.3)
    print(f"✓ 搜索查询: '{query}'")
    print(f"✓ 找到 {len(results.results)} 条相关记忆")
    for i, result in enumerate(results.results, 1):
        print(f"  {i}. [相似度: {result.similarity_score:.2%}] {result.content[:50]}...")

    # 获取搜索统计
    print(f"\n[6] 搜索统计...")
    stats = client.get_search_stats()
    print(f"✓ 总记忆数: {stats.total_memories}")
    print(f"✓ 可搜索记忆数: {stats.searchable_memories}")
    print(f"✓ 嵌入覆盖率: {stats.embedding_coverage:.1%}")

    # 更新记忆
    print(f"\n[7] 更新记忆...")
    updated = client.update_memory(
        memory1.id,
        content="Machine learning 是人工智能的重要分支，涉及算法和统计模型。它是深度学习的基础。"
    )
    print(f"✓ 记忆已更新")
    print(f"  内容: {updated.content[:60]}...")

    # 共享记忆
    print(f"\n[8] 共享记忆...")
    other_agent_id = str(uuid.uuid4())
    client.share_memory(memory1.id, other_agent_id)
    print(f"✓ 已与 Agent {other_agent_id[:8]}... 共享")

    # 获取共享列表
    print(f"\n[9] 获取共享列表...")
    shared_with = client.get_shared_with(memory1.id)
    print(f"✓ 共享给 {len(shared_with)} 个 Agent")
    for agent_id in shared_with:
        print(f"  - {agent_id}")

    # 撤销共享
    print(f"\n[10] 撤销共享...")
    client.revoke_sharing(memory1.id, other_agent_id)
    print(f"✓ 已撤销共享")

    # 删除记忆
    print(f"\n[11] 删除记忆...")
    client.delete_memory(memory3.id)
    print(f"✓ 记忆已删除")

    print("\n" + "=" * 60)
    print("✓ 快速開始示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
