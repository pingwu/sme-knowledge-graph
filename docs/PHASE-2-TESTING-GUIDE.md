# Phase 2 Testing Guide

**Comprehensive testing checklist for validating Phase 2 (RAG) deployment**

This guide helps you verify that Phase 2 is working correctly before students use it.

---

## Testing Overview

**What We're Testing:**
- ✅ Docker services start and stay healthy
- ✅ Models download successfully
- ✅ ChromaDB accepts connections
- ✅ Knowledge vault indexing works
- ✅ Semantic search returns relevant results
- ✅ Source citations appear correctly
- ✅ Error handling works properly

**Time Required:** 15-20 minutes

---

## Pre-Flight Checklist

Before starting tests, ensure:

```bash
# 1. Docker Desktop is running
docker --version
# Expected: Docker version 20.10+ or higher

# 2. You're in the correct directory
cd sme-knowledge-graph/deployments/phase-2-rag
pwd
# Expected: .../sme-knowledge-graph/deployments/phase-2-rag

# 3. Clean slate (optional - removes old containers/volumes)
docker compose down -v
```

---

## Test Suite 1: Service Health

### Test 1.1: Start All Services

```bash
docker compose up -d
```

**Expected Output:**
```
[+] Running 4/4
 ✔ Network phase-2-rag_sme-network       Created
 ✔ Container sme-ollama-phase2           Started
 ✔ Container sme-chromadb-phase2         Started
 ✔ Container sme-chatbot-phase2          Started
```

**✅ PASS Criteria:**
- All 3 containers start without errors
- Network created successfully
- Command completes in < 30 seconds

**❌ FAIL Indicators:**
- Error messages during startup
- Containers exit immediately
- Port conflicts (8000, 8080, 11434 already in use)

**Troubleshooting:**
```bash
# Check for port conflicts
netstat -ano | findstr "8000"   # Windows
lsof -i :8000                   # Mac/Linux

# View startup logs
docker compose logs
```

---

### Test 1.2: Verify Service Health

Wait 30 seconds for health checks, then:

```bash
docker compose ps
```

**Expected Output:**
```
NAME                   STATUS
sme-ollama-phase2      Up 30 seconds (healthy)
sme-chromadb-phase2    Up 30 seconds (healthy)
sme-chatbot-phase2     Up 30 seconds
```

**✅ PASS Criteria:**
- Ollama: Status = "healthy"
- ChromaDB: Status = "healthy"
- Chatbot: Status = "Up" (no health check defined)

**❌ FAIL Indicators:**
- Any service shows "unhealthy"
- Services show "Restarting"
- Services show "Exit 1"

**Troubleshooting:**
```bash
# Check individual service logs
docker compose logs ollama
docker compose logs chromadb
docker compose logs chatbot

# Check health status
docker inspect sme-ollama-phase2 --format='{{.State.Health.Status}}'
```

---

### Test 1.3: Test Ollama API Endpoint

```bash
curl http://localhost:11434/api/tags
```

