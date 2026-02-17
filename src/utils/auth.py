"""認證和授權工具"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from starlette.requests import Request
from sqlalchemy.orm import Session
from uuid import UUID
from src.db.database import get_db
from src.models.models import Agent

security = HTTPBearer()


async def get_current_agent(
    request: Request,
    db: Session = Depends(get_db)
) -> Agent:
    """驗證並獲取當前Agent

    Args:
        request: HTTP 請求
        db: 數據庫會話

    Returns:
        Agent: 當前認證的Agent

    Raises:
        HTTPException: 如果認證失敗
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效的認證令牌"
        )

    token = auth_header[7:]  # 移除 "Bearer "

    try:
        # 簡單實現：使用 token 作為 agent_id
        agent_id = UUID(token)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效的認證令牌"
        )

    agent = db.query(Agent).filter(Agent.id == agent_id).first()

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Agent 不存在"
        )

    return agent
