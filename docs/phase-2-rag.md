# Phase 2: Semantic Search & RAG - Deployment Guide

**Subtitle:** *Intelligence - Teach AI About YOUR Knowledge*

This guide walks you through deploying Phase 2 of the SME Knowledge Graph, which adds Retrieval Augmented Generation (RAG) capabilities using ChromaDB vector database.

---

## What You'll Build

By the end of this guide, you'll have:
- ✅ **Phase 1 capabilities** (Local LLM chatbot)
- ✅ **ChromaDB vector database** for semantic search
- ✅ **Knowledge vault** indexed with your markdown files
- ✅ **RAG-powered chatbot** that answers questions with source citations

---

## Prerequisites

### From Phase 1
You should have completed Phase 1 or have:
- Docker Desktop installed and running
- Basic understanding of Docker commands
- 16GB RAM (minimum 8GB)

### New for Phase 2
- **Additional disk space**: +2GB for ChromaDB
- **Markdown files**: Your knowledge documents (or use provided samples)
- **Embedding model**: We'll download `nomic-embed-text` (274MB)

---

## Architecture Overview

### Phase 1 Architecture
```
┌─────────────────┐
│   Chatbot UI    │
│   (Streamlit)   │
└────────┬────────┘
         │
┌────────▼────────┐
│     Ollama      │
│  (llama3.2:1b)  │
└─────────────────┘
```

### Phase 2 Architecture (What We're Adding)
```
┌─────────────────────────────────────────────┐
│            Chatbot UI (Streamlit)           │
│  - Chat interface                           │
│  - Knowledge vault indexing                 │
│  - Source citation display                  │
└─────────┬──────────────────┬────────────────┘
          │                  │
┌─────────▼─────────┐  ┌────▼──────────────┐
│      Ollama       │  │    ChromaDB       │
│  - LLM inference  │  │  - Vector storage │
│  - Embeddings     │  │  - Semantic search│
└───────────────────┘  └───────────────────┘
          │                  │
          └────────┬─────────┘
                   │
          ┌────────▼────────┐
          │ Knowledge Vault │
          │ (Markdown files)│
          └─────────────────┘
```

**Key Concepts:**
- **Embeddings**: Converting text to numerical vectors that capture meaning
- **Vector Database**: Stores embeddings and enables similarity search
- **Semantic Search**: Find documents by meaning, not just keyword matching
- **RAG (Retrieval Augmented Generation)**: LLM + your documents = accurate, cited answers

---

## Step 1: Navigate to Phase 2 Directory

```bash
cd sme-knowledge-graph/deployments/phase-2-rag
```

**What's here:**
```
phase-2-rag/
├── docker-compose.yml       # 3 services: Ollama, ChromaDB, Chatbot
├── chatbot-ui/              # Enhanced UI with RAG
└── knowledge-vault/         # Your markdown files go here
    ├── README.md
    ├── sample-decision.md
    ├── sample-meeting-notes.md
    └── sample-technical-doc.md
```

---

## Step 2: Start the Services

```bash
docker compose up -d
```

**This starts 3 containers:**
1. **sme-ollama-phase2** - Local LLM (port 11434)
2. **sme-chromadb-phase2** - Vector database (port 8000)
3. **sme-chatbot-phase2** - Web UI (port 8080)

**Wait for services to be healthy** (~30 seconds):
```bash
docker compose ps
```

Expected output:
```
NAME                   STATUS
sme-ollama-phase2      Up (healthy)
sme-chromadb-phase2    Up (healthy)
sme-chatbot-phase2     Up
```

---

## Step 3: Download AI Models

### Download LLM Model (Same as Phase 1)

```bash
docker exec sme-ollama-phase2 ollama pull llama3.2:1b
```

**Download time**: ~2 minutes (1.3GB)

### Download Embedding Model (NEW for Phase 2)

```bash
docker exec sme-ollama-phase2 ollama pull nomic-embed-text
```

