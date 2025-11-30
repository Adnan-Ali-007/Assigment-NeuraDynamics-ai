# Deployment Guide: RAG + Weather Assistant

## 1. Local Deployment (Development)

### Setup
```powershell
# Clone or navigate to project root
cd C:\Users\1azha\OneDrive\Desktop\assignment_ai

# Create virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env with your keys
# Copy .env.example or create:
# OPENROUTER_API_KEY=sk-or-v1-...
# OPENWEATHER_API_KEY=cc256d...
```

### Run
```powershell
streamlit run streamlit_app/app.py
```
- Opens at `http://localhost:8501`
- Upload PDF, ask questions, use weather lookup
- Stop with `Ctrl+C`

### Notes
- Stores uploaded PDFs in `data/` directory (local)
- Vector store is in-memory (lost on restart)
- Keys loaded from `.env` at startup

---

## 2. Streamlit Cloud Deployment (easiest)

### Prerequisites
- GitHub account
- Streamlit account (free at streamlit.io)
- Your code pushed to a public GitHub repo

### Steps
1. Push your repo to GitHub:
```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/assignment_ai.git
git push -u origin main
```

2. Go to streamlit.io and sign in with GitHub

3. Click **New app** → **From existing repo**
   - Repo: `YOUR_USERNAME/assignment_ai`
   - Branch: `main`
   - Main file path: `streamlit_app/app.py`

4. In the Streamlit Cloud dashboard, go to **Settings** (gear icon) → **Secrets**
   - Add your keys:
   ```
   OPENROUTER_API_KEY = "sk-or-v1-..."
   OPENWEATHER_API_KEY = "cc256d..."
   LANGCHAIN_API_KEY = "lsv2_pt_..."
   LANGCHAIN_PROJECT = "rag-weather-pipeline"
   ```

5. Click **Deploy** — app is live in ~2 min at `https://YOUR_USERNAME-assignment-ai.streamlit.app`

### Important
- `.env` is NOT uploaded to GitHub (add to `.gitignore` if not already)
- Streamlit Cloud loads secrets from dashboard, not `.env` file
- PDF uploads stored in temp dir (cleared between sessions by default)
- Free tier has limits (no persistent storage across restarts)

### Persistent Storage (upgrade option)
- For persistent vector store: use AWS S3 or a small database
- Add this to `streamlit_app/app.py`:
```python
import boto3
s3 = boto3.client('s3', aws_access_key_id=..., aws_secret_access_key=...)
# Save/load vector store to S3
```

---

## 3. Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Create .dockerignore
```
.git
.gitignore
venv
__pycache__
.pytest_cache
tests
data
.env
*.pyc
.DS_Store
```

### Build and run
```powershell
# Build
docker build -t rag-weather-app .

# Run locally (test)
docker run -e OPENROUTER_API_KEY="sk-or-v1-..." `
           -e OPENWEATHER_API_KEY="cc256d..." `
           -p 8501:8501 `
           rag-weather-app

# Now visit http://localhost:8501
```

### Deploy to Docker Hub
```powershell
# Tag
docker tag rag-weather-app YOUR_USERNAME/rag-weather-app:latest

# Login and push
docker login
docker push YOUR_USERNAME/rag-weather-app:latest
```

### Run on any server with Docker
```bash
docker run -e OPENROUTER_API_KEY="..." \
           -e OPENWEATHER_API_KEY="..." \
           -p 80:8501 \
           YOUR_USERNAME/rag-weather-app:latest
```

---

## 4. Cloud Deployment (AWS / Google Cloud / Azure)

### Option A: AWS EC2 + Streamlit
1. Launch an EC2 instance (Ubuntu 22.04, t2.micro free tier eligible)
2. SSH into instance:
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. Install Python and dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Create `.env` on server:
```bash
nano .env
# Paste your keys and save (Ctrl+O, Enter, Ctrl+X)
```

5. Run Streamlit:
```bash
streamlit run streamlit_app/app.py --server.port 80 --server.address 0.0.0.0
```

6. Access at `http://your-instance-ip`

### Option B: AWS ECS + Docker (managed)
1. Build Docker image (see Docker section above)
2. Push to Amazon ECR (Elastic Container Registry)
3. Create ECS task definition pointing to your image
4. Deploy task on ECS Fargate (serverless containers)
5. Attach ALB (Application Load Balancer) for HTTPS

