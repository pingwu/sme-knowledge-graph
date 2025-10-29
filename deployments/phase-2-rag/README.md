# Phase 1: Minimal Chatbot

**Goal**: Get a local AI chatbot running in 5 minutes

**What you'll have**:
- Local LLM (llama3.2) running on your computer
- Web UI chatbot interface
- Chat history maintained in browser
- 100% private - no cloud, no data leaves your machine

---

## Prerequisites

- **Docker Desktop** installed and running
- **16GB RAM** recommended (8GB minimum)
- **10GB free disk space** (for model download)
- **Internet connection** (first time only, to download model)

---

## Quick Start (3 Steps)

### Step 1: Navigate to Phase 1 Directory

```bash
cd sme-knowledge-graph\deployments\phase-1-minimal
```

### Step 2: Start the Services

```bash
docker-compose up
```

**What happens**:
1. Downloads Ollama container (~500MB)
2. Downloads llama3.2 model (~3GB) - **This takes 5-10 minutes first time**
3. Builds chatbot UI container
4. Starts both services

**Expected output**:
```
sme-ollama    | Ollama ready with llama3.2 model
sme-chatbot   | You can now view your Streamlit app in your browser.
sme-chatbot   | URL: http://0.0.0.0:8080
```

### Step 3: Open Your Browser

Navigate to: **http://localhost:8080**

You should see the chatbot interface!

---

## First Use

### Test Your Chatbot

Try these prompts:

1. **Basic conversation**:
   ```
   Hello! Can you help me organize my meeting notes?
   ```

2. **Brainstorming**:
   ```
   I need to capture tribal knowledge about our PostgreSQL setup.
   What categories should I organize this under?
   ```

3. **Structuring information**:
   ```
   I had a meeting with Acme Corp about their database migration.
   They prefer PostgreSQL over MySQL. How should I structure this note?
   ```

---

## Architecture (Phase 1)

```
┌─────────────────────────────────────┐
│   Browser (localhost:8080)          │
│   - Streamlit Web UI                │
│   - Chat interface                  │
│   - History in browser              │
└──────────────┬──────────────────────┘
               │ HTTP
┌──────────────▼──────────────────────┐
│   Chatbot Container                 │
│   - Streamlit app                   │
│   - Python requests                 │
└──────────────┬──────────────────────┘
               │ HTTP API
┌──────────────▼──────────────────────┐
│   Ollama Container                  │
│   - llama3.2 model (3GB)            │
│   - Local inference                 │
│   - No cloud, 100% private          │
└─────────────────────────────────────┘
```

---

## Common Issues & Solutions

### Issue 1: "Cannot connect to Ollama"

**Cause**: Ollama service not ready yet

**Solution**: Wait 30 seconds for model download to complete, then refresh browser

### Issue 2: "Error: API returned status 404"

**Cause**: Model not downloaded yet

**Solution**:
```bash
# Check Ollama logs
docker logs sme-ollama

# You should see: "Ollama ready with llama3.2 model"
```

### Issue 3: Slow responses (30+ seconds)

**Cause**: Normal for first query (model loading)

**Solution**: Subsequent queries will be faster (2-5 seconds)

### Issue 4: Out of memory error

**Cause**: Not enough RAM

**Solution**:
- Close other applications
- Increase Docker memory limit: Docker Desktop → Settings → Resources → Memory (12GB+)

---

## Stopping the Services

```bash
# Stop services (keeps data)
docker-compose down

# Stop and remove all data
docker-compose down -v
```

---

## Resource Usage

| Component | Disk | RAM | CPU |
|-----------|------|-----|-----|
| Ollama container | 500MB | 2GB | Low |
| llama3.2 model | 3GB | 4GB | Medium |
| Chatbot UI | 200MB | 500MB | Low |
| **Total** | **~4GB** | **~6.5GB** | **Low-Medium** |

---

## What's NOT in Phase 1

- ❌ Markdown file search (Phase 2)
- ❌ Knowledge graph (Phase 3)
- ❌ MCP server integration (Phase 3)
- ❌ Team collaboration features (Phase 3)
- ❌ Obsidian integration (Phase 2-3)

**This is intentional!** Phase 1 is about getting comfortable with a local LLM.

---

## Next Steps

Once you're comfortable with the chatbot:

### → [Phase 2: RAG Search](../../docs/phase-2-rag.md)

Add ability to search your markdown files and get answers based on your notes.

**What you'll add**:
- Markdown file ingestion
- Semantic search
- Source citations

**Time to implement**: ~10 minutes

---

## Customization

### Change the Model

Edit `docker-compose.yml`:

```yaml
command: >
  sh -c "ollama serve &
         sleep 15 &&
         ollama pull mistral &&  # ← Change this
         wait"
```

**Available models**:
- `llama3.2` (default, 3GB) - Good balance
- `mistral` (4GB) - Better quality
- `phi` (1.5GB) - Faster, less RAM
- See all: https://ollama.ai/library

### Change the Port

Edit `docker-compose.yml`:

```yaml
chatbot:
  ports:
    - "3000:8080"  # ← Access at localhost:3000
```

---

## Troubleshooting Commands

```bash
# View chatbot logs
docker logs sme-chatbot

# View Ollama logs
docker logs sme-ollama

# Restart everything
docker-compose restart

# Rebuild chatbot (if you changed code)
docker-compose up --build

# Check running containers
docker ps

# Check Docker resource usage
docker stats
```

---

## Data Persistence

**What's saved**:
- ✅ Downloaded model (in Docker volume `ollama-data`)
- ❌ Chat history (browser only, clears on refresh)

**To preserve chat history** → Wait for Phase 2 (saves to markdown files)

---

## Security Notes

- All processing happens **locally** on your machine
- No data sent to cloud services
- No API keys required
- No network access needed (after initial model download)
- Safe for confidential/proprietary information

---

## Support

**Issues?**
1. Check logs: `docker logs sme-chatbot` and `docker logs sme-ollama`
2. Restart: `docker-compose restart`
3. Full reset: `docker-compose down -v && docker-compose up`

**Need help?**
- GitHub Issues: https://github.com/pingwu/sme-knowledge-graph/issues
- Documentation: `../../docs/faq.md`

---

**Congratulations!** You now have a local AI chatbot running.

Next: Add RAG search to query your markdown files → [Phase 2 Guide](../../docs/phase-2-rag.md)
