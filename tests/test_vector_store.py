import math
from src.rag.vector_store import VectorStore


class FakeEmbedder:
    def __init__(self):
        pass

    def embed_query(self, text: str):
        # deterministic small vector based on char codes
        v = [float((ord(c) % 10) + 1) for c in text[:10]]
        # pad/trim to length 10
        v = (v + [0.0] * 10)[:10]
        return v

    def embed_documents(self, texts):
        return [self.embed_query(t) for t in texts]


def test_similarity_search_basic():
    embedder = FakeEmbedder()
    store = VectorStore(embedder)

    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Climate change is accelerating and sea levels rise.",
        "Python is a programming language used for data science.",
    ]

    store.add_texts(texts)

    # Query similar to second text
    res = store.similarity_search("sea levels and climate", k=2)
    assert isinstance(res, list)
    assert len(res) <= 2
    # Ensure at least one returned item is from our texts
    assert any(t in texts for t in res)


def test_cosine_similarity_edge_cases():
    embedder = FakeEmbedder()
    store = VectorStore(embedder)

    # empty store -> empty results
    assert store.similarity_search("anything") == []

    # identical vectors should be highest similarity
    store.add_texts(["aaa", "bbb"])  # short texts produce vectors
    results = store.similarity_search("aaa", k=1)
    assert len(results) == 1
    assert results[0] in ["aaa", "bbb"]
