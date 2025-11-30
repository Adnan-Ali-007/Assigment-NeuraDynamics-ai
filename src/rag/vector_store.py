import math
from typing import List


class VectorStore:
    def __init__(self, embedder, collection_name: str = "documents"):
        self.embedder = embedder
        self.collection_name = collection_name
        self._texts: List[str] = []
        self._vectors: List[List[float]] = []

    def create_collection(self, vector_size: int):
        self._texts = []
        self._vectors = []

    def add_texts(self, texts: list):
        for text in texts:
            emb = self.embedder.embed_query(text)
            self._texts.append(text)
            self._vectors.append(list(emb))

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def similarity_search(self, query: str, k: int = 5) -> list:
        q_emb = list(self.embedder.embed_query(query))
        scores = []
        for text, vec in zip(self._texts, self._vectors):
            score = self._cosine_similarity(q_emb, vec)
            scores.append((score, text))
        scores.sort(reverse=True, key=lambda x: x[0])
        return [t for s, t in scores[:k]]
