# Phase 2 Quick Start Guide

**Get Phase 2 running in 5 commands** (10 minutes)

---

## Prerequisites

- ✅ Docker Desktop installed and running
- ✅ 16GB RAM recommended (8GB minimum)
- ✅ 5GB free disk space

---

## Quick Start Commands

```bash
# 1. Navigate to Phase 2
cd sme-knowledge-graph/deployments/phase-2-rag

# 2. Start all services (Ollama + ChromaDB + Chatbot)
docker compose up -d

# 3. Download LLM model (~2 minutes, 1.3GB)
docker exec sme-ollama-phase2 ollama pull llama3.2:1b

# 4. Download embedding model (~1 minute, 274MB) - NEW for Phase 2
docker exec sme-ollama-phase2 ollama pull nomic-embed-text

# 5. Verify models downloaded
docker exec sme-ollama-phase2 ollama list
```

**Expected output:**
```
NAME                TAG       SIZE
llama3.2:1b         latest    1.3GB
nomic-embed-text    latest    274MB
```

---

## Access the Application

**Open browser:** http://localhost:8080

**You should see:**
- "SME Knowledge Chatbot - Phase 2"
- System status: All 🟢 Connected
- Sidebar with "📚 Knowledge Vault" section

---

## Index Sample Knowledge

**In the chatbot sidebar:**

1. Click **"🔄 Index Knowledge Vault"**
2. Wait ~10 seconds
3. See: "✅ Indexed 3 documents!"

**Sample files included:**
- `sample-decision.md` - Database selection decision
- `sample-meeting-notes.md` - Weekly standup
- `sample-technical-doc.md` - PostgreSQL architecture

---

## Test Semantic Search

Try these queries in the chatbot:

1. **"What did we decide about the database?"**
   - Should cite `sample-decision.md`
   - Answer: PostgreSQL selected

2. **"Why did we choose PostgreSQL?"**
   - Tests semantic understanding (not exact keywords)
   - Should explain: reliability, features, compliance

3. **"Who was involved in database decisions?"**
   - Should extract: John Smith, Sarah Johnson, Mike Chen

4. **"What were the main risks discussed?"**
   - Should cite `sample-meeting-notes.md`
   - Answer: Test data, Docker licensing, training gaps

**Notice:**
- ✅ Answers include source citations
- ✅ Semantic search (understands synonyms)
- ✅ Works with sample files immediately

---

## What's Different from Phase 1?

| Feature | Phase 1 | Phase 2 |
|---------|---------|---------|
| **Knowledge** | LLM training data only | LLM + YOUR documents |
| **Search** | N/A | Semantic vector search |
| **Citations** | N/A | Source file references |
| **Database** | None | ChromaDB (vector DB) |
| **Models** | 1 (LLM only) | 2 (LLM + embeddings) |

---

## Troubleshooting

### ChromaDB shows disconnected

```bash
# Check service status
docker compose ps

# Restart ChromaDB
docker compose restart chromadb

# Check logs
docker compose logs chromadb
```

### Indexing fails

```bash
# Verify embedding model downloaded
docker exec sme-ollama-phase2 ollama list | grep nomic

# If missing, download it
docker exec sme-ollama-phase2 ollama pull nomic-embed-text
```

### No search results

1. Click "🔄 Index Knowledge Vault" first
2. Wait for "✅ Indexed X documents!"
3. Then try searching

---

## Add Your Own Knowledge

```bash
# Navigate to knowledge vault
cd knowledge-vault

# Add your markdown files
cp ~/my-notes/*.md .

# Or create a new file
cat > my-document.md << 'EOF'
# My Knowledge Document

## Key Information
- Point 1: RAG enables source citations
- Point 2: Semantic search understands meaning

## Tags
#personal #knowledge #rag
EOF

# Re-index in chatbot UI
# Click "🔄 Index Knowledge Vault"
```

---

## Stop Services

```bash
# Stop (keeps data)
docker compose down

# Start again later
docker compose up -d
```

**Your data persists:**
- ✅ Downloaded models (Ollama volume)
- ✅ Indexed documents (ChromaDB volume)
- ✅ Knowledge vault files (local directory)

---

## Next Steps

### Option 1: Learn the Concepts

Read: [docs/phase-2-rag.md](phase-2-rag.md) - Full deployment guide with explanations

**You'll learn:**
- What are vector databases?
- How do embeddings work?
- Semantic search vs keyword search
- Industry shift: SEO → GEO

### Option 2: Continue to Phase 3

**Phase 3 adds:**
- Neo4j knowledge graph
- Relationship mapping (people, companies, decisions)
- Graph traversal queries
- MCP server integration

---

## Model Downloads Reference

### LLM Models (Choose one)

```bash
# Fast (recommended for learning)
docker exec sme-ollama-phase2 ollama pull llama3.2:1b    # 1.3GB, fast

# Better quality
docker exec sme-ollama-phase2 ollama pull llama3.2:3b    # 2.0GB, slower
docker exec sme-ollama-phase2 ollama pull llama3:8b      # 4.7GB, best
```

### Embedding Model (Required for Phase 2)

```bash
# This is required - don't skip!
docker exec sme-ollama-phase2 ollama pull nomic-embed-text  # 274MB
```

**Why nomic-embed-text?**
- Optimized for markdown/documentation
- 768-dimensional embeddings
- Fast (274M parameters)
- Works great with technical content

### Check Downloaded Models

```bash
docker exec sme-ollama-phase2 ollama list
```

---

## Quick Commands Cheat Sheet

```bash
# Start services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f chatbot    # Chatbot logs
docker compose logs -f chromadb   # ChromaDB logs
docker compose logs -f ollama     # Ollama logs

# Stop services (keep data)
docker compose down

# Stop and delete everything
docker compose down -v

# Download models
docker exec sme-ollama-phase2 ollama pull <model-name>

# List models
docker exec sme-ollama-phase2 ollama list

# Restart specific service
docker compose restart chatbot
```

---

## Support

- **Full guide**: [docs/phase-2-rag.md](phase-2-rag.md)
- **Architecture deep dive**: [docs/ARCHITECTURE-VECTOR-DATABASES-AND-GEO.md](ARCHITECTURE-VECTOR-DATABASES-AND-GEO.md)
- **GitHub Issues**: https://github.com/pingwu/sme-knowledge-graph/issues

---

**Total time:** 10 minutes
**Result:** Local AI that understands YOUR knowledge with source citations! 🚀
