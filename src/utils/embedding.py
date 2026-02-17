"""嵌入工具函數 - 改進版本"""

from typing import List, Optional
import numpy as np


def validate_embedding(embedding: List[float], expected_dim: Optional[int] = None) -> bool:
    """驗證嵌入向量的有效性

    Args:
        embedding: 要驗證的嵌入向量
        expected_dim: 期望的維度（可選）

    Returns:
        bool: 嵌入是否有效
    """
    if not embedding or not isinstance(embedding, list):
        return False

    if expected_dim is not None and len(embedding) != expected_dim:
        return False

    try:
        # 驗證所有元素都是數字
        for val in embedding:
            float(val)
        return True
    except (TypeError, ValueError):
        return False


def normalize_embedding(embedding: List[float]) -> List[float]:
    """規範化嵌入向量

    Args:
        embedding: 原始嵌入向量

    Returns:
        List[float]: 規範化後的嵌入向量

    Raises:
        ValueError: 如果嵌入向量無效
    """
    if not validate_embedding(embedding):
        raise ValueError("無效的嵌入向量")

    arr = np.array(embedding, dtype=np.float32)
    norm = np.linalg.norm(arr)

    if norm == 0:
        return embedding

    normalized = arr / norm
    return normalized.tolist()


def embedding_dimension(embedding: List[float]) -> int:
    """獲取嵌入向量的維度

    Args:
        embedding: 嵌入向量

    Returns:
        int: 向量維度

    Raises:
        ValueError: 如果嵌入向量無效
    """
    if not validate_embedding(embedding):
        raise ValueError("無效的嵌入向量")

    return len(embedding)


def cosine_similarity_batch(
    query_embedding: List[float],
    embeddings: List[List[float]]
) -> List[float]:
    """批量計算余弦相似度

    Args:
        query_embedding: 查詢嵌入向量
        embeddings: 嵌入向量列表

    Returns:
        List[float]: 相似度分數列表
    """
    if not validate_embedding(query_embedding):
        raise ValueError("無效的查詢嵌入向量")

    if not embeddings:
        return []

    similarities = []
    query_arr = np.array(query_embedding, dtype=np.float32)
    query_norm = np.linalg.norm(query_arr)

    if query_norm == 0:
        return [0.0] * len(embeddings)

    query_normalized = query_arr / query_norm

    for embedding in embeddings:
        if not validate_embedding(embedding):
            similarities.append(0.0)
            continue

        embed_arr = np.array(embedding, dtype=np.float32)
        embed_norm = np.linalg.norm(embed_arr)

        if embed_norm == 0:
            similarities.append(0.0)
        else:
            embed_normalized = embed_arr / embed_norm
            similarity = float(np.dot(query_normalized, embed_normalized))
            similarities.append(similarity)

    return similarities
