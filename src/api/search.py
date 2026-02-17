"""搜索 API 路由"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
from src.utils.auth import get_current_agent
from src.services.search_service import SearchService
from src.services.embedding_service import EmbeddingService
from src.db.database import get_db
from src.models.models import Memory, Agent

router = APIRouter(prefix="/memories", tags=["search"])


class SearchRequest(BaseModel):
    """搜索請求"""
    query: str
    limit: int = 10
    offset: int = 0
    similarity_threshold: float = 0.3


@router.post("/search")
async def search_memories(
    request: SearchRequest,
    current_agent: Agent = Depends(get_current_agent),
    db: Session = Depends(get_db)
):
    """進行語義搜索

    邏輯：
        1. 驗證查詢合法性
        2. 獲取當前 Agent 可訪問的所有記憶
        3. 使用 SearchService 進行語義搜索
        4. 返回排序結果
    """
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="查詢不能為空")

    try:
        # 獲取所有可訪問的記憶
        accessible_memories = db.query(Memory).filter(
            Memory.workspace_id == current_agent.workspace_id,
            Memory.is_deleted == False
        ).all()

        embedding_service = EmbeddingService()
        search_service = SearchService(embedding_service)
        results = await search_service.semantic_search(
            request.query,
            accessible_memories,
            top_k=request.limit,
            similarity_threshold=request.similarity_threshold
        )

        return {
            "results": [
                {
                    "memory_id": str(r[0].id),
                    "content": r[0].content,
                    "relevance_score": r[1],
                    "type": r[0].type,
                    "category": r[0].category
                }
                for r in results
            ],
            "total": len(results),
            "limit": request.limit,
            "offset": request.offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/stats")
async def search_stats(
    current_agent: Agent = Depends(get_current_agent),
    db: Session = Depends(get_db)
):
    """獲取搜索統計信息"""
    total_memories = db.query(Memory).filter(
        Memory.workspace_id == current_agent.workspace_id,
        Memory.is_deleted == False
    ).count()

    memories_with_embeddings = db.query(Memory).filter(
        Memory.workspace_id == current_agent.workspace_id,
        Memory.is_deleted == False,
        Memory.embeddings != None
    ).count()

    return {
        "total_memories": total_memories,
        "searchable_memories": memories_with_embeddings,
        "embedding_coverage": (
            memories_with_embeddings / total_memories
            if total_memories > 0 else 0.0
        )
    }
