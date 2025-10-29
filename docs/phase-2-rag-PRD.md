# Phase 2: RAG Search - Product Requirements Document

**Project**: SME Knowledge Graph
**Phase**: 2 - Retrieval Augmented Generation (RAG)
**Status**: In Development
**Date**: 2025-10-27
**Owner**: Ping Wu

---

## Executive Summary

Phase 2 adds **Retrieval Augmented Generation (RAG)** to the SME Knowledge Graph, enabling the chatbot to search through your markdown knowledge vault and answer questions with sources. This transforms the basic chatbot from Phase 1 into a **context-aware knowledge assistant** that can recall information from your documents.

**Business Value:**
- **Reduced knowledge search time** (21% of work time → near instant)
- **Context preservation** across team members and time
- **Decision support** with source citations
- **Knowledge retention** when SMEs leave

**Technical Achievement:**
- Vector search with semantic understanding (not just keyword matching)
- Local ChromaDB deployment (no cloud dependencies)
- Markdown file indexing and retrieval
- Source attribution for AI responses

---

## Problem Statement

### Current State (Phase 1 Limitations)

**What Phase 1 Does:**
- Basic chatbot with conversational AI
- General knowledge from LLM training
- No access to your specific documents

**What Phase 1 Cannot Do:**
- ❌ Answer questions about YOUR documents
- ❌ Recall specific decisions documented in markdown files
- ❌ Provide source citations
- ❌ Search across your knowledge vault
- ❌ Connect information from multiple documents

### Real-World Scenario

**Without RAG (Phase 1):**
```
User: "Why did we choose PostgreSQL over MongoDB for the Acme project?"

Chatbot: "PostgreSQL is a relational database known for ACID compliance and
structured data. MongoDB is a NoSQL database good for flexible schemas."
```
**Problem:** Generic answer, doesn't know YOUR specific decision context.

**With RAG (Phase 2):**
```
User: "Why did we choose PostgreSQL over MongoDB for the Acme project?"

Chatbot: "Based on your project notes, you chose PostgreSQL because:
1. Acme's compliance requirements needed ACID transactions
2. Existing team expertise in SQL reduced training costs
3. Integration with current analytics stack was smoother

Sources:
- acme-project/architecture-decision.md (lines 45-67)
- acme-project/vendor-evaluation.md (lines 23-34)"
```
**Solution:** Specific answer based on YOUR documents with source citations.

---

## Success Metrics

### Learning Objectives (Student Perspective)

**By completing Phase 2, students will be able to:**
1. ✅ Explain what RAG is and why it's valuable for knowledge management
2. ✅ Deploy [[ChromaDB]] [[vector database]] with Docker
3. ✅ Understand vector embeddings and semantic search concepts
4. ✅ Index markdown files into a vector database
5. ✅ Query knowledge vault using natural language
6. ✅ Interpret source citations and verify AI responses
7. ✅ Compare keyword search vs. semantic search
8. ✅ Understand privacy benefits of local RAG (vs. cloud solutions)

### Technical Success Criteria

**Phase 2 is successful when:**
- [ ] [[ChromaDB]] container runs and passes healthcheck
- [ ] Markdown files are indexed with embeddings
- [ ] Chatbot can retrieve relevant documents for queries
- [ ] Responses include source citations (file + line numbers)
- [ ] Search uses semantic similarity (not just keywords)
- [ ] All components run 100% locally (no cloud API calls)
- [ ] Deployment time: < 15 minutes (including model downloads)
- [ ] Works with Phase 1 models (`llama3.2:1b` or `llama3.2:3b`)

### Business Value Metrics

**For Individual Contributors:**
- **Knowledge search time**: 21% work time → < 5 minutes per query
- **Context recall**: Manual document searching → instant semantic search
- **Decision transparency**: "Why did we decide X?" answerable with sources

**For Teams:**
- **Onboarding acceleration**: New members find context without asking everyone
- **Knowledge preservation**: SME departure doesn't lose institutional knowledge
- **Cross-functional alignment**: Engineering + Sales + Product context in one place

