from src.agents.rag_node import rag_node


class FakeRetriever:
    def __init__(self, texts):
        self._texts = texts

    def similarity_search(self, query, k=3):
        return []


def test_rag_node_fallback_keyword_search():
    retriever = FakeRetriever(["This doc mentions Paris and weather.", "Other content about biology."])
    state = {"user_input": "Tell me about Paris weather", "retriever": retriever}
    out = rag_node(state)
    assert "context" in out
    assert "Paris" in out["context"] or "Paris" in " ".join(retriever._texts)
