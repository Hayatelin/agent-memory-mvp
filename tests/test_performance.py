"""性能測試"""

import pytest
import asyncio
import time
from uuid import uuid4
from src.services.embedding_service import EmbeddingService
from src.services.search_service import SearchService


class MockMemory:
    """模擬 Memory 對象"""
    def __init__(self, id, content, embeddings):
        self.id = id
        self.content = content
        self.embeddings = embeddings


@pytest.mark.asyncio
async def test_embedding_generation_speed():
    """測試：嵌入生成速度 >10/秒"""
    embedding_service = EmbeddingService()

    texts = [
        f"測試文本 {i}" for i in range(20)
    ]

    start_time = time.time()
    embeddings = await embedding_service.batch_embeddings(texts, batch_size=32)
    elapsed = time.time() - start_time

    # 20 個嵌入應該在 2 秒內完成（>10/秒）
    assert elapsed < 2.0
    assert len(embeddings) == 20


@pytest.mark.asyncio
async def test_search_latency_small():
    """測試：100 個記憶搜索延遲 <200ms"""
    embedding_service = EmbeddingService()
    search_service = SearchService(embedding_service)

    # 創建 100 個測試記憶
    texts = [f"記憶 {i} 的內容是關於主題 {i % 10}" for i in range(100)]
    embeddings_list = await embedding_service.batch_embeddings(texts)

    memories = [
        MockMemory(uuid4(), texts[i], embeddings_list[i])
        for i in range(100)
    ]

    # 測試搜索延遲
    start_time = time.time()
    results = await search_service.semantic_search(
        "記憶內容",
        memories,
        top_k=10
    )
    elapsed = time.time() - start_time

    assert elapsed < 0.2  # 200ms
    assert len(results) > 0


@pytest.mark.asyncio
async def test_search_latency_large():
    """測試：1000 個記憶搜索延遲 <500ms"""
    embedding_service = EmbeddingService()
    search_service = SearchService(embedding_service)

    # 創建 1000 個測試記憶（分批生成嵌入）
    texts = [f"記憶 {i} 的內容涉及主題 {i % 50}" for i in range(1000)]

    # 分批生成嵌入以節省時間
    batch_size = 100
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        batch_embeddings = await embedding_service.batch_embeddings(batch_texts)
        all_embeddings.extend(batch_embeddings)

    memories = [
        MockMemory(uuid4(), texts[i], all_embeddings[i])
        for i in range(1000)
    ]

    # 測試搜索延遲
    start_time = time.time()
    results = await search_service.semantic_search(
        "記憶信息",
        memories,
        top_k=10
    )
    elapsed = time.time() - start_time

    assert elapsed < 0.5  # 500ms
    assert len(results) > 0


@pytest.mark.asyncio
async def test_cosine_similarity_throughput():
    """測試：相似度計算速度"""
    search_service = SearchService(None)

    # 創建向量
    vec1 = [0.1 * i for i in range(384)]  # 384 維向量
    vectors = [[0.1 * (i + j) % 1.0 for j in range(384)] for i in range(1000)]

    # 測試 1000 次相似度計算的速度
    start_time = time.time()
    for vec in vectors:
        SearchService.cosine_similarity(vec1, vec)
    elapsed = time.time() - start_time

    # 應該快速完成（1000 次在 0.1 秒內）
    assert elapsed < 0.1


@pytest.mark.asyncio
async def test_batch_embedding_efficiency():
    """測試：批量嵌入相比單個嵌入的效率"""
    embedding_service = EmbeddingService()

    texts = [f"測試文本 {i}" for i in range(50)]

    # 批量嵌入
    start_batch = time.time()
    batch_embeddings = await embedding_service.batch_embeddings(texts, batch_size=32)
    elapsed_batch = time.time() - start_batch

    # 單個嵌入
    start_single = time.time()
    for text in texts:
        await embedding_service.get_embeddings(text)
    elapsed_single = time.time() - start_single

    # 批量應該比單個快
    assert elapsed_batch < elapsed_single
    assert len(batch_embeddings) == 50
