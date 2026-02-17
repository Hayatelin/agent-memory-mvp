"""搜索 API 測試"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from src.main import app
from src.db.database import Base, get_db
from src.models.models import Agent, Memory

# 使用內存 SQLite 數據庫進行測試
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
def test_agent_and_token():
    """創建測試 Agent 並返回 token"""
    db = TestingSessionLocal()
    agent_id = uuid4()
    workspace_id = uuid4()

    agent = Agent(
        id=agent_id,
        name="test_agent",
        workspace_id=workspace_id
    )
    db.add(agent)
    db.commit()
    db.close()

    return str(agent_id), workspace_id


@pytest.fixture
def test_memories(test_agent_and_token):
    """創建測試記憶"""
    agent_token, workspace_id = test_agent_and_token
    from uuid import UUID as UUIDType
    agent_id = UUIDType(agent_token)

    db = TestingSessionLocal()

    # 創建幾個測試記憶
    memories = []
    texts = [
        "機器學習是人工智能的重要分支",
        "深度學習使用神經網絡",
        "自然語言處理是 NLP 的核心"
    ]

    for text in texts:
        memory = Memory(
            id=uuid4(),
            workspace_id=workspace_id,
            created_by_agent_id=agent_id,
            type="knowledge",
            category="ai",
            content=text,
            visibility="private"
        )
        db.add(memory)
        memories.append(memory)

    db.commit()
    db.close()

    return memories, agent_token


def test_search_endpoint_basic(test_agent_and_token):
    """基本搜索測試"""
    agent_token, _ = test_agent_and_token

    response = client.post(
        "/memories/search",
        json={"query": "機器學習", "limit": 10},
        headers={"Authorization": f"Bearer {agent_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total" in data


def test_search_stats(test_agent_and_token):
    """統計端點測試"""
    agent_token, _ = test_agent_and_token

    response = client.get(
        "/memories/search/stats",
        headers={"Authorization": f"Bearer {agent_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "total_memories" in data
    assert "searchable_memories" in data
    assert "embedding_coverage" in data


def test_search_auth_required():
    """認證檢查測試"""
    response = client.post(
        "/memories/search",
        json={"query": "test"}
    )

    assert response.status_code == 403


def test_search_with_empty_query(test_agent_and_token):
    """空查詢測試"""
    agent_token, _ = test_agent_and_token

    response = client.post(
        "/memories/search",
        json={"query": "", "limit": 10},
        headers={"Authorization": f"Bearer {agent_token}"}
    )

    assert response.status_code == 400