**For Enterprise:**
- **ROI**: $2.4B annual knowledge mismanagement cost reduction
- **Compliance**: Local deployment = no data governance concerns
- **Scalability**: Same solution works for 1 person → 10,000 documents

---

## User Stories

### US-1: Index Existing Knowledge Vault
**As a** knowledge worker
**I want to** index my existing markdown files into the vector database
**So that** the chatbot can search through my documented knowledge

**Acceptance Criteria:**
- [ ] Command to index entire knowledge-vault directory
- [ ] Progress indicator during indexing
- [ ] Confirmation message showing number of documents indexed
- [ ] Error handling for invalid markdown files
- [ ] Re-indexing capability (updates without duplicates)

**Technical Notes:**
- Use [[ChromaDB]] collection for document storage
- Embedding model: `nomic-embed-text` (recommended for markdown)
- Chunk strategy: Split by paragraphs/sections (not arbitrary character limits)
- Metadata: Store file path, line numbers, headers for citation

---

### US-2: Semantic Search Through Documents
**As a** knowledge worker
**I want to** ask questions about my documents in natural language
**So that** I can find relevant information without keyword guessing

**Acceptance Criteria:**
- [ ] Natural language query in chatbot
- [ ] Semantic search retrieves top-K relevant chunks (K=5 default)
- [ ] Results ranked by similarity score
- [ ] Related documents surfaced even if keywords don't match
- [ ] Context window includes surrounding text (not just matched chunk)

**Example:**
- **Query:** "customer complaints about performance"
- **Matches:** Documents mentioning "client frustration with speed", "user feedback on latency", "slow response time issues"
- **Note:** Finds semantically similar content, not just keyword "complaint"

---

### US-3: Source Attribution
**As a** knowledge worker
**I want to** see which documents the AI used to answer my question
**So that** I can verify accuracy and find related context

**Acceptance Criteria:**
- [ ] Every RAG-based response includes source citations
- [ ] Citation format: `filename.md (lines X-Y)` or `filename.md (section: Header)`
- [ ] Clickable links to source files (if file paths are accessible)
- [ ] Distinction between RAG-retrieved knowledge vs. general LLM knowledge
- [ ] Confidence indicator (optional): "High confidence (3 sources)" vs "Low confidence (1 source)"

**Example Citation Format:**
```
Answer: PostgreSQL was chosen for ACID compliance and team expertise.

Sources:
📄 projects/acme/architecture-decision.md (lines 45-67)
📄 projects/acme/vendor-evaluation.md (lines 23-34)
📄 team/engineering-skills-audit.md (lines 78-82)
```

---

### US-4: Knowledge Vault Management
**As a** knowledge worker
**I want to** add, update, and remove documents from the searchable knowledge vault
**So that** the chatbot always has current information

**Acceptance Criteria:**
- [ ] Add new markdown files → automatic re-indexing (or manual trigger)
- [ ] Update existing files → detect changes, re-embed modified sections
- [ ] Delete files → remove from vector database
- [ ] Vault statistics: X documents, Y total chunks, Z total tokens
- [ ] Last indexed timestamp shown

