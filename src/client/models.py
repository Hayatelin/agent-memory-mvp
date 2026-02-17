"""
AgentMem 客户端数据模型
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class Memory:
    """记忆对象"""

    id: str
    content: str
    type: str
    category: str
    visibility: str
    embeddings: Optional[List[float]] = None
    embedding_model: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by_agent_id: Optional[str] = None

    def __repr__(self) -> str:
        return f"Memory(id={self.id}, type={self.type}, category={self.category})"


@dataclass
class SearchResult:
    """搜索结果对象"""

    memory_id: str
    content: str
    similarity_score: float
    type: str
    category: str
    visibility: str

    def __repr__(self) -> str:
        return f"SearchResult(memory_id={self.memory_id}, score={self.similarity_score:.2f})"


@dataclass
class SearchResponse:
    """搜索响应对象"""

    results: List[SearchResult]
    total: int
    query_embedding_time_ms: float
    search_time_ms: float

    def __repr__(self) -> str:
        return f"SearchResponse(total={self.total}, results={len(self.results)})"


@dataclass
class SearchStats:
    """搜索统计对象"""

    total_memories: int
    searchable_memories: int
    embedding_coverage: float

    def __repr__(self) -> str:
        return (
            f"SearchStats(total={self.total_memories}, "
            f"searchable={self.searchable_memories}, "
            f"coverage={self.embedding_coverage:.1%})"
        )


@dataclass
class Agent:
    """Agent 对象"""

    id: str
    name: str
    workspace_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __repr__(self) -> str:
        return f"Agent(id={self.id}, name={self.name})"
