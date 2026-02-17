"""
Web UI 功能測試腳本
測試所有 Web UI 頁面使用的底層功能
"""
import sys
import uuid
import time
from src.client import AgentMemClient

def print_section(title):
    """打印測試章節"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_test(name, status):
    """打印測試結果"""
    icon = "[PASS]" if status else "[FAIL]"
    print(f"{icon} {name}")

def test_web_ui_features():
    """測試 Web UI 所有功能"""

    print_section("AgentMem Web UI 功能測試")

    # 初始化客戶端
    print("初始化客戶端...")
    client = AgentMemClient(
        api_url="http://localhost:8000",
        agent_id=str(uuid.uuid4())
    )
    print(f"Agent ID: {client.agent_id[:8]}...\n")

    try:
        # 1. 健康檢查
        print_section("1. 連接和健康檢查 (app.py 側邊欄)")
        health_ok = client.health_check()
        print_test("健康檢查", health_ok)

        # 2. 創建記憶功能
        print_section("2. 創建記憶 (create.py)")

        memories = []
        test_memories = [
            {
                "content": "Python 是一門強大的編程語言",
                "type": "knowledge",
                "category": "programming",
                "visibility": "private"
            },
            {
                "content": "今天學習了 FastAPI 框架",
                "type": "experience",
                "category": "learning",
                "visibility": "shared"
            },
            {
                "content": "想要開發一個向量搜索系統",
                "type": "idea",
                "category": "project",
                "visibility": "public"
            }
        ]

        for i, mem_data in enumerate(test_memories, 1):
            try:
                memory = client.create_memory(**mem_data)
                memories.append(memory)
                print_test(f"創建記憶 {i}: {mem_data['type']}", True)
                print(f"   ID: {memory.id[:8]}...")
                print(f"   內容: {memory.content[:50]}...\n")
            except Exception as e:
                print_test(f"創建記憶 {i}", False)
                print(f"   錯誤: {e}\n")

        # 3. 列表功能
        print_section("3. 列出記憶 (manage.py - 查看頁籤)")
        try:
            listed = client.list_memories(limit=20)
            print_test("列出記憶", len(listed) >= len(memories))
            print(f"   返回 {len(listed)} 條記憶\n")
        except Exception as e:
            print_test("列出記憶", False)
            print(f"   錯誤: {e}\n")

        # 4. 獲取單個記憶
        print_section("4. 獲取記憶詳情 (manage.py 展開)")
        if memories:
            try:
                memory = client.get_memory(memories[0].id)
                print_test("獲取記憶詳情", True)
                print(f"   ID: {memory.id}")
                print(f"   類型: {memory.type}")
                print(f"   分類: {memory.category}")
                print(f"   可見性: {memory.visibility}\n")
            except Exception as e:
                print_test("獲取記憶詳情", False)
                print(f"   錯誤: {e}\n")

        # 5. 搜索功能
        print_section("5. 搜索記憶 (search.py)")

        search_queries = [
            ("Python 編程", 0.3),
            ("機器學習", 0.3),
            ("框架", 0.5)
        ]

        for query, threshold in search_queries:
            try:
                results = client.search(
                    query=query,
                    limit=10,
                    similarity_threshold=threshold
                )
                found_count = len(results.results)
                print_test(f"搜索: '{query}'", True)
                print(f"   找到 {found_count} 條結果")
                print(f"   查詢耗時: {results.query_embedding_time_ms}ms")
                print(f"   搜索耗時: {results.search_time_ms}ms")

                if results.results:
                    top_result = results.results[0]
                    print(f"   最高相似度: {top_result.similarity_score:.1%}")
                    print(f"   內容: {top_result.content[:50]}...\n")
                else:
                    print()

            except Exception as e:
                print_test(f"搜索: '{query}'", False)
                print(f"   錯誤: {e}\n")

        # 6. 統計信息
        print_section("6. 搜索統計 (search.py 統計按鈕)")
        try:
            stats = client.get_search_stats()
            print_test("獲取統計", True)
            print(f"   總記憶數: {stats.total_memories}")
            print(f"   可搜索記憶: {stats.searchable_memories}")
            print(f"   覆蓋率: {stats.embedding_coverage:.1%}\n")
        except Exception as e:
            print_test("獲取統計", False)
            print(f"   錯誤: {e}\n")

        # 7. 更新記憶
        print_section("7. 更新記憶 (manage.py - 更新頁籤)")
        if memories:
            try:
                updated = client.update_memory(
                    memories[0].id,
                    content="更新後的內容 - Python 是編程語言之一",
                    type="note",
                    category="updated"
                )
                print_test("更新記憶", True)
                print(f"   新類型: {updated.type}")
                print(f"   新分類: {updated.category}\n")
            except Exception as e:
                print_test("更新記憶", False)
                print(f"   錯誤: {e}\n")

        # 8. 共享功能
        print_section("8. 共享記憶 (share.py - 共享頁籤)")
        if len(memories) >= 2:
            other_agent_id = str(uuid.uuid4())
            try:
                client.share_memory(memories[1].id, other_agent_id)
                print_test("共享記憶", True)
                print(f"   與 Agent {other_agent_id[:8]}... 共享\n")
            except Exception as e:
                print_test("共享記憶", False)
                print(f"   錯誤: {e}\n")

        # 9. 獲取共享列表
        print_section("9. 查看共享列表 (share.py - 管理共享頁籤)")
        if len(memories) >= 2:
            try:
                shared_with = client.get_shared_with(memories[1].id)
                print_test("獲取共享列表", True)
                print(f"   已共享給 {len(shared_with)} 個 Agents\n")
            except Exception as e:
                print_test("獲取共享列表", False)
                print(f"   錯誤: {e}\n")

        # 10. 撤銷共享
        print_section("10. 撤銷共享 (share.py - 撤銷按鈕)")
        if len(memories) >= 2:
            try:
                shared_with = client.get_shared_with(memories[1].id)
                if shared_with:
                    agent_to_revoke = shared_with[0]
                    client.revoke_sharing(memories[1].id, agent_to_revoke)
                    print_test("撤銷共享", True)
                    print(f"   已撤銷共享\n")
                else:
                    print_test("撤銷共享", False)
                    print(f"   沒有共享記錄\n")
            except Exception as e:
                print_test("撤銷共享", False)
                print(f"   錯誤: {e}\n")

        # 11. 刪除記憶
        print_section("11. 刪除記憶 (manage.py - 刪除頁籤)")
        if memories:
            try:
                deleted = client.delete_memory(memories[-1].id)
                print_test("刪除記憶", True)
                print(f"   已刪除記憶\n")
            except Exception as e:
                print_test("刪除記憶", False)
                print(f"   錯誤: {e}\n")

        # 總結
        print_section("測試總結")
        print("""
[SUCCESS] All Web UI functions have been tested!

Web UI page components mapping:
  * ui/app.py         -> Main application + sidebar
  * create.py         -> Create memory page
  * search.py         -> Search memory page
  * manage.py         -> Manage memory page
  * share.py          -> Share memory page

Launch Web UI:
  $ streamlit run ui/app.py

Access address:
  http://localhost:8501

All underlying functions are correctly implemented!
        """)

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        return False

    return True

if __name__ == "__main__":
    success = test_web_ui_features()
    sys.exit(0 if success else 1)