**Expected Output:**
```json
{
  "models": []
}
```
*(Empty at first - we haven't downloaded models yet)*

**✅ PASS Criteria:**
- HTTP 200 response
- Valid JSON returned
- No connection errors

**❌ FAIL Indicators:**
- Connection refused
- Timeout
- HTTP 500 error

---

### Test 1.4: Test ChromaDB API Endpoint

```bash
curl http://localhost:8000/api/v1/heartbeat
```

**Expected Output:**
```json
{
  "nanosecond heartbeat": 1234567890123456789
}
```

**✅ PASS Criteria:**
- HTTP 200 response
- Valid JSON with timestamp
- Response time < 1 second

**❌ FAIL Indicators:**
- Connection refused
- Timeout
- HTTP 404 (wrong URL)

---

### Test 1.5: Test Chatbot UI Access

Open browser: **http://localhost:8080**

**Expected UI:**
- Page loads without errors
- Header: "🧠 SME Knowledge Chatbot"
- Subtitle: "Phase 2: Semantic Search & RAG"
- Sidebar shows system status
- Chat input box visible

**✅ PASS Criteria:**
- Page loads in < 3 seconds
- No error messages in browser
- UI elements render correctly

**❌ FAIL Indicators:**
- "Connection refused" in browser
- Blank page
- Streamlit error messages
- Status shows all "🔴 Disconnected"

**Troubleshooting:**
```bash
# Check chatbot logs
docker compose logs chatbot | tail -20

# Restart chatbot
docker compose restart chatbot
```

---

## Test Suite 2: Model Downloads

### Test 2.1: Download LLM Model

```bash
docker exec sme-ollama-phase2 ollama pull llama3.2:1b
```

**Expected Output:**
```
pulling manifest
pulling 74701a8c35f6... 100% ▕████████████████▏ 1.3 GB
pulling 966de95ca8a6... 100% ▕████████████████▏ 1.4 KB
...
verifying sha256 digest
writing manifest
success
```

**⏱️ Expected Duration:** 2-5 minutes (depends on internet speed)

**✅ PASS Criteria:**
- Download completes successfully
- "success" message appears
- No error messages

**❌ FAIL Indicators:**
- Network timeout
- Disk space error
- Checksum verification failed

**Troubleshooting:**
```bash
# Check available disk space
docker system df

# Retry download
docker exec sme-ollama-phase2 ollama pull llama3.2:1b
```

---

### Test 2.2: Download Embedding Model

```bash
docker exec sme-ollama-phase2 ollama pull nomic-embed-text
```

**Expected Output:**
```
pulling manifest
pulling 970aa74c0a90... 100% ▕████████████████▏ 274 MB
...
success
```

**⏱️ Expected Duration:** 1-3 minutes

**✅ PASS Criteria:**
- Download completes successfully
- Model size ~274MB
- "success" message appears

---

### Test 2.3: Verify Both Models Downloaded

```bash
docker exec sme-ollama-phase2 ollama list
```

**Expected Output:**
```
NAME                TAG       SIZE      MODIFIED
llama3.2:1b         latest    1.3 GB    X seconds ago
nomic-embed-text    latest    274 MB    X seconds ago
```

**✅ PASS Criteria:**
- Both models appear in list
- Sizes match expected values
- No errors

**❌ FAIL Indicators:**
- Only one model listed
- Size shows 0 GB
- "model not found" errors

---

## Test Suite 3: Knowledge Vault Indexing

### Test 3.1: Verify Sample Files Exist

```bash
ls -la knowledge-vault/
```

**Expected Output:**
```
README.md
sample-decision.md
sample-meeting-notes.md
sample-technical-doc.md
```

**✅ PASS Criteria:**
- All 4 files present
- Files are not empty
- Files are .md format

**Check file sizes:**
```bash
wc -l knowledge-vault/*.md
```

**Expected:** Each file should have 100+ lines

---

### Test 3.2: Test Embedding Generation (Direct API)

```bash
curl -X POST http://localhost:11434/api/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-embed-text",
    "prompt": "This is a test document about databases."
  }'
```

**Expected Output:**
```json
{
  "embedding": [0.123, -0.456, 0.789, ..., 0.012]
}
```
*(Array of 768 numbers)*

**✅ PASS Criteria:**
- HTTP 200 response
- Returns array of 768 numbers
- Response time < 2 seconds

**❌ FAIL Indicators:**
- Model not found error
- Empty embedding array
- Timeout

---

### Test 3.3: UI-Based Indexing

**In Browser (http://localhost:8080):**

1. **Check Sidebar Status:**
   - Ollama: 🟢 Connected
   - RAG Status: 🟢 Enabled
   - ChromaDB: 🟢 Connected

2. **Click "🔄 Index Knowledge Vault" button**

**Expected Behavior:**
- Loading spinner appears
- After 10-30 seconds: "✅ Indexed 3 documents!"
- No error messages

**✅ PASS Criteria:**
- Success message shows exactly 3 documents
- Process completes in < 60 seconds
- No errors in UI or logs

**❌ FAIL Indicators:**
- "❌ Indexing failed" message
- Timeout after 60 seconds
- Error about ChromaDB connection
- Error about embedding model

**Check Logs If Failed:**
```bash
docker compose logs chatbot | grep -i error
docker compose logs chromadb | grep -i error
```

---

### Test 3.4: Verify ChromaDB Contains Data

```bash
curl http://localhost:8000/api/v1/collections
```

**Expected Output:**
```json
[
  {
    "name": "knowledge_vault",
    "metadata": {"description": "SME Knowledge Graph documents"}
  }
]
```

**Then check document count:**
```bash
curl http://localhost:8000/api/v1/collections/knowledge_vault/count
```

**Expected Output:**
```json
3
```

**✅ PASS Criteria:**
- Collection exists
- Count = 3
- No errors

---

## Test Suite 4: Semantic Search Functionality

### Test 4.1: Basic Query - Database Decision

**In Chatbot UI, type:**
```
What did we decide about the database?
```

**Expected Response:**
```
Based on the knowledge vault, we decided to use PostgreSQL 15 as our
primary database. The decision was made on January 15, 2024.

Key reasons for choosing PostgreSQL:
1. Proven reliability - Battle-tested at our scale
2. Rich feature set - JSONB, full-text search, advanced indexing
3. Open source - No vendor lock-in
4. Compliance ready - Meets SOC2 requirements
5. Team expertise - Senior engineers have 5+ years experience

---
Sources:
1. `sample-decision.md`
```

**✅ PASS Criteria:**
- Mentions PostgreSQL
- Cites `sample-decision.md`
- Provides relevant reasons
- Response time < 15 seconds

**❌ FAIL Indicators:**
- "I don't have information about that"
- No sources cited
- Completely unrelated answer
- Error message

---

### Test 4.2: Semantic Understanding - Synonym Query

**Type:**
```
Why did we pick that data storage technology?
```
*(Note: Uses "pick" instead of "choose", "data storage" instead of "database")*

**Expected Response:**
- Should still find and cite `sample-decision.md`
- Should answer about PostgreSQL
- Demonstrates semantic search (not keyword matching)

**✅ PASS Criteria:**
- Correct answer despite different wording
- Cites same source as Test 4.1
- Shows understanding of synonyms

**❌ FAIL Indicators:**
- "I don't know" response
- No sources found
- Answers about different topic

---

### Test 4.3: Entity Extraction - People Query

**Type:**
```
Who was involved in the database decision?
```

**Expected Response:**
```
The database decision involved:
- John Smith (@john) - Engineering Lead, PostgreSQL advocate
- Sarah Johnson (@sarah) - Product Manager, handled customer requirements
- Mike Chen (@mike) - DevOps, infrastructure and compliance

---
Sources:
1. `sample-decision.md`
```

**✅ PASS Criteria:**
- Names all 3 people
- Includes their roles
- Cites correct source

---

### Test 4.4: Cross-Document Query - Timeline/Risks

**Type:**
```
What risks were discussed in meetings?
```

**Expected Response:**
- Should cite `sample-meeting-notes.md`
- Should mention:
  - Test data availability
  - Docker Desktop licensing
  - PostgreSQL training gap

**✅ PASS Criteria:**
- Cites meeting notes file
- Lists 2+ risks
- Relevant to actual content

---

### Test 4.5: Negative Test - Out of Scope Query

**Type:**
```
What is the capital of France?
```

**Expected Response:**
```
I don't have information about that in the knowledge vault.
The documents I have access to are about database decisions,
engineering meetings, and PostgreSQL architecture.

However, I can answer: The capital of France is Paris.
[OR] I don't have information about that in my knowledge base.

---
Sources:
(None - using general knowledge)
```

**✅ PASS Criteria:**
- Acknowledges not in knowledge vault
- Either answers from general LLM knowledge OR says "I don't know"
- No false sources cited

**❌ FAIL Indicators:**
- Makes up sources
- Hallucinates documents
- Cites irrelevant files

---

## Test Suite 5: Error Handling

### Test 5.1: ChromaDB Offline Scenario

**Simulate ChromaDB failure:**
```bash
docker compose stop chromadb
```

**In UI:**
1. Check sidebar - ChromaDB should show 🔴 Disconnected
2. Try asking: "What did we decide about databases?"

**Expected Behavior:**
- Warning message about ChromaDB unavailable
- Chatbot still responds (using LLM general knowledge)
- No crash or blank screen

**✅ PASS Criteria:**
- Graceful degradation
- User sees clear error message
- Chatbot remains functional

**Restore:**
```bash
docker compose start chromadb
```

---

### Test 5.2: Ollama Offline Scenario

**Simulate Ollama failure:**
```bash
docker compose stop ollama
```

**In UI:**
1. Check sidebar - Ollama should show 🔴 Disconnected
2. Try asking any question

**Expected Behavior:**
```
⚠️ Cannot connect to Ollama. Make sure Ollama service is running.
```

**✅ PASS Criteria:**
- Clear error message
- No application crash
- Sidebar shows correct status

**Restore:**
```bash
docker compose start ollama
```

---

### Test 5.3: Empty Knowledge Vault

**Backup and clear knowledge vault:**
```bash
cd knowledge-vault
mkdir ../vault-backup
mv *.md ../vault-backup/
```

**In UI:**
1. Click "🔄 Index Knowledge Vault"

**Expected Behavior:**
```
⚠️ No markdown files found in /knowledge-vault
```
OR
```
✅ Indexed 0 documents
```

**✅ PASS Criteria:**
- Graceful handling of empty vault
- Clear message to user
- No crash

**Restore:**
```bash
mv ../vault-backup/*.md .
```

---

## Test Suite 6: Performance Benchmarks

### Test 6.1: Indexing Performance

**Measure indexing time:**
```bash
time docker compose exec chatbot python -c "
from app_phase2 import index_knowledge_vault
count = index_knowledge_vault()
print(f'Indexed {count} documents')
"
```

**Benchmark:**
- **3 documents**: < 30 seconds
- **10 documents**: < 60 seconds
- **50 documents**: < 5 minutes

**✅ PASS Criteria:**
- Meets benchmark for document count
- No timeouts
- Linear scaling (2x docs ≈ 2x time)

---

### Test 6.2: Query Response Time

**Measure query time in UI:**

1. Type: "What did we decide about databases?"
2. Observe response time

**Benchmark:**
- **Embedding generation**: 1-3 seconds
- **Vector search**: 1-2 seconds
- **LLM response**: 5-10 seconds
- **Total**: < 15 seconds

**✅ PASS Criteria:**
- Total response < 20 seconds
- Consistent across multiple queries
- No progressive slowdown

---

## Test Suite 7: Data Persistence

### Test 7.1: Restart Services - Data Persists

```bash
# Stop services
docker compose down

# Start again
docker compose up -d

# Wait 30 seconds
sleep 30
```

**Verify in UI:**
1. Models still listed: `ollama list` shows both models
2. ChromaDB still has data: Collection count = 3
3. No need to re-index

**✅ PASS Criteria:**
- Models don't need re-download
- ChromaDB data persists
- Immediate functionality after restart

---

### Test 7.2: Volume Inspection

```bash
# List volumes
docker volume ls | grep phase-2-rag

# Expected:
# phase-2-rag_ollama-data
# phase-2-rag_chromadb-data

# Check volume sizes
docker system df -v | grep phase-2-rag
```

**Expected Sizes:**
- `ollama-data`: ~1.6 GB (both models)
- `chromadb-data`: ~50-100 MB (3 docs)

**✅ PASS Criteria:**
- Both volumes exist
- Sizes match expectations
- Volumes survive `docker compose down`

---

## Complete Test Checklist

Copy this checklist for testing runs:

```
Phase 2 Testing Checklist - Date: __________

□ Suite 1: Service Health
  □ 1.1 All services start
  □ 1.2 All services healthy
  □ 1.3 Ollama API responds
  □ 1.4 ChromaDB API responds
  □ 1.5 Chatbot UI loads

□ Suite 2: Model Downloads
  □ 2.1 LLM model downloaded
  □ 2.2 Embedding model downloaded
  □ 2.3 Both models listed

□ Suite 3: Knowledge Vault Indexing
  □ 3.1 Sample files exist
  □ 3.2 Embedding API works
  □ 3.3 UI indexing succeeds
  □ 3.4 ChromaDB contains data

□ Suite 4: Semantic Search
  □ 4.1 Basic query works
  □ 4.2 Synonym understanding
  □ 4.3 Entity extraction
  □ 4.4 Cross-document query
  □ 4.5 Out-of-scope handling

□ Suite 5: Error Handling
  □ 5.1 ChromaDB offline graceful
  □ 5.2 Ollama offline graceful
  □ 5.3 Empty vault graceful

□ Suite 6: Performance
  □ 6.1 Indexing < 30 sec (3 docs)
  □ 6.2 Query response < 15 sec

□ Suite 7: Data Persistence
  □ 7.1 Data persists after restart
  □ 7.2 Volumes correct size

Overall Status: PASS / FAIL
Notes:
```

---

## Known Issues / Expected Behaviors

### Issue 1: First Query Slow
**Symptom:** First query after indexing takes 20-30 seconds
**Cause:** ChromaDB warming up, embedding model loading
**Expected:** Normal - subsequent queries faster (< 15 sec)

### Issue 2: LLM Responses Vary
**Symptom:** Same query gives slightly different answers
**Cause:** LLM non-deterministic (even with temp=0)
**Expected:** Normal - content should be consistent, wording may vary

### Issue 3: ChromaDB Takes Time to Start
**Symptom:** ChromaDB shows unhealthy for 10-20 seconds
**Cause:** Initial database setup
**Expected:** Normal - wait 30 seconds before testing

---

## Regression Testing

When making changes, re-run these critical tests:

**Smoke Test (5 minutes):**
1. Test 1.2: Service health
2. Test 2.3: Models listed
3. Test 4.1: Basic query works

**Full Regression (20 minutes):**
- All tests in Suites 1-5

**Before Release:**
- All 7 suites
- Performance benchmarks
- Document all failures

---

## Test Environment Details

**Record for each test run:**

```
Date: __________
Tester: __________

Environment:
- OS: Windows 11 / macOS / Linux
- Docker Desktop Version: ______
- RAM Available: ______
- Disk Space Free: ______

Results:
- Total Tests Run: ______
- Passed: ______
- Failed: ______
- Skipped: ______

Critical Failures:
[List any blocking issues]

Notes:
[Additional observations]
```

---

## Cleanup After Testing

```bash
# Stop all services
docker compose down

# Remove volumes (clean slate for next test)
docker compose down -v

# Remove downloaded models (optional - saves disk space)
docker volume rm phase-2-rag_ollama-data

# Keep knowledge vault files (they're in local directory)
```

---

## Next Steps After Testing

**If All Tests Pass:**
- ✅ Phase 2 ready for students
- ✅ Document any quirks in deployment guide
- ✅ Create video walkthrough (optional)
- ✅ Move to Phase 3 development

**If Tests Fail:**
1. Document exact failure
2. Check logs: `docker compose logs > test-logs.txt`
3. Create GitHub issue with:
   - Test that failed
   - Expected vs actual behavior
   - Logs
   - Environment details

---

## Support

**For testing questions:**
- See: [docs/phase-2-rag.md](phase-2-rag.md) - Deployment guide
- See: [docs/PHASE-2-QUICK-START.md](PHASE-2-QUICK-START.md) - Quick reference

**Report bugs:**
- GitHub Issues: https://github.com/pingwu/sme-knowledge-graph/issues
- Include: Test number, logs, environment details