**Technical Notes:**
- Watch directory for changes (optional: file watcher)
- Incremental indexing (don't re-index unchanged files)
- Version tracking (detect file modifications by hash or mtime)

---

### US-5: Compare Search Methods
**As a** student learning RAG
**I want to** compare keyword search vs. semantic search results
**So that** I understand why vector embeddings are valuable

**Acceptance Criteria:**
- [ ] Toggle between "Keyword Search" and "Semantic Search" modes
- [ ] Side-by-side results comparison (optional teaching feature)
- [ ] Explanation of why semantic search found different results
- [ ] Example queries that demonstrate semantic advantage

**Example Teaching Moment:**
```
Query: "Why are customers frustrated?"

Keyword Search:
- ❌ Finds only documents containing "frustrated"

Semantic Search:
- ✅ Finds: "client dissatisfaction", "user complaints", "negative feedback"
- Explanation: Embeddings understand "frustrated" ≈ "dissatisfied" ≈ "unhappy"
```

---

## Technical Architecture

### System Components

```
┌──────────────────────────────────────────────────────────┐
│  Web UI (Streamlit)                                      │
│  - Chat interface                                        │
│  - RAG toggle (enable/disable)                          │
│  - Source citation display                               │
│  - Index management UI                                   │
└─────────┬────────────────────────────────────────────────┘
          │
          ├─────► Ollama (LLM)
          │       - llama3.2:1b (text generation)
          │       - nomic-embed-text (embeddings)
          │
          └─────► ChromaDB (Vector Database)
                  - Document storage
                  - Vector search
                  - Metadata (file paths, line numbers)

┌──────────────────────────────────────────────────────────┐
│  Knowledge Vault (Markdown Files)                       │
│  - ./knowledge-vault/ directory                         │
│  - Mounted as read-only volume                          │
│  - Student provides their own documents                  │
└──────────────────────────────────────────────────────────┘
```

### Data Flow: RAG Query

```
1. User Query
   ↓
2. Embed query using nomic-embed-text
   ↓
3. ChromaDB vector search (top-K similar chunks)
   ↓
4. Retrieve document chunks + metadata
   ↓
5. Build prompt: Context + User Query
   ↓
6. LLM generates answer with sources
   ↓
7. Display answer + citations in UI
```

### Docker Services

**Phase 2 Adds:**
- `chromadb` service (vector database)
- `knowledge-vault` volume mount (markdown files)
- Updated `chatbot` with RAG capabilities

**Port Allocation:**
- `8080` - Web UI (same as Phase 1)
- `11434` - Ollama API (same as Phase 1)
- `8000` - ChromaDB API (new)

**Container Names:**
- `sme-ollama-phase2`
- `sme-chromadb-phase2`
- `sme-chatbot-phase2`

**Note:** Phase 2 containers use different names than Phase 1 to allow side-by-side comparison.

---

## Implementation Plan

### Milestone 1: ChromaDB Integration (Week 1)

**Tasks:**
- [ ] Add ChromaDB service to docker-compose.yml
- [ ] Configure persistent volume for ChromaDB data
- [ ] Add healthcheck for ChromaDB service
- [ ] Update chatbot service dependencies

**Deliverable:** ChromaDB runs and passes healthcheck

---

### Milestone 2: Embedding & Indexing (Week 1-2)

**Tasks:**
- [ ] Download `nomic-embed-text` embedding model
- [ ] Write indexing script (Python)
  - Read markdown files from knowledge-vault
  - Split into semantic chunks (by paragraph/section)
  - Generate embeddings
  - Store in ChromaDB with metadata
- [ ] Add indexing command to chatbot UI
- [ ] Create sample knowledge vault (5-10 markdown files)

**Deliverable:** Markdown files indexed into ChromaDB

---

### Milestone 3: RAG Query Pipeline (Week 2)

**Tasks:**
- [ ] Implement vector search in chatbot app
- [ ] Build RAG prompt template (context + query)
- [ ] Add source citation formatting
- [ ] Test with sample queries
- [ ] Handle edge cases (no results, low confidence)

**Deliverable:** Chatbot answers questions using RAG

---

### Milestone 4: UI Enhancements (Week 2-3)

**Tasks:**
- [ ] Add RAG toggle (enable/disable)
- [ ] Display source citations in sidebar
- [ ] Show vault statistics (X docs, Y chunks)
- [ ] Add indexing progress indicator
- [ ] Create "How RAG Works" teaching section

**Deliverable:** Student-friendly RAG interface

---

### Milestone 5: Documentation & Testing (Week 3)

**Tasks:**
- [ ] Write phase-2-rag.md deployment guide
- [ ] Create troubleshooting section
- [ ] Test with Phase 1 models (llama3.2:1b, llama3.2:3b)
- [ ] Measure deployment time (< 15 minutes target)
- [ ] Create student exercise examples

**Deliverable:** Complete Phase 2 ready for students

---

## Technical Specifications

### Embedding Model Selection

**Recommended: `nomic-embed-text`**
- **Size:** 274M parameters (relatively small)
- **Context length:** 8192 tokens
- **Performance:** Best for markdown/documentation
- **License:** Apache 2.0
- **Download:** `ollama pull nomic-embed-text`

**Alternative: `mxbai-embed-large`**
- **Size:** 335M parameters
- **Context length:** 512 tokens
- **Performance:** Good for short queries
- **Use case:** If embedding speed is critical

### Chunking Strategy

**Approach: Semantic Chunking (Recommended)**
- Split by markdown headers (H1, H2, H3)
- Preserve code blocks as single chunks
- Maximum chunk size: 512 tokens
- Overlap: 50 tokens between chunks

**Metadata Stored:**
```python
{
  "file_path": "projects/acme/architecture-decision.md",
  "line_start": 45,
  "line_end": 67,
  "header": "Database Selection",
  "chunk_index": 3,
  "total_chunks": 12
}
```

### ChromaDB Configuration

**Collection Settings:**
```python
collection = client.create_collection(
    name="knowledge_vault",
    metadata={"hnsw:space": "cosine"},  # Cosine similarity
    embedding_function=embedding_function
)
```

**Performance:**
- In-memory index with disk persistence
- Supports 10,000+ documents on 8GB RAM
- Query time: < 100ms for most queries

---

## Non-Functional Requirements

### Performance

**Indexing Performance:**
- **Target:** 100 documents (10MB) indexed in < 5 minutes
- **Bottleneck:** Embedding generation (CPU-bound)
- **Optimization:** Batch embedding (10-50 chunks at a time)

**Query Performance:**
- **Target:** < 3 seconds end-to-end (search + LLM generation)
- **Breakdown:**
  - Vector search: < 100ms
  - LLM generation: 2-4 seconds (CPU)
- **User experience:** Show "Searching..." and "Generating..." states

### Scalability

**Small Scale (Phase 2 Target):**
- 100-500 markdown files
- 1,000-5,000 embedded chunks
- 8GB RAM sufficient

**Medium Scale (Future):**
- 1,000-5,000 markdown files
- 10,000-50,000 embedded chunks
- 16GB RAM recommended

**Note:** Neo4j (Phase 3) handles larger scale and relationship queries

### Privacy & Security

**Data Locality:**
- ✅ All processing happens locally
- ✅ No embeddings sent to cloud APIs
- ✅ ChromaDB data persists only on user's machine
- ✅ Knowledge vault never leaves local environment

**Access Control:**
- Knowledge vault mounted as read-only
- ChromaDB data directory owned by container user
- No external network access required

### Reliability

**Error Handling:**
- Graceful degradation if ChromaDB unavailable (fall back to Phase 1)
- Clear error messages for indexing failures
- Healthcheck ensures ChromaDB running before chatbot starts

**Data Durability:**
- ChromaDB data persisted to Docker volume
- Survives container restarts
- Manual backup: copy `chromadb-data` volume

---

## User Experience

### First-Time Setup (Student Flow)

1. **Clone Phase 2 folder**
   ```bash
   cd deployments/phase-2-rag
   ```

2. **Create knowledge vault directory**
   ```bash
   mkdir knowledge-vault
   # Add some markdown files
   ```

3. **Start services**
   ```bash
   docker compose up -d
   ```

4. **Download embedding model** (one-time)
   ```bash
   docker exec sme-ollama-phase2 ollama pull nomic-embed-text
   ```

5. **Index knowledge vault** (in UI)
   - Click "Index Knowledge Vault" button
   - Wait 2-5 minutes
   - See confirmation: "Indexed 47 chunks from 12 documents"

6. **Ask questions**
   - Toggle "Enable RAG" on
   - Ask: "What did we discuss about PostgreSQL?"
   - See answer with source citations

### Iterative Development Flow

**Adding New Documents:**
1. Add markdown file to `knowledge-vault/`
2. Click "Re-index" in UI
3. New documents immediately searchable

**Updating Existing Documents:**
1. Edit markdown file in `knowledge-vault/`
2. Click "Re-index" in UI
3. Updated content reflected in search

---

## Risks & Mitigation

### Risk 1: Embedding Model Too Large
**Impact:** Students with 8GB RAM can't run Phase 2

**Mitigation:**
- Use smallest embedding model (`nomic-embed-text` 274M)
- Fall back to Phase 1 LLM if embedding model unavailable
- Document RAM requirements clearly

### Risk 2: Indexing Takes Too Long
**Impact:** Student loses interest waiting for indexing

**Mitigation:**
- Start with small sample vault (5-10 documents)
- Show progress indicator with ETA
- Teach incremental indexing (don't re-index everything)
- Batch embedding for speed

### Risk 3: RAG Quality Issues
**Impact:** Chatbot gives wrong answers or irrelevant sources

**Mitigation:**
- Show source citations (student can verify)
- Add confidence indicator (high/medium/low)
- Allow disabling RAG (fall back to Phase 1)
- Teach students to evaluate RAG quality

### Risk 4: Port Conflicts with Phase 1
**Impact:** Can't run Phase 1 and Phase 2 simultaneously

**Mitigation:**
- Use different container names (`-phase2` suffix)
- Document: "Stop Phase 1 before starting Phase 2"
- Future: Make ports configurable via .env

---

## Future Enhancements (Not Phase 2)

**Phase 2 Scope:**
- Basic RAG with vector search
- Source citations
- Markdown file indexing

**Out of Scope (Future Phases):**
- [ ] Graph relationships (Phase 3: Neo4j)
- [ ] Multi-turn conversation with RAG context
- [ ] Filtering by metadata (date, author, tags)
- [ ] Hybrid search (keyword + semantic)
- [ ] Re-ranking search results
- [ ] Document similarity recommendations
- [ ] Automatic summarization of large documents

---

## Success Definition

**Phase 2 is ready for students when:**

1. ✅ **Deployment**: `docker compose up -d` → all services healthy in < 5 minutes
2. ✅ **Indexing**: Sample vault (10 docs) indexed in < 3 minutes
3. ✅ **Query**: "Why did we choose X?" returns answer with sources in < 5 seconds
4. ✅ **Documentation**: Step-by-step guide + troubleshooting
5. ✅ **Comparison**: Students can compare Phase 1 (no RAG) vs Phase 2 (with RAG)
6. ✅ **Learning**: Student understands vector embeddings, semantic search, RAG value

**Validation Queries:**
- "What are the advantages of PostgreSQL?" → Retrieves relevant docs
- "Why did customers complain?" → Semantic match (not just keyword "complain")
- "Summary of Acme project decisions" → Multi-document synthesis

---

## Appendix A: Technology Choices

### Why ChromaDB?

**Alternatives Considered:**
- Qdrant: More features, heavier
- Weaviate: Production-grade, complex setup
- FAISS: Library not service, harder for students

**ChromaDB Selected Because:**
- ✅ Simplest Docker deployment
- ✅ Python-native (matches student skill level)
- ✅ Good documentation
- ✅ Sufficient for Phase 2 scale (< 10K documents)

### Why `nomic-embed-text`?

**Alternatives Considered:**
- OpenAI `text-embedding-ada-002`: Cloud API (violates privacy)
- Sentence-Transformers `all-MiniLM-L6-v2`: No Ollama support

**nomic-embed-text Selected Because:**
- ✅ Available in Ollama (consistent tooling)
- ✅ Optimized for markdown/documentation
- ✅ Small enough for 8GB RAM
- ✅ Apache 2.0 license (permissive)

---

## Appendix B: Learning Resources

**For Students:**
- [What is RAG?](https://www.pinecone.io/learn/retrieval-augmented-generation/) - Pinecone guide
- [Vector Embeddings Explained](https://www.youtube.com/watch?v=viZrOnJclY0) - Video (3Blue1Brown style)
- [ChromaDB Getting Started](https://docs.trychroma.com/getting-started) - Official docs

**For Implementation:**
- [Ollama Embeddings API](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-embeddings)
- [ChromaDB Python Client](https://docs.trychroma.com/usage-guide)
- [Streamlit File Upload](https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader)

---

**Document Status:** Draft
**Last Updated:** 2025-10-27
**Next Review:** After Milestone 1 completion
**Owner:** Ping Wu