**Download time**: ~1 minute (274MB)

**Why this model?**
- **Optimized for markdown**: Trained on technical documentation
- **Fast**: 274M parameters (vs 1B for LLM)
- **High quality**: 768-dimensional embeddings
- **Local**: Runs 100% offline like everything else

**Verify both models downloaded:**
```bash
docker exec sme-ollama-phase2 ollama list
```

Expected output:
```
NAME                TAG       SIZE
llama3.2:1b         latest    1.3GB
nomic-embed-text    latest    274MB
```

---

## Step 4: Add Your Knowledge Files

### Option A: Use Sample Files (Recommended for Learning)

Sample files are already in `knowledge-vault/`:
- `sample-decision.md` - Database selection decision
- `sample-meeting-notes.md` - Weekly standup notes
- `sample-technical-doc.md` - PostgreSQL architecture

**These demonstrate:**
- Decision documentation
- Meeting notes capture
- Technical deep dives
- Source citations

### Option B: Add Your Own Files

```bash
# Copy your markdown files
cp ~/Documents/my-notes/*.md knowledge-vault/

# Or create a new file
cat > knowledge-vault/my-first-doc.md << 'EOF'
# My First Knowledge Document

## Context
This is a test document for RAG.

## Key Points
- Point 1: RAG enables source citations
- Point 2: Semantic search understands meaning
- Point 3: Works 100% offline

## Tags
#test #rag #learning
EOF
```

