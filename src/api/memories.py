"""記憶 API 路由"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from src.utils.auth import get_current_agent
from src.services.embedding_service import EmbeddingService
from src.db.database import get_db
from src.models.models import Memory, Agent

router = APIRouter(prefix="/memories", tags=["memories"])


class MemoryCreate(BaseModel):
    """創建記憶的請求"""
    type: str
    category: str
    content: str
    visibility: str = "private"


class MemoryUpdate(BaseModel):
    """更新記憶的請求"""
    content: str
    visibility: str = None


class MemoryResponse(BaseModel):
    """記憶響應"""
    id: str
    type: str
    category: str
    content: str
    visibility: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


@router.post("", status_code=201)
async def create_memory(
    memory_data: MemoryCreate,
    current_agent: Agent = Depends(get_current_agent),
    db: Session = Depends(get_db)
) -> MemoryResponse:
    """創建新記憶"""
    memory = Memory(
        workspace_id=current_agent.workspace_id,
        created_by_agent_id=current_agent.id,
        type=memory_data.type,
        category=memory_data.category,
        content=memory_data.content,
        visibility=memory_data.visibility
    )

    # 生成嵌入
    try:
        embedding_service = EmbeddingService()
        embeddings = await embedding_service.get_embeddings(memory_data.content)
        memory.embeddings = embeddings
        memory.embedding_updated_at = datetime.utcnow()
    except Exception as e:
        # 如果嵌入失敗，仍然創建記憶但不設置嵌入
        pass

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return MemoryResponse.model_validate(memory)


@router.get("/{memory_id}")
async def get_memory(
    memory_id: UUID,
    current_agent: Agent = Depends(get_current_agent),
    db: Session = Depends(get_db)
) -> MemoryResponse:
    """獲取記憶"""
    memory = db.query(Memory).filter(Memory.id == memory_id).first()

    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    # 檢查讀取權限
    if (memory.created_by_agent_id != current_agent.id and
            current_agent not in memory.shared_with_agents and
            memory.visibility != "public"):
        raise HTTPException(status_code=403, detail="Not authorized")

    return MemoryResponse.model_validate(memory)


@router.put("/{memory_id}")
async def update_memory(
    memory_id: UUID,
    memory_data: MemoryUpdate,
    current_agent: Agent = Depends(get_current_agent),
    db: Session = Depends(get_db)
) -> MemoryResponse:
    """更新記憶"""
    memory = db.query(Memory).filter(Memory.id == memory_id).first()

    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    if memory.created_by_agent_id != current_agent.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    memory.content = memory_data.content
    if memory_data.visibility:
        memory.visibility = memory_data.visibility

    # 更新嵌入
    try:
        embedding_service = EmbeddingService()
        embeddings = await embedding_service.get_embeddings(memory_data.content)
        memory.embeddings = embeddings
        memory.embedding_updated_at = datetime.utcnow()
    except Exception as e:
        pass

    db.commit()
    db.refresh(memory)

    return MemoryResponse.model_validate(memory)


@router.delete("/{memory_id}")
async def delete_memory(
    memory_id: UUID,
    current_agent: Agent = Depends(get_current_agent),
    db: Session = Depends(get_db)
):
    """刪除記憶"""
    memory = db.query(Memory).filter(Memory.id == memory_id).first()

    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    if memory.created_by_agent_id != current_agent.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    memory.is_deleted = True
    db.commit()

    return {"success": True}


@router.get("")
async def list_memories(
    current_agent: Agent = Depends(get_current_agent),
    db: Session = Depends(get_db)
):
    """列出記憶"""
    memories = db.query(Memory).filter(
        Memory.workspace_id == current_agent.workspace_id,
        Memory.is_deleted == False
    ).all()

    return {
        "memories": [MemoryResponse.model_validate(m) for m in memories],
        "total": len(memories)
    }
