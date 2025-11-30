Guide to run this locally
setup your own virtual environmet
install the requirement.txt packages via pip install -r requirements.txt
setup api key via open router
and setup OPENWEATHER_API_KEY
LANGCHAIN_API_KEY 
have these api keys in your .env 
after alll this setup you can run the application via 
streamlit run streamlit_app/app.py
u can check langsmith evaluation via your dashboard

Run unit tests:
pytest -v tests/
Add a documenment for rag funcunality and u can chat for realtime weather updates have used both free api keys so limited functionalities  are there 

A simple Streamlit app that answers questions about uploaded PDFs using retrieval-augmented generation (RAG) and also provides current weather information.

## Features

- **PDF Upload & Indexing** — extract text, chunk, and embed documents
- **RAG Retrieval** — semantic search over document chunks
- **Weather Lookup** — current weather via OpenWeather or Open‑Meteo
- **Agent Routing** — automatically routes queries to RAG or weather
- **Clean API** — uses OpenRouter for embeddings and chat

## Prerequisites

- Python 3.10+
- `pip` or conda
- API keys:
  - `OPENROUTER_API_KEY` (required for embeddings & LLM)
  - `OPENWEATHER_API_KEY` (optional; falls back to Open‑Meteo if not set)

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/Adnan-Ali-007/Assigment-NeuraDynamics-ai.git
cd Assigment-NeuraDynamics-ai
```

### 2. Create virtual environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root:
```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENWEATHER_API_KEY=your-openweather-key-here
```

Get keys from:
- OpenRouter: https://openrouter.ai/
- OpenWeather: https://openweathermap.org/api (optional)

### 5. Run the app
```bash
streamlit run streamlit_app/app.py
```

Open your browser to `http://localhost:8501`

## Usage

1. **Upload a PDF** — click the uploader in the sidebar
2. **Wait for indexing** — app chunks, embeds, and stores in vector DB
3. **Ask a question** — either about your document or about weather
4. Examples:
   - "What is this document about?" (RAG)
   - "What's the weather in London?" (Weather)

## Project Structure

```
.
├── streamlit_app/
│   └── app.py                 # Main Streamlit UI
├── src/
│   ├── rag/
│   │   ├── pdf_loader.py      # PDF text extraction & chunking
│   │   ├── embedder.py        # OpenRouter embeddings wrapper
│   │   └── vector_store.py    # In-memory vector store with cosine similarity
│   ├── agents/
│   │   ├── graph_builder.py   # LangGraph state graph
│   │   ├── router_node.py     # Routes queries to weather or RAG
│   │   ├── rag_node.py        # Retrieves document chunks
│   │   ├── weather_node.py    # Extracts location and fetches weather
│   │   └── llm_node.py        # Calls OpenRouter chat with context
│   ├── weather/
│   │   └── weather_api.py     # Weather API wrapper (OpenWeather + fallback)
│   └── testing/
│       └── langsmith_helper.py # Simple local evaluation logger
├── tests/
│   ├── conftest.py            # Pytest configuration
│   ├── test_*.py              # Unit tests
│   └── langsmith_logs.jsonl   # Evaluation logs (generated)
├── run_graph.py               # CLI runner (alternative to Streamlit)
├── requirements.txt           # Dependencies
├── DEPLOYMENT.md              # Deployment guide
└── README.md                  # This file
```

## How It Works

### RAG Pipeline
1. **Load PDF** → extract text using pypdf
2. **Chunk** → split into 1000-char chunks with 200-char overlap
3. **Embed** → send chunks to OpenRouter embeddings API
4. **Store** → keep vectors in memory with raw text
5. **Query** → embed user question, search top-3 similar chunks
6. **LLM** → pass retrieved context + question to LLM with strict prompt

### Weather Route
1. **Detect** → router checks for "weather" / "temperature" keywords
2. **Parse** → extract location via regex (e.g., "weather in London" → "London")
3. **Fetch** → call OpenWeather (if key set) or Open‑Meteo
4. **Return** → formatted string with temperature and conditions

## Testing

Run unit tests:
```bash
pytest -v tests/
```

Tests use mocking to avoid real API calls during CI. Check `tests/langsmith_logs.jsonl` for evaluation logs.


## Deployment

See `DEPLOYMENT.md` for guides on:
- Streamlit Cloud (free, easiest)

Quick start: push to GitHub, deploy to Streamlit Cloud in 10 min.


## Troubleshooting

**"ModuleNotFoundError: No module named 'src'"**
- Ensure `tests/conftest.py` exists and sets `sys.path`
- Run from project root: `streamlit run streamlit_app/app.py`

**"OPENROUTER_API_KEY not found"**
- Check `.env` is in project root
- Verify key format: should start with `sk-or-v1-`

**PDF upload fails**
- Check file size (large PDFs may timeout)
- Ensure PDF is readable (not scanned image only)

**Weather query returns generic response**
- Check location extraction regex in `src/agents/weather_node.py`
- Try format: "weather in [city]"


