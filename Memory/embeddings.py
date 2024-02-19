import numpy as np
from scipy.spatial.distance import cosine
from typing import List, Tuple

class Embedding:
    def __init__(self):
        pass

    @staticmethod
    def calculate_cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
        """计算余弦相似度"""
        return 1 - cosine(embedding1, embedding2)

    @staticmethod
    def find_top_similar_messages(target_message: str, data: List[dict], top_n: int = 5) -> List[Tuple[str, float]]:
        """找到与目标消息最相似的top_n个消息及其相似度"""
        similarities = []  # 存储相似度及对应的消息
        target_embedding = None  # 目标消息的嵌入向量
        # 获取目标消息的嵌入向量
        for entry in data:
            if entry.get('message') == target_message:
                target_embedding = entry.get('embedding')
                break
        if target_embedding is None:
            raise ValueError("Target message not found in the data.")

        # 计算目标消息与其他消息的相似度
        for entry in data:
            if entry.get('message') != target_message and 'embedding' in entry:
                similarity = Embedding.calculate_cosine_similarity(target_embedding, entry['embedding'])
                similarities.append((entry.get('message'), similarity))

        # 根据相似度排序，并返回top_n个最相似的消息及其相似度
        sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
        return sorted_similarities[:top_n]