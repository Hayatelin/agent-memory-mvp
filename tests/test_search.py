"""搜索服務測試"""

import pytest
import asyncio
from src.services.embedding_service import EmbeddingService
from src.services.search_service import SearchService


@pytest.fixture
def embedding_service():
    """創建嵌入服務實例"""
    return EmbeddingService(use_openai=False, model_name="all-MiniLM-L6-v2")


@pytest.fixture
def search_service(embedding_service):
    """創建搜索服務實例"""
    return SearchService(embedding_service)


class MockMemory:
    """模擬Memory對象用於測試"""
    def __init__(self, id, content, embeddings):
        self.id = id
        self.content = content
        self.embeddings = embeddings


@pytest.mark.asyncio
async def test_semantic_search_basic(embedding_service, search_service):
    """基本搜索測試"""
    # 創建測試記憶
    embedding1 = await embedding_service.get_embeddings("機器學習是人工智能的一部分")
    embedding2 = await embedding_service.get_embeddings("深度學習使用神經網絡")
    embedding3 = await embedding_service.get_embeddings("天氣今天很好")

    memories = [
        MockMemory(1, "機器學習是人工智能的一部分", embedding1),
        MockMemory(2, "深度學習使用神經網絡", embedding2),
        MockMemory(3, "天氣今天很好", embedding3),
    ]

    query = "人工智能"
    results = await search_service.semantic_search(query, memories, top_k=2)

    assert len(results) <= 2
    assert all(isinstance(r, tuple) and len(r) == 2 for r in results)


@pytest.mark.asyncio
async def test_cosine_similarity(search_service):
    """相似度計算驗證"""
    # 相同向量的相似度應為 1.0
    vec1 = [1.0, 0.0, 0.0]
    vec2 = [1.0, 0.0, 0.0]
    similarity = SearchService.cosine_similarity(vec1, vec2)
    assert abs(similarity - 1.0) < 0.01

    # 正交向量的相似度應為 0.0
    vec1 = [1.0, 0.0, 0.0]
    vec2 = [0.0, 1.0, 0.0]
    similarity = SearchService.cosine_similarity(vec1, vec2)
    assert abs(similarity) < 0.01

    # 相反向量的相似度應為 -1.0
    vec1 = [1.0, 0.0, 0.0]
    vec2 = [-1.0, 0.0, 0.0]
    similarity = SearchService.cosine_similarity(vec1, vec2)
    assert abs(similarity + 1.0) < 0.01


@pytest.mark.asyncio
async def test_search_ranking(embedding_service, search_service):
    """排序邏輯驗證"""
    # 創建相關性不同的記憶
    embedding1 = await embedding_service.get_embeddings("機器學習算法")
    embedding2 = await embedding_service.get_embeddings("機器學習是人工智能的核心")
    embedding3 = await embedding_service.get_embeddings("統計學基礎")

    memories = [
        MockMemory(1, "機器學習算法", embedding1),
        MockMemory(2, "機器學習是人工智能的核心", embedding2),
        MockMemory(3, "統計學基礎", embedding3),
    ]

    query = "機器學習"
    results = await search_service.semantic_search(query, memories, top_k=10)

    # 驗證結果按相似度降序排列
    if len(results) > 1:
        for i in range(len(results) - 1):
            assert results[i][1] >= results[i + 1][1]


@pytest.mark.asyncio
async def test_search_threshold_filtering(embedding_service, search_service):
    """閾值過濾驗證"""
    # 創建記憶
    embedding1 = await embedding_service.get_embeddings("機器學習")
    embedding2 = await embedding_service.get_embeddings("天氣預報")

    memories = [
        MockMemory(1, "機器學習", embedding1),
        MockMemory(2, "天氣預報", embedding2),
    ]

    query = "機器學習"

    # 使用高閾值應返回較少結果
    results_high_threshold = await search_service.semantic_search(
        query, memories, similarity_threshold=0.8
    )

    # 使用低閾值應返回更多結果
    results_low_threshold = await search_service.semantic_search(
        query, memories, similarity_threshold=0.1
    )

    assert len(results_high_threshold) <= len(results_low_threshold)


@pytest.mark.asyncio
async def test_empty_memories_list(search_service):
    """空記憶列表"""
    results = await search_service.semantic_search("查詢", [], top_k=10)
    assert results == []


@pytest.mark.asyncio
async def test_zero_norm_vectors(search_service):
    """零向量處理"""
    # 創建零向量
    zero_vec = [0.0, 0.0, 0.0]
    vec = [1.0, 0.0, 0.0]

    similarity = SearchService.cosine_similarity(zero_vec, vec)
    assert similarity == 0.0

    similarity = SearchService.cosine_similarity(vec, zero_vec)
    assert similarity == 0.0
