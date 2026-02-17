"""
AgentMem Python 客户端库

简化的 API 接口，让用户轻松使用 AgentMem
"""
import requests
import uuid
from typing import List, Optional, Dict, Any
from .models import Memory, SearchResult, SearchResponse, SearchStats
from .exceptions import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
    ConnectionError,
    ServerError,
)


class AgentMemClient:
    """AgentMem 客户端主类"""

    def __init__(
        self,
        api_url: str = "http://localhost:8000",
        agent_id: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        初始化客户端

        参数:
            api_url: API 服务器地址 (默认: http://localhost:8000)
            agent_id: Agent ID (如果为空，则自动生成)
            timeout: 请求超时时间（秒）
        """
        self.api_url = api_url.rstrip("/")
        self.agent_id = agent_id or str(uuid.uuid4())
        self.timeout = timeout
        self.session = requests.Session()
        self._setup_auth()

    def _setup_auth(self) -> None:
        """设置认证信息"""
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.agent_id}",
                "Content-Type": "application/json",
            }
        )

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """处理 API 响应"""
        if response.status_code == 401:
            raise AuthenticationError("认证失败，请检查 Agent ID")
        elif response.status_code == 404:
            raise NotFoundError("请求的资源不存在")
        elif response.status_code == 400:
            raise ValidationError(f"数据验证失败: {response.text}")
        elif response.status_code >= 500:
            raise ServerError(f"服务器错误: {response.status_code}")
        elif response.status_code >= 400:
            raise ConnectionError(f"请求失败: {response.status_code}")

        return response.json()

    def _request(
        self, method: str, endpoint: str, **kwargs
    ) -> Dict[str, Any]:
        """发送 HTTP 请求的通用方法"""
        url = f"{self.api_url}{endpoint}"
        try:
            response = self.session.request(
                method, url, timeout=self.timeout, **kwargs
            )
            return self._handle_response(response)
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"无法连接到服务器: {e}")
        except requests.exceptions.Timeout as e:
            raise ConnectionError(f"请求超时: {e}")

    def create_memory(
        self,
        content: str,
        type: str = "knowledge",
        category: str = "general",
        visibility: str = "private",
    ) -> Memory:
        """
        创建一条新记忆

        参数:
            content: 记忆内容
            type: 记忆类型 (默认: knowledge)
            category: 记忆分类 (默认: general)
            visibility: 可见性 (private/shared/public，默认: private)

        返回:
            Memory 对象
        """
        payload = {
            "content": content,
            "type": type,
            "category": category,
            "visibility": visibility,
        }
        response = self._request("POST", "/memories", json=payload)
        return Memory(**response)

    def get_memory(self, memory_id: str) -> Memory:
        """
        获取记忆详情

        参数:
            memory_id: 记忆 ID

        返回:
            Memory 对象
        """
        response = self._request("GET", f"/memories/{memory_id}")
        return Memory(**response)

    def list_memories(self, limit: int = 100, offset: int = 0) -> List[Memory]:
        """
        列出所有记忆

        参数:
            limit: 返回数量限制
            offset: 偏移量

        返回:
            Memory 对象列表
        """
        response = self._request(
            "GET", "/memories", params={"limit": limit, "offset": offset}
        )
        return [Memory(**item) for item in response.get("memories", [])]

    def update_memory(
        self,
        memory_id: str,
        content: Optional[str] = None,
        type: Optional[str] = None,
        category: Optional[str] = None,
        visibility: Optional[str] = None,
    ) -> Memory:
        """
        更新记忆

        参数:
            memory_id: 记忆 ID
            content: 新内容
            type: 新类型
            category: 新分类
            visibility: 新可见性

        返回:
            更新后的 Memory 对象
        """
        payload = {}
        if content is not None:
            payload["content"] = content
        if type is not None:
            payload["type"] = type
        if category is not None:
            payload["category"] = category
        if visibility is not None:
            payload["visibility"] = visibility

        response = self._request(
            "PUT", f"/memories/{memory_id}", json=payload
        )
        return Memory(**response)

    def delete_memory(self, memory_id: str) -> bool:
        """
        删除记忆

        参数:
            memory_id: 记忆 ID

        返回:
            成功返回 True
        """
        self._request("DELETE", f"/memories/{memory_id}")
        return True

    def search(
        self,
        query: str,
        limit: int = 10,
        similarity_threshold: float = 0.3,
    ) -> SearchResponse:
        """
        搜索记忆

        参数:
            query: 搜索查询
            limit: 返回结果数量
            similarity_threshold: 相似度阈值

        返回:
            SearchResponse 对象，包含搜索结果
        """
        payload = {
            "query": query,
            "limit": limit,
            "similarity_threshold": similarity_threshold,
        }
        response = self._request("POST", "/memories/search", json=payload)

        results = [
            SearchResult(
                memory_id=item["memory_id"],
                content=item["content"],
                similarity_score=item["similarity_score"],
                type=item.get("type", "unknown"),
                category=item.get("category", "unknown"),
                visibility=item.get("visibility", "private"),
            )
            for item in response.get("results", [])
        ]

        return SearchResponse(
            results=results,
            total=response.get("total", 0),
            query_embedding_time_ms=response.get("query_embedding_time_ms", 0),
            search_time_ms=response.get("search_time_ms", 0),
        )

    def get_search_stats(self) -> SearchStats:
        """
        获取搜索统计信息

        返回:
            SearchStats 对象
        """
        response = self._request("GET", "/memories/search/stats")
        return SearchStats(**response)

    def share_memory(self, memory_id: str, agent_id: str) -> bool:
        """
        与另一个 Agent 共享记忆

        参数:
            memory_id: 记忆 ID
            agent_id: 目标 Agent ID

        返回:
            成功返回 True
        """
        payload = {"agent_id": agent_id}
        self._request("POST", f"/memories/{memory_id}/share", json=payload)
        return True

    def get_shared_with(self, memory_id: str) -> List[str]:
        """
        获取共享列表

        参数:
            memory_id: 记忆 ID

        返回:
            共享给的 Agent ID 列表
        """
        response = self._request("GET", f"/memories/{memory_id}/shared-with")
        return response.get("shared_with_agents", [])

    def revoke_sharing(self, memory_id: str, agent_id: str) -> bool:
        """
        撤销共享

        参数:
            memory_id: 记忆 ID
            agent_id: 目标 Agent ID

        返回:
            成功返回 True
        """
        self._request(
            "DELETE", f"/memories/{memory_id}/share/{agent_id}"
        )
        return True

    def health_check(self) -> bool:
        """
        检查服务器健康状态

        返回:
            服务器在线返回 True
        """
        try:
            response = self._request("GET", "/health")
            return response.get("status") == "healthy"
        except Exception:
            return False

    def __repr__(self) -> str:
        return (
            f"AgentMemClient("
            f"api_url={self.api_url}, "
            f"agent_id={self.agent_id})"
        )
