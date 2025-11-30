def rag_node(state):
    user_input = state.get("user_input", "")
    retriever = state.get("retriever")

    if not retriever:
        return {"context": ""}

    try:
        context_docs = retriever.similarity_search(user_input, k=3)
    except Exception:
        context_docs = []

    if not context_docs or all(len(doc.strip()) < 50 for doc in context_docs):
        texts = getattr(retriever, "_texts", [])
        context_docs = _keyword_search(user_input, texts)

    context = "\n---\n".join(context_docs) if context_docs else ""
    return {"context": context}


def _keyword_search(query: str, texts: list, k: int = 3) -> list:
    q_words = set(w for w in query.lower().split() if len(w) > 2)
    scored = []
    for text in texts:
        t = text.lower()
        matches = sum(1 for w in q_words if w in t)
        if matches:
            scored.append((matches, text))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [text for _, text in scored[:k]]

