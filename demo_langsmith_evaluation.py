import os
from dotenv import load_dotenv

load_dotenv()

from src.rag.pdf_loader import load_and_chunk_pdf
from src.rag.embedder import get_embedder
from src.rag.vector_store import VectorStore
from src.agents.graph_builder import build_graph
from src.testing.langsmith_helper import log_evaluation


def run_demo():
    pdf_path = "data/uploaded.pdf"
    
    if not os.path.exists(pdf_path):
        run_weather_demo()
        return
    
    chunks = load_and_chunk_pdf(pdf_path)
    embedder = get_embedder()
    store = VectorStore(embedder)
    store.add_texts(chunks)
    graph = build_graph()
    
    queries = [
        ("what is this document about?", "RAG"),
        ("weather in london", "Weather"),
        ("what are the main topics?", "RAG"),
    ]
    
    for query, qtype in queries:
        try:
            if qtype == "Weather":
                res = graph.invoke({"user_input": query, "retriever": None})
            else:
                res = graph.invoke({"user_input": query, "retriever": store})
            ans = res.get("final_answer", "")
            print(f"{query}\n{ans}\n")
            log_evaluation(f"demo-{qtype.lower()}", ans, query)
        except Exception as e:
            print(f"Error: {e}")


def run_weather_demo():
    graph = build_graph()
    query = "What is the weather in Paris?"
    try:
        res = graph.invoke({"user_input": query, "retriever": None})
        ans = res.get("final_answer", "")
        print(f"{query}\n{ans}")
        log_evaluation("demo-weather", ans, query)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run_demo()

