"""權限管理測試"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from src.db.database import Base
from src.models.models import Agent, Memory
from src.core.permissions import PermissionManager

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def db_session():
    """創建測試數據庫會話"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_data(db_session):
    """創建測試數據"""
    workspace_id = uuid4()

    # 創建 Agents
    agent1 = Agent(id=uuid4(), name="agent1", workspace_id=workspace_id)
    agent2 = Agent(id=uuid4(), name="agent2", workspace_id=workspace_id)

    db_session.add(agent1)
    db_session.add(agent2)
    db_session.commit()

    # 創建 Memory
    memory = Memory(
        id=uuid4(),
        workspace_id=workspace_id,
        created_by_agent_id=agent1.id,
        type="knowledge",
        category="test",
        content="Test memory",
        visibility="private"
    )
    db_session.add(memory)
    db_session.commit()

    return {
        "agent1": agent1,
        "agent2": agent2,
        "memory": memory,
        "db": db_session
    }


@pytest.mark.asyncio
async def test_can_read_memory_owner(test_data):
    """所有者可以讀取記憶"""
    agent1 = test_data["agent1"]
    memory = test_data["memory"]
    db = test_data["db"]

    can_read = await PermissionManager.can_read_memory(
        agent1.id,
        memory.id,
        db
    )

    assert can_read is True


@pytest.mark.asyncio
async def test_can_read_memory_other(test_data):
    """非所有者不能讀取私有記憶"""
    agent2 = test_data["agent2"]
    memory = test_data["memory"]
    db = test_data["db"]

    can_read = await PermissionManager.can_read_memory(
        agent2.id,
        memory.id,
        db
    )

    assert can_read is False


@pytest.mark.asyncio
async def test_can_read_memory_shared(test_data):
    """共享對象可以讀取記憶"""
    agent1 = test_data["agent1"]
    agent2 = test_data["agent2"]
    memory = test_data["memory"]
    db = test_data["db"]

    # 共享記憶
    memory.shared_with_agents.append(agent2)
    db.commit()

    can_read = await PermissionManager.can_read_memory(
        agent2.id,
        memory.id,
        db
    )

    assert can_read is True


@pytest.mark.asyncio
async def test_can_read_memory_public(test_data):
    """任何人都可以讀取公開記憶"""
    agent2 = test_data["agent2"]
    memory = test_data["memory"]
    db = test_data["db"]

    # 設置為公開
    memory.visibility = "public"
    db.commit()

    can_read = await PermissionManager.can_read_memory(
        agent2.id,
        memory.id,
        db
    )

    assert can_read is True


@pytest.mark.asyncio
async def test_can_write_memory_owner(test_data):
    """所有者可以編輯記憶"""
    agent1 = test_data["agent1"]
    memory = test_data["memory"]
    db = test_data["db"]

    can_write = await PermissionManager.can_write_memory(
        agent1.id,
        memory.id,
        db
    )

    assert can_write is True


@pytest.mark.asyncio
async def test_can_write_memory_other(test_data):
    """非所有者不能編輯記憶"""
    agent2 = test_data["agent2"]
    memory = test_data["memory"]
    db = test_data["db"]

    can_write = await PermissionManager.can_write_memory(
        agent2.id,
        memory.id,
        db
    )

    assert can_write is False


@pytest.mark.asyncio
async def test_can_share_memory_owner(test_data):
    """所有者可以共享記憶"""
    agent1 = test_data["agent1"]
    memory = test_data["memory"]
    db = test_data["db"]

    can_share = await PermissionManager.can_share_memory(
        agent1.id,
        memory.id,
        db
    )

    assert can_share is True


@pytest.mark.asyncio
async def test_can_share_memory_other(test_data):
    """非所有者不能共享記憶"""
    agent2 = test_data["agent2"]
    memory = test_data["memory"]
    db = test_data["db"]

    can_share = await PermissionManager.can_share_memory(
        agent2.id,
        memory.id,
        db
    )

    assert can_share is False
