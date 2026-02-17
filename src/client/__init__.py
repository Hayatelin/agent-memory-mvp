"""
AgentMem Python 客户端库

简化的 API 接口，让用户轻松使用 AgentMem

使用示例:
    from agentmem import AgentMemClient
    
    # 初始化客户端
    client = AgentMemClient(api_url="http://localhost:8000")
    
    # 创建记忆
    memory = client.create_memory(
        content="Machine learning basics",
        type="knowledge",
        category="ai"
    )
    
    # 搜索记忆
    results = client.search("AI and ML", limit=10)
    for result in results.results:
        print(f"{result.memory_id}: {result.similarity_score:.2f}")
    
    # 共享记忆
    client.share_memory(memory.id, "other-agent-id")
"""

from .client import AgentMemClient
from .models import Memory, SearchResult, SearchResponse, SearchStats, Agent
from .exceptions import (
    AgentMemException,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    ConnectionError,
    ServerError,
)

__version__ = "0.1.0"
__all__ = [
    "AgentMemClient",
    "Memory",
    "SearchResult",
    "SearchResponse",
    "SearchStats",
    "Agent",
    "AgentMemException",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "ConnectionError",
    "ServerError",
]
