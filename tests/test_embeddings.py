"""嵌入服務測試"""

import pytest
import asyncio
from src.services.embedding_service import EmbeddingService


@pytest.fixture
def embedding_service():
    """創建嵌入服務實例"""
    return EmbeddingService(use_openai=False, model_name="all-MiniLM-L6-v2")


@pytest.mark.asyncio
async def test_embedding_service_basic(embedding_service):
    """基本嵌入測試"""
    text = "這是一個測試文本"
    embedding = await embedding_service.get_embeddings(text)

    assert isinstance(embedding, list)
    assert len(embedding) > 0
    assert all(isinstance(x, float) for x in embedding)


@pytest.mark.asyncio
async def test_batch_embeddings(embedding_service):
    """批量嵌入測試"""
    texts = [
        "第一個測試文本",
        "第二個測試文本",
        "第三個測試文本"
    ]
    embeddings = await embedding_service.batch_embeddings(texts)

    assert isinstance(embeddings, list)
    assert len(embeddings) == 3
    assert all(isinstance(e, list) for e in embeddings)
    assert all(len(e) > 0 for e in embeddings)


@pytest.mark.asyncio
async def test_embedding_consistency(embedding_service):
    """一致性測試（相同輸入 → 相同輸出）"""
    text = "一致性測試文本"

    embedding1 = await embedding_service.get_embeddings(text)
    embedding2 = await embedding_service.get_embeddings(text)

    assert embedding1 == embedding2


@pytest.mark.asyncio
async def test_embedding_dimensions(embedding_service):
    """驗證維度正確"""
    text = "維度測試"
    embedding = await embedding_service.get_embeddings(text)

    # all-MiniLM-L6-v2 的維度是 384
    assert len(embedding) == 384


@pytest.mark.asyncio
async def test_empty_text_raises_error(embedding_service):
    """空文本應引發錯誤"""
    with pytest.raises(ValueError):
        await embedding_service.get_embeddings("")

    with pytest.raises(ValueError):
        await embedding_service.get_embeddings("   ")


@pytest.mark.asyncio
async def test_batch_embeddings_empty_list(embedding_service):
    """空列表應返回空列表"""
    embeddings = await embedding_service.batch_embeddings([])
    assert embeddings == []


@pytest.mark.asyncio
async def test_batch_embeddings_single_item(embedding_service):
    """單項批量嵌入"""
    texts = ["單個文本"]
    embeddings = await embedding_service.batch_embeddings(texts)

    assert len(embeddings) == 1
    assert len(embeddings[0]) == 384
