import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, SRC_DIR)
from dotenv import load_dotenv
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(ENV_PATH) 
import streamlit as st

try:
    import langchain as _langchain
    if not hasattr(_langchain, "debug"):
        _langchain.debug = False
    if not hasattr(_langchain, "verbose"):
        _langchain.verbose = False
    if not hasattr(_langchain, "llm_cache"):
        _langchain.llm_cache = None
except Exception:
    pass

from src.rag.pdf_loader import load_and_chunk_pdf
from src.rag.embedder import get_embedder
from src.rag.vector_store import VectorStore
from src.agents.graph_builder import build_graph
from src.agents.router_node import route_query

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

st.set_page_config(page_title="Weather & document assistant", layout="centered")
st.title("Weather & document assistant")

st.subheader("Upload a PDF for querying ")
uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"], accept_multiple_files=False)

if uploaded_pdf:
    pdf_path = os.path.join(DATA_DIR, "uploaded.pdf")
    with open(pdf_path, "wb") as f:
        f.write(uploaded_pdf.read())

    st.success("PDF uploaded successfully.")

    chunks = load_and_chunk_pdf(pdf_path)
    embedder = get_embedder()
    vector_dim = len(embedder.embed_query("test"))

    store = VectorStore(embedder)
    store.create_collection(vector_dim)
    store.add_texts(chunks)

    st.session_state["retriever"] = store
    st.info(f"PDF processed and indexed into {len(chunks)} chunks.")

st.subheader("Ask a question")
query = st.text_input("Ask about realtime weather or your PDF", "")

if st.button("Ask"):
    if not query.strip():
        st.error("Please enter a question.")
    else:
        query_type = route_query(query)
        graph = build_graph()

        if query_type == "weather":
            result = graph.invoke({
                "user_input": query,
                "retriever": None
            })
            st.success("Weather result:")
            st.info(result["final_answer"])
        else:
            if "retriever" not in st.session_state:
                st.error("Please upload a PDF to answer document-based questions.")
            else:
                result = graph.invoke({
                    "user_input": query,
                    "retriever": st.session_state["retriever"]
                })
                st.success("PDF RAG Answer:")
                st.info(result["final_answer"])
