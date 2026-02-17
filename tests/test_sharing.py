"""共享功能測試"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from src.main import app
from src.db.database import Base, get_db
from src.models.models import Agent, Memory

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def test_agents():
    """創建測試 Agents"""
    db = TestingSessionLocal()
    workspace_id = uuid4()

    agent1 = Agent(id=uuid4(), name="agent1", workspace_id=workspace_id)
    agent2 = Agent(id=uuid4(), name="agent2", workspace_id=workspace_id)

    db.add(agent1)
    db.add(agent2)
    db.commit()

    agent1_id = agent1.id
    agent2_id = agent2.id

    db.close()

    return str(agent1_id), str(agent2_id)


@pytest.fixture
def test_memory_and_agents(test_agents):
    """創建測試記憶和 Agents"""
    agent1_token, agent2_token = test_agents
    db = TestingSessionLocal()

    from uuid import UUID as UUIDType
    agent1_id = UUIDType(agent1_token)
    memory = Memory(
        id=uuid4(),
        workspace_id=uuid4(),
        created_by_agent_id=agent1_id,
        type="knowledge",
        category="test",
        content="Test memory",
        visibility="private"
    )
    db.add(memory)
    db.commit()

    memory_id = memory.id

    db.close()

    return str(memory_id), agent1_token, agent2_token


def test_share_memory(test_memory_and_agents):
    """共享記憶測試"""
    memory_id, agent1_token, agent2_token = test_memory_and_agents

    response = client.post(
        f"/memories/{memory_id}/share",
        json={"agent_id": agent2_token},
        headers={"Authorization": f"Bearer {agent1_token}"}
    )

    assert response.status_code == 200
    assert response.json()["success"] is True


def test_get_shared_with(test_memory_and_agents):
    """查詢共享測試"""
    memory_id, agent1_token, agent2_token = test_memory_and_agents

    response = client.get(
        f"/memories/{memory_id}/shared-with",
        headers={"Authorization": f"Bearer {agent1_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "memory_id" in data
    assert "shared_with" in data


def test_revoke_sharing(test_memory_and_agents):
    """撤銷共享測試"""
    memory_id, agent1_token, agent2_token = test_memory_and_agents

    # 先共享
    client.post(
        f"/memories/{memory_id}/share",
        json={"agent_id": agent2_token},
        headers={"Authorization": f"Bearer {agent1_token}"}
    )

    # 再撤銷
    response = client.delete(
        f"/memories/{memory_id}/share/{agent2_token}",
        headers={"Authorization": f"Bearer {agent1_token}"}
    )

    assert response.status_code == 200
    assert response.json()["success"] is True


def test_sharing_permissions(test_memory_and_agents):
    """權限驗證測試"""
    memory_id, agent1_token, agent2_token = test_memory_and_agents

    # Agent 2 不能共享 Agent 1 的記憶
    response = client.post(
        f"/memories/{memory_id}/share",
        json={"agent_id": agent2_token},
        headers={"Authorization": f"Bearer {agent2_token}"}
    )

    assert response.status_code == 403