**Best practices:**
- Use clear headers (# ## ###)
- Include metadata (dates, tags, people)
- Keep files focused (one topic per file)
- Use descriptive filenames

---

## Step 5: Access the Chatbot

Open your browser: **http://localhost:8080**

You should see:
- **Header**: "SME Knowledge Chatbot - Phase 2"
- **Subtitle**: "Semantic Search & RAG"
- **Sidebar**: System status showing all services connected
- **Chat interface**: Ready for questions

**System Status Check:**
```
✅ Ollama: 🟢 Connected
✅ RAG Status: 🟢 Enabled
✅ ChromaDB: 🟢 Connected
```

---

## Step 6: Index Your Knowledge Vault

**In the chatbot sidebar**, you'll see "📚 Knowledge Vault" section.

1. Click **"🔄 Index Knowledge Vault"**
2. Wait for indexing (10-30 seconds depending on file count)
3. You'll see: "✅ Indexed X documents!"

**What's happening:**
1. Chatbot reads all `.md` files in `knowledge-vault/`
2. Each file is converted to embeddings using `nomic-embed-text`
3. Embeddings are stored in ChromaDB with metadata (filename, path)
4. Now your documents are searchable by meaning!

**Re-indexing:**
- Add new files → Click "Index" again
- Edit existing files → Re-index to update
- No duplicates → ChromaDB updates existing entries

---

## Step 7: Test Semantic Search

### Try These Sample Queries

**Using sample files:**

1. **"What did we decide about the database?"**
   - Should cite `sample-decision.md`
   - Answer: PostgreSQL selection

2. **"Why did we choose PostgreSQL?"**
   - Semantic search (not exact keywords)
   - Should explain: reliability, features, compliance

3. **"Who was involved in the database decision?"**
   - Should extract: John Smith, Sarah Johnson, Mike Chen

4. **"What were the risks mentioned in meetings?"**
   - Should cite `sample-meeting-notes.md`
   - Answer: Test data, Docker licensing, PostgreSQL training

### Semantic Search vs Keyword Search

**❌ Traditional keyword search:**
Query: "database decision"
Finds: Only docs with exact words "database" AND "decision"

**✅ Semantic search (Phase 2):**
Query: "Why did we pick that data storage technology?"
Finds: `sample-decision.md` (understands synonyms: pick=choose, data storage=database)

---

## Step 8: Understand Source Citations

When the chatbot answers using RAG, you'll see:

```markdown
[AI Answer based on your documents]

---
**Sources:**
1. `sample-decision.md`
2. `sample-meeting-notes.md`
```

**Why citations matter:**
- **Verifiable**: You can check the source
- **Transparent**: Know where AI got information
- **Trustworthy**: Not hallucinated, grounded in your docs

---

## Troubleshooting

### Issue 1: ChromaDB shows "🔴 Disconnected"

**Check if ChromaDB is running:**
```bash
docker compose ps
```

**If not running:**
```bash
docker compose up -d chromadb
```

**Check ChromaDB logs:**
```bash
docker compose logs chromadb
```

### Issue 2: Indexing fails

**Common causes:**
1. **No markdown files**: Add at least one `.md` file to `knowledge-vault/`
2. **Embedding model not downloaded**: Run `ollama pull nomic-embed-text`
3. **ChromaDB not ready**: Wait 10 seconds after `docker compose up`

**Debug:**
```bash
# Check knowledge vault has files
ls knowledge-vault/

# Check embedding model
docker exec sme-ollama-phase2 ollama list | grep nomic

# Restart services
docker compose restart
```

### Issue 3: Search returns no results

**Possible reasons:**
1. **Not indexed yet**: Click "Index Knowledge Vault" first
2. **Query too specific**: Try broader questions
3. **Empty files**: Make sure markdown files have content

**Test indexing:**
```bash
# Check ChromaDB has data
docker exec sme-chromadb-phase2 curl http://localhost:8000/api/v1/collections
```

### Issue 4: Slow responses

**Expected performance:**
- **Indexing**: 1-3 seconds per document
- **Search**: 2-5 seconds (embedding + vector search)
- **Answer generation**: 5-15 seconds (depends on LLM model)

**Speed improvements:**
- Use smaller files (< 5000 chars per file)
- Reduce `n_results` in search (default: 3)
- Upgrade to faster model if needed

### Issue 5: Out of memory

**Phase 2 memory usage:**
- Ollama: ~2GB (LLM + embedding model)
- ChromaDB: ~500MB (for 100 docs)
- Chatbot: ~200MB
- **Total**: ~3-4GB

**If system is slow:**
1. Close other applications
2. Restart Docker Desktop
3. Increase Docker memory limit (Settings → Resources)

---

## Understanding the Technology

### What Are Embeddings?

**Analogy: GPS Coordinates for Meaning**

Just like GPS represents location as numbers:
- San Francisco: `[37.77, -122.42]`
- New York: `[40.71, -74.01]`

Embeddings represent meaning as numbers:
- "frustrated": `[0.23, -0.47, 0.81, ..., 0.15]` (768 dimensions)
- "unhappy": `[0.25, -0.45, 0.79, ..., 0.18]` ← Close to "frustrated"!

**Distance = Similarity:**
- Small distance → Similar meaning
- Large distance → Different meaning

### How RAG Works (Step by Step)

**1. Indexing (One-time per document):**
```
Your document → Embedding Model → Vector (768 numbers) → ChromaDB
```

**2. Query (Every question):**
```
Your question → Embedding Model → Query Vector
Query Vector → ChromaDB.search() → Top 3 similar documents
Documents + Question → LLM → Answer with citations
```

**Example:**
```
Q: "Why did we choose PostgreSQL?"

Step 1: Convert question to embedding [0.12, -0.34, ...]
Step 2: ChromaDB finds similar doc: sample-decision.md
Step 3: LLM reads: question + sample-decision.md
Step 4: Answer: "PostgreSQL was chosen for reliability,
        feature set, and team expertise. Source: sample-decision.md"
```

### Why Vector Databases? (vs Traditional SQL)

**SQL Keyword Search:**
```sql
SELECT * FROM documents
WHERE content LIKE '%PostgreSQL%';
```
- Finds exact word "PostgreSQL"
- Misses: "database", "Postgres", "RDBMS"

**Vector Similarity Search:**
```python
chromadb.query(
    query_embeddings=[question_vector],
    n_results=3
)
```
- Finds documents with similar *meaning*
- Captures: synonyms, related concepts, context

---

## Next Steps

### Phase 2 Complete! What Can You Do Now?

✅ **Local AI with memory** - Ask about YOUR documents
✅ **Semantic search** - Find by meaning, not keywords
✅ **Source citations** - Verifiable, grounded answers
✅ **100% private** - No cloud, no data leakage

### Continue to Phase 3: Knowledge Graph

**Phase 3 adds:**
- **Neo4j graph database** - Relationship mapping
- **Entity extraction** - Automatic person/company/decision detection
- **Graph queries** - "How are these concepts connected?"
- **MCP integration** - AI agents can query your knowledge graph

**When to move to Phase 3:**
- You're comfortable with RAG concepts
- You want to understand *relationships* between entities
- You need multi-perspective context (Engineering vs Sales view)
- You want to see "decision trails" (Customer need → Tech choice → Implementation)

---

## Cleanup (Optional)

### Stop Services (Keep data)
```bash
docker compose down
```
**Preserves:**
- Ollama models (in Docker volume)
- ChromaDB indexed data (in Docker volume)
- Knowledge vault files (local directory)

### Start Again
```bash
docker compose up -d
```
Everything comes back exactly as you left it!

### Complete Removal (Delete everything)
```bash
docker compose down -v
```
**Deletes:**
- All containers
- All volumes (models, ChromaDB data)

**Keeps:**
- Your knowledge vault files (safe!)
- docker-compose.yml

---

## Advanced Configuration

### Change LLM Model

**For better quality** (but slower):
```yaml
# docker-compose.yml
environment:
  - MODEL_NAME=llama3.2:3b  # or llama3:8b
```

Then:
```bash
docker exec sme-ollama-phase2 ollama pull llama3.2:3b
docker compose up -d --build chatbot
```

### Change Number of Search Results

More results = more context, but slower:

```python
# In chatbot-ui/app.py
search_results = search_knowledge_vault(query, n_results=5)  # default: 3
```

### Add More Knowledge Vaults

```yaml
# docker-compose.yml
volumes:
  - ./knowledge-vault:/knowledge-vault:ro
  - ./work-notes:/work-notes:ro  # Add second vault
```

---

## Learning Outcomes

After completing Phase 2, you should understand:

- ✅ What vector databases are and why they matter
- ✅ How embeddings represent semantic meaning
- ✅ Difference between keyword search and semantic search
- ✅ How RAG combines retrieval with generation
- ✅ Why source citations make AI trustworthy
- ✅ Industry shift from SEO → GEO (keyword → semantic)

**Real-world application:**
- Personal knowledge management
- Team documentation search
- Customer support knowledge base
- Technical documentation Q&A
- Decision history tracking

---

## Related Documentation

- [Phase 2 PRD](phase-2-rag-PRD.md) - Product requirements
- [Architecture: Vector Databases & GEO](ARCHITECTURE-VECTOR-DATABASES-AND-GEO.md) - Deep dive
- [Model Management Guide](MODEL-MANAGEMENT-GUIDE.md) - Switching models
- [Docker DNS Guide](DOCKER-SERVICE-DNS-TEACHING-NOTE.md) - Container networking

---

## Support

**Issues?**
- GitHub Issues: https://github.com/pingwu/sme-knowledge-graph/issues
- Discussions: https://github.com/pingwu/sme-knowledge-graph/discussions

**Questions about concepts?**
- Vector databases: See [Architecture doc](ARCHITECTURE-VECTOR-DATABASES-AND-GEO.md)
- RAG: See [Phase 2 PRD](phase-2-rag-PRD.md)
- Embeddings: See "Understanding the Technology" section above

---

**Congratulations!** You now have a local AI assistant that understands YOUR knowledge, provides verifiable answers, and runs 100% offline.

Ready for Phase 3? Let's add relationship intelligence with knowledge graphs! 🚀
