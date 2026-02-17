"""語義搜索引擎 - 基於向量相似度"""

from typing import List, Tuple, Optional
import numpy as np


class SearchService:
    """語義搜索引擎，基於向量相似度"""

    def __init__(self, embedding_service: 'EmbeddingService'):
        """初始化搜索服務

        Args:
            embedding_service: 嵌入服務實例
        """
        self.embedding_service = embedding_service

    async def semantic_search(
        self,
        query: str,
        memories: List,
        top_k: int = 10,
        similarity_threshold: float = 0.3
    ) -> List[Tuple]:
        """語義搜索記憶

        邏輯：
            1. 獲取查詢的嵌入
            2. 為每個 memory 計算相似度
            3. 過濾相似度低於閾值的結果
            4. 按相似度降序排序
            5. 返回前 top_k 個結果

        Args:
            query: 搜索查詢文本
            memories: 記憶列表
            top_k: 返回前 K 個結果
            similarity_threshold: 相似度閾值

        Returns:
            [(memory, similarity_score), ...] 排序後的結果
        """
        query_embedding = await self.embedding_service.get_embeddings(query)

        results = []
        for memory in memories:
            if hasattr(memory, 'embeddings') and memory.embeddings:
                score = self.cosine_similarity(query_embedding, memory.embeddings)
                if score >= similarity_threshold:
                    results.append((memory, score))

        # 按相似度降序排序
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """計算兩個向量的余弦相似度

        Args:
            vec1: 第一個向量
            vec2: 第二個向量

        Returns:
            相似度分數 (0.0 到 1.0)
        """
        try:
            arr1 = np.array(vec1)
            arr2 = np.array(vec2)

            norm1 = np.linalg.norm(arr1)
            norm2 = np.linalg.norm(arr2)

            if norm1 == 0 or norm2 == 0:
                return 0.0

            arr1_normalized = arr1 / norm1
            arr2_normalized = arr2 / norm2

            return float(np.dot(arr1_normalized, arr2_normalized))
        except Exception:
            return 0.0
