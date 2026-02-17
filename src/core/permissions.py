"""權限管理系統"""

from sqlalchemy.orm import Session
from uuid import UUID
from src.models.models import Memory, Agent


class PermissionManager:
    """管理記憶的存取權限"""

    @staticmethod
    async def can_read_memory(
        agent_id: UUID,
        memory_id: UUID,
        db: Session
    ) -> bool:
        """檢查 Agent 是否可以讀取記憶

        Args:
            agent_id: Agent ID
            memory_id: Memory ID
            db: 數據庫會話

        Returns:
            bool: 是否有讀取權限
        """
        memory = db.query(Memory).filter(Memory.id == memory_id).first()

        if not memory:
            return False

        # 所有者可以讀
        if memory.created_by_agent_id == agent_id:
            return True

        # 共享對象可以讀
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if agent and agent in memory.shared_with_agents:
            return True

        # 公開記憶可以讀
        if memory.visibility == "public":
            return True

        return False

    @staticmethod
    async def can_write_memory(
        agent_id: UUID,
        memory_id: UUID,
        db: Session
    ) -> bool:
        """檢查 Agent 是否可以編輯記憶

        Args:
            agent_id: Agent ID
            memory_id: Memory ID
            db: 數據庫會話

        Returns:
            bool: 是否有編輯權限
        """
        memory = db.query(Memory).filter(Memory.id == memory_id).first()

        if not memory:
            return False

        # 只有所有者可以寫
        return memory.created_by_agent_id == agent_id

    @staticmethod
    async def can_share_memory(
        agent_id: UUID,
        memory_id: UUID,
        db: Session
    ) -> bool:
        """檢查 Agent 是否可以共享記憶

        Args:
            agent_id: Agent ID
            memory_id: Memory ID
            db: 數據庫會話

        Returns:
            bool: 是否有共享權限
        """
        memory = db.query(Memory).filter(Memory.id == memory_id).first()

        if not memory:
            return False

        # 只有所有者可以共享
        return memory.created_by_agent_id == agent_id
