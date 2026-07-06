"""數據庫模型"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Table, JSON, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from src.db.database import Base
from datetime import datetime
import uuid
import json
from uuid import UUID


# SQLAlchemy GUID 類型，兼容 SQLite 和 PostgreSQL
import sqlalchemy.types as types


class GUID(types.TypeDecorator):
    """使用 VARCHAR 存儲的 GUID 類型"""
    impl = types.String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.String(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            return value
        return str(value).replace('-', '')

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        return value

# 關聯表：記憶與 Agent 共享
memory_shared_agents = Table(
    'memory_shared_agents',
    Base.metadata,
    Column('memory_id', GUID, ForeignKey('memory.id')),
    Column('agent_id', GUID, ForeignKey('agent.id'))
)


class Agent(Base):
    """Agent 模型"""
    __tablename__ = "agent"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    workspace_id = Column(GUID, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    memories = relationship("Memory", back_populates="creator")


class Memory(Base):
    """記憶模型"""
    __tablename__ = "memory"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    workspace_id = Column(GUID, index=True)
    created_by_agent_id = Column(GUID, ForeignKey("agent.id"))
    type = Column(String)  # preference, knowledge, history, etc.
    category = Column(String)
    content = Column(String)
    visibility = Column(String, default="private")  # private, shared, public
    is_deleted = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 嵌入相關欄位
    embeddings = Column(JSON, nullable=True)  # 存儲為 JSON
    embedding_model = Column(String(50), default="all-MiniLM-L6-v2")
    embedding_updated_at = Column(DateTime, nullable=True)

    # 關係
    creator = relationship("Agent", back_populates="memories")
    shared_with_agents = relationship(
        "Agent",
        secondary=memory_shared_agents,
        backref="shared_memories"
    )
