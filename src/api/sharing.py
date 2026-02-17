"""共享管理 API"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
from src.utils.auth import get_current_agent
from src.db.database import get_db
from src.models.models import Memory, Agent

router = APIRouter(prefix="/memories", tags=["sharing"])


class ShareRequest(BaseModel):
    """共享請求"""
    agent_id: UUID


@router.post("/{memory_id}/share")
async def share_memory(
    memory_id: UUID,
    request: ShareRequest,
    current_agent: Agent = Depends(get_current_agent),
    db: Session = Depends(get_db)
):
    """與另一個 Agent 共享記憶"""
    memory = db.query(Memory).filter(Memory.id == memory_id).first()

    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    if memory.created_by_agent_id != current_agent.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    target_agent = db.query(Agent).filter(Agent.id == request.agent_id).first()
    if not target_agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if target_agent not in memory.shared_with_agents:
        memory.shared_with_agents.append(target_agent)
        db.commit()

    return {"success": True, "memory_id": str(memory_id)}


@router.get("/{memory_id}/shared-with")
async def get_shared_with(
    memory_id: UUID,
    current_agent: Agent = Depends(get_current_agent),
    db: Session = Depends(get_db)
):
    """查詢一個記憶與誰共享"""
    memory = db.query(Memory).filter(Memory.id == memory_id).first()

    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    return {
        "memory_id": str(memory_id),
        "shared_with": [str(agent.id) for agent in memory.shared_with_agents]
    }


@router.delete("/{memory_id}/share/{agent_id}")
async def revoke_sharing(
    memory_id: UUID,
    agent_id: UUID,
    current_agent: Agent = Depends(get_current_agent),
    db: Session = Depends(get_db)
):
    """撤銷與某個 Agent 的共享"""
    memory = db.query(Memory).filter(Memory.id == memory_id).first()

    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")

    if memory.created_by_agent_id != current_agent.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    target_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if target_agent in memory.shared_with_agents:
        memory.shared_with_agents.remove(target_agent)
        db.commit()

    return {"success": True}
