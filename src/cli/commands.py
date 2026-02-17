"""
CLI 命令實現
"""
from typing import Optional
from src.client import AgentMemClient
from .config import Config
from .formatter import (
    print_success,
    print_error,
    print_info,
    print_table,
    print_json,
    print_memory,
    print_search_results,
)


class Commands:
    """CLI 命令類"""

    def __init__(self, config: Config):
        self.config = config
        self.client = self._create_client()

    def _create_client(self) -> AgentMemClient:
        """創建客戶端"""
        api_url = self.config.get("api_url")
        agent_id = self.config.get("agent_id")
        timeout = self.config.get("timeout", 30)

        if not agent_id:
            import uuid
            agent_id = str(uuid.uuid4())
            self.config.set("agent_id", agent_id)
            print_info(f"已生成 Agent ID: {agent_id}")

        return AgentMemClient(
            api_url=api_url,
            agent_id=agent_id,
            timeout=timeout,
        )

    def health_check(self, verbose: bool = False) -> bool:
        """檢查服務器健康狀態"""
        try:
            is_healthy = self.client.health_check()
            if is_healthy:
                print_success(f"服務器在線: {self.config.get('api_url')}")
                if verbose:
                    print_info(f"Agent ID: {self.client.agent_id}")
                return True
            else:
                print_error("服務器無法連接")
                return False
        except Exception as e:
            print_error(f"連接失敗: {e}")
            return False

    def create_memory(
        self,
        content: str,
        type: str = "knowledge",
        category: str = "general",
        visibility: str = "private",
        output_json: bool = False,
    ) -> bool:
        """創建記憶"""
        try:
            memory = self.client.create_memory(
                content=content,
                type=type,
                category=category,
                visibility=visibility,
            )
            if output_json:
                print_json(vars(memory))
            else:
                print_success(f"記憶已創建")
                print_info(f"ID: {memory.id}")
                print_info(f"類型: {memory.type}, 分類: {memory.category}")
            return True
        except Exception as e:
            print_error(f"創建失敗: {e}")
            return False

    def list_memories(self, limit: int = 20, output_json: bool = False) -> bool:
        """列出記憶"""
        try:
            memories = self.client.list_memories(limit=limit)
            if output_json:
                print_json([vars(m) for m in memories])
            else:
                data = [
                    {
                        "ID": m.id[:8] + "...",
                        "類型": m.type,
                        "分類": m.category,
                        "可見性": m.visibility,
                        "內容": m.content[:50] + "...",
                    }
                    for m in memories
                ]
                print_table(data, title=f"記憶列表 ({len(memories)} 條)")
            return True
        except Exception as e:
            print_error(f"列表失敗: {e}")
            return False

    def get_memory(self, memory_id: str, output_json: bool = False) -> bool:
        """獲取記憶詳情"""
        try:
            memory = self.client.get_memory(memory_id)
            if output_json:
                print_json(vars(memory))
            else:
                print_memory(vars(memory))
            return True
        except Exception as e:
            print_error(f"獲取失敗: {e}")
            return False

    def search_memories(
        self,
        query: str,
        limit: int = 10,
        similarity_threshold: float = 0.3,
        output_json: bool = False,
    ) -> bool:
        """搜索記憶"""
        try:
            results = self.client.search(
                query=query,
                limit=limit,
                similarity_threshold=similarity_threshold,
            )
            if output_json:
                print_json(
                    {
                        "results": [vars(r) for r in results.results],
                        "total": results.total,
                        "query_embedding_time_ms": results.query_embedding_time_ms,
                        "search_time_ms": results.search_time_ms,
                    }
                )
            else:
                print_search_results(
                    {
                        "results": [vars(r) for r in results.results],
                        "total": results.total,
                        "query_embedding_time_ms": results.query_embedding_time_ms,
                        "search_time_ms": results.search_time_ms,
                    }
                )
            return True
        except Exception as e:
            print_error(f"搜索失敗: {e}")
            return False

    def delete_memory(self, memory_id: str) -> bool:
        """刪除記憶"""
        try:
            self.client.delete_memory(memory_id)
            print_success(f"記憶已刪除: {memory_id[:8]}...")
            return True
        except Exception as e:
            print_error(f"刪除失敗: {e}")
            return False

    def update_memory(
        self,
        memory_id: str,
        content: Optional[str] = None,
        type: Optional[str] = None,
        category: Optional[str] = None,
        visibility: Optional[str] = None,
        output_json: bool = False,
    ) -> bool:
        """更新記憶"""
        try:
            memory = self.client.update_memory(
                memory_id=memory_id,
                content=content,
                type=type,
                category=category,
                visibility=visibility,
            )
            if output_json:
                print_json(vars(memory))
            else:
                print_success(f"記憶已更新")
                print_info(f"ID: {memory.id}")
            return True
        except Exception as e:
            print_error(f"更新失敗: {e}")
            return False

    def share_memory(self, memory_id: str, agent_id: str) -> bool:
        """共享記憶"""
        try:
            self.client.share_memory(memory_id, agent_id)
            print_success(f"已共享記憶給 Agent: {agent_id[:8]}...")
            return True
        except Exception as e:
            print_error(f"共享失敗: {e}")
            return False

    def get_stats(self, output_json: bool = False) -> bool:
        """獲取搜索統計"""
        try:
            stats = self.client.get_search_stats()
            if output_json:
                print_json(vars(stats))
            else:
                data = [
                    {
                        "指標": "總記憶數",
                        "值": str(stats.total_memories),
                    },
                    {
                        "指標": "可搜索記憶數",
                        "值": str(stats.searchable_memories),
                    },
                    {
                        "指標": "嵌入覆蓋率",
                        "值": f"{stats.embedding_coverage:.1%}",
                    },
                ]
                print_table(data, title="搜索統計")
            return True
        except Exception as e:
            print_error(f"獲取統計失敗: {e}")
            return False