### Option C: Google Cloud Run (simplest serverless)
1. Install Google Cloud CLI
2. Build and push to Google Container Registry:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/rag-weather-app
```

3. Deploy to Cloud Run:
```bash
gcloud run deploy rag-weather-app \
  --image gcr.io/PROJECT_ID/rag-weather-app \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --set-env-vars OPENROUTER_API_KEY=sk-or-v1-...,OPENWEATHER_API_KEY=cc256d...
```

4. Access at `https://rag-weather-app-XXXX.a.run.app`

---

## 5. Production Checklist

### Security
- [ ] Never commit `.env` or keys to public repos
- [ ] Use environment variables or secret managers (AWS Secrets Manager, Google Secret Manager, Azure Key Vault)
- [ ] Enable HTTPS (Streamlit Cloud and cloud providers do this automatically)
- [ ] Restrict API key permissions (read-only where possible)

### Performance
- [ ] Cache embeddings and vectors (consider Qdrant, Faiss, or Chroma for persistent store)
- [ ] Batch embedding API calls (current code loops; optimize in `src/rag/embedder.py`)
- [ ] Set request timeouts (weather API, embeddings API)
- [ ] Add rate limiting and authentication if public-facing

### Monitoring & Logging
- [ ] Log queries and responses (for debugging)
- [ ] Monitor LLM API costs (track token usage)
- [ ] Set up alerts for API failures (weather, OpenRouter)
- [ ] Track user sessions and error rates

### Data Persistence
- [ ] Store uploaded PDFs in S3 / Cloud Storage (not in container)
- [ ] Persist vector store in a dedicated database (Qdrant, Weaviate)
- [ ] Backup evaluation logs (`tests/langsmith_logs.jsonl`)

### Testing
- [ ] Run unit tests before deploying (`pytest -v tests/`)
- [ ] Test with real API keys in staging environment
- [ ] Load test (simulate multiple users / queries)

---

## 6. Quick Comparison

| Option | Cost | Setup Time | Persistence | Scaling |
|--------|------|-----------|-------------|---------|
| Local | Free | 5 min | Manual | N/A |
| Streamlit Cloud | Free tier / $5+/mo | 10 min | Limited | Easy |
| Docker + EC2 | $5–50/mo | 20 min | Manual | Manual |
| Google Cloud Run | Pay per request (~$0.40/M) | 15 min | Managed | Auto |
| AWS ECS Fargate | $10–100+/mo | 30 min | S3/RDS | Auto |

---

## 7. Recommended Starting Point for You

**For a quick demo:**
- Use **Streamlit Cloud** — free, live in 10 minutes, no ops needed.

**For production with low cost:**
- Use **Google Cloud Run** — serverless, scales automatically, pay only for execution.

**For full control:**
- Use **AWS EC2 + Docker** — more setup but flexible.

---

## 8. Deployment Troubleshooting

### Streamlit Cloud
- **"ModuleNotFoundError: src"** — add `conftest.py` to tests/ (already done) and ensure `src/` files are in repo
- **"OPENROUTER_API_KEY not found"** — check Secrets in dashboard are set and spelled correctly
- **PDF upload fails** — Streamlit Cloud has limited temp storage; for persistent uploads use S3

### Docker
- **Port already in use** — change `-p 8501:8501` to `-p 8502:8501` or kill the existing process
- **Permission denied on .env** — use `--build-arg` to pass env vars instead:
```powershell
docker build --build-arg OPENROUTER_API_KEY="sk-or-v1-..." -t rag-weather-app .
```

### Cloud providers
- **Timeout on first request** — cold start (container spinning up). Normal; optimize by keeping container warm or using provisioned concurrency
- **API key visible in logs** — sanitize logs before sharing; never hardcode keys in Dockerfile

---

## Next Steps

1. **Choose your deployment target** (recommend Streamlit Cloud for demo)
2. **Push to GitHub** (if using Streamlit Cloud)
3. **Set secrets** in dashboard
4. **Test** with sample queries
5. **Monitor** logs and costs

Questions? Refer to the provider's docs:
- Streamlit Cloud: https://docs.streamlit.io/deploy/streamlit-community-cloud
- Google Cloud Run: https://cloud.google.com/run/docs
- AWS ECS: https://docs.aws.amazon.com/ecs/
