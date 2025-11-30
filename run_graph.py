from dotenv import load_dotenv
load_dotenv()
from src.rag.pdf_loader import load_and_chunk_pdf
from src.rag.embedder import get_embedder
from src.rag.vector_store import VectorStore
from src.agents.graph_builder import build_graph
def init_rag(pdf_path="data/uploaded.pdf"):
    chunks = load_and_chunk_pdf(pdf_path)

    embedder = get_embedder()
    vector_dim = len(embedder.embed_query("sample text"))

    store = VectorStore(embedder)
    store.create_collection(vector_dim)
    store.add_texts(chunks)

    return store


if __name__ == "__main__":
    retriever = init_rag()
    graph = build_graph()

    print("\nRAG + Weather Assistant")
    print("-----------------------")

    while True:
        user_query = input("\nAsk something: ")
        out = graph.invoke({"user_input": user_query, "retriever": retriever})
        print("\n→", out["final_answer"])
