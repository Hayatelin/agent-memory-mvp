"""端到端整合測試"""

import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from src.db.database import Base, get_db
from src.models.models import Agent, Memory
from src.services.embedding_service import EmbeddingService
from src.services.search_service import SearchService

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
def test_workspace(db_session):
    """創建測試工作區"""
    workspace_id = uuid4()
    agent = Agent(id=uuid4(), name="test_agent", workspace_id=workspace_id)
    db_session.add(agent)
    db_session.commit()

    return agent, workspace_id


@pytest.mark.asyncio
async def test_create_and_search_memory(test_workspace, db_session):
    """測試：創建記憶後能搜索到它"""
    agent, workspace_id = test_workspace

    # 1. 創建記憶
    memory = Memory(
        id=uuid4(),
        workspace_id=workspace_id,
        created_by_agent_id=agent.id,
        type="knowledge",
        category="ai",
        content="機器學習是人工智能的重要分支",
        visibility="private"
    )

    # 2. 生成嵌入
    embedding_service = EmbeddingService()
    embeddings = await embedding_service.get_embeddings(memory.content)
    memory.embeddings = embeddings

    db_session.add(memory)
    db_session.commit()

    # 3. 搜索相關記憶
    all_memories = db_session.query(Memory).filter(
        Memory.workspace_id == workspace_id,
        Memory.is_deleted == False
    ).all()

    search_service = SearchService(embedding_service)
    results = await search_service.semantic_search(
        "機器學習",
        all_memories,
        top_k=10
    )

    # 4. 驗證結果
    assert len(results) > 0
    assert results[0][0].id == memory.id


@pytest.mark.asyncio
async def test_search_with_multiple_memories(test_workspace, db_session):
    """測試：多個記憶搜索排序正確"""
    agent, workspace_id = test_workspace

    # 創建多個記憶
    texts = [
        "機器學習是人工智能的核心",
        "深度學習使用神經網絡",
        "自然語言處理是 NLP 的重要領域"
    ]

    embedding_service = EmbeddingService()
    memories = []

    for i, text in enumerate(texts):
        embeddings = await embedding_service.get_embeddings(text)
        memory = Memory(
            id=uuid4(),
            workspace_id=workspace_id,
            created_by_agent_id=agent.id,
            type="knowledge",
            category="ai",
            content=text,
            visibility="private",
            embeddings=embeddings
        )
        db_session.add(memory)
        memories.append(memory)

    db_session.commit()

    # 搜索
    all_memories = db_session.query(Memory).filter(
        Memory.workspace_id == workspace_id,
        Memory.is_deleted == False
    ).all()

    search_service = SearchService(embedding_service)
    results = await search_service.semantic_search(
        "機器學習",
        all_memories,
        top_k=3
    )

    # 驗證排序
    assert len(results) > 0
    for i in range(len(results) - 1):
        assert results[i][1] >= results[i + 1][1]


@pytest.mark.asyncio
async def test_embedding_generation(test_workspace, db_session):
    """測試：自動生成嵌入"""
    agent, workspace_id = test_workspace

    embedding_service = EmbeddingService()

    # 創建記憶
    memory = Memory(
        id=uuid4(),
        workspace_id=workspace_id,
        created_by_agent_id=agent.id,
        type="preference",
        category="user",
        content="用戶偏好 JSON 格式的回應",
        visibility="private"
    )

    # 生成嵌入
    embeddings = await embedding_service.get_embeddings(memory.content)
    memory.embeddings = embeddings

    db_session.add(memory)
    db_session.commit()

    # 驗證嵌入已保存
    saved_memory = db_session.query(Memory).filter(Memory.id == memory.id).first()
    assert saved_memory.embeddings is not None
    assert len(saved_memory.embeddings) == 384  # all-MiniLM-L6-v2 維度


@pytest.mark.asyncio
async def test_shared_memory_visibility(test_workspace, db_session):
    """測試：共享記憶的可見性"""
    agent, workspace_id = test_workspace

    # 創建另一個 Agent
    other_agent = Agent(id=uuid4(), name="other_agent", workspace_id=workspace_id)
    db_session.add(other_agent)
    db_session.commit()

    # 創建記憶
    memory = Memory(
        id=uuid4(),
        workspace_id=workspace_id,
        created_by_agent_id=agent.id,
        type="knowledge",
        category="test",
        content="私有記憶",
        visibility="private"
    )

    db_session.add(memory)
    db_session.commit()

    # 共享
    memory.shared_with_agents.append(other_agent)
    db_session.commit()

    # 驗證共享
    saved_memory = db_session.query(Memory).filter(Memory.id == memory.id).first()
    assert other_agent in saved_memory.shared_with_agents
