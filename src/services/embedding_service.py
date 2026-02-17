"""向量嵌入服務 - 支持本地模型和 OpenAI API"""

from sentence_transformers import SentenceTransformer
from typing import List, Optional
import numpy as np


class EmbeddingService:
    """向量嵌入服務，支持本地模型和 OpenAI API"""

    def __init__(self, use_openai: bool = False, model_name: str = "all-MiniLM-L6-v2"):
        """初始化嵌入服務

        Args:
            use_openai: 是否使用 OpenAI API
            model_name: 本地模型名稱
        """
        self.use_openai = use_openai
        self.model_name = model_name
        if not use_openai:
            self.model = SentenceTransformer(model_name)

    async def get_embeddings(
        self,
        text: str,
        model_name: Optional[str] = None
    ) -> List[float]:
        """獲取單個文本的嵌入

        Args:
            text: 要嵌入的文本
            model_name: 模型名稱（可選，覆蓋默認值）

        Returns:
            嵌入向量 (List[float])

        Raises:
            ValueError: 如果文本為空
            RuntimeError: 如果嵌入生成失敗
        """
        if not text or not text.strip():
            raise ValueError("文本不能為空")

        try:
            model_to_use = model_name or self.model_name
            if self.use_openai:
                # OpenAI API 實現（可選）
                pass
            else:
                # 本地模型實現
                embedding = self.model.encode(text)
                return embedding.tolist()
        except Exception as e:
            raise RuntimeError(f"嵌入生成失敗: {e}")

    async def batch_embeddings(
        self,
        texts: List[str],
        batch_size: int = 32
    ) -> List[List[float]]:
        """批量獲取嵌入

        Args:
            texts: 文本列表
            batch_size: 批次大小（控制內存使用）

        Returns:
            嵌入列表 (List[List[float]])
        """
        if not texts:
            return []

        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.model.encode(batch)
            embeddings.extend([e.tolist() for e in batch_embeddings])
        return embeddings
