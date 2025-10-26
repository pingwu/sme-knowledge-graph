# SME Knowledge Graph

**Turn scattered information into context-aware intelligence that drives better business decisions**

100% on-premise. Zero cloud dependencies. Supplements your existing tools.

---

## The Problem: Disconnected Information Creates Decision Blindness

### Scenario 1: Cross-Department Decision-Making (the context gap)
**Current Reality:**
- **Engineering** has technical constraints → sees vendor selection as architecture problem
- **Sales** has customer relationships → sees same decision as revenue opportunity
- **Product** has roadmap priorities → sees it as feature delivery question
- **Finance** has budget pressures → sees it as cost optimization
- **Nobody connects the dots** → Each department has pieces, but missing the full picture
- **Result**: Decisions made in silos, optimizing locally but failing globally

### Scenario 2: Strategic Context Lost in Translation (the agenda gap)
**Current Reality:**
- **Executive asks**: "Should we partner with Acme Corp?"
- **CTO thinks**: Technical integration complexity
- **VP Sales thinks**: Revenue potential and relationship history
- **CFO thinks**: Financial terms and risk
- **Each has valid concerns**, but systems store isolated facts without connecting agendas
- **Result**: Decisions based on incomplete relationship intelligence

### Scenario 3: Cross-Functional Alignment (the knowledge gap)
**Current Reality:**
- New PM asks: *"Why did we choose this vendor?"*
- Engineering remembers: Technical specs (in Confluence)
- Sales remembers: Customer commitment (in CRM)
- Finance remembers: Budget constraints (in spreadsheet)
- **Context missing**: How these agendas aligned to drive the original decision
- **Result**: Can't replicate successful decisions, repeat past mistakes

**The Real Cost (Research-Backed):**
- 💰 **$2.4 billion annual loss** for a $9B company from knowledge mismanagement ([Harvard Business Review](https://hbr.org/sponsored/2025/04/how-knowledge-mismanagement-is-costing-your-company-millions))
- ⏰ **21% of work time** spent searching for knowledge + 14% recreating it ([HBR/Bloomfire 2025](https://hbr.org/sponsored/2025/04/how-knowledge-mismanagement-is-costing-your-company-millions))
- 🚪 **$678 million** - Amazon's 2-year onboarding cost in lost productivity ([eLearning Industry](https://elearningindustry.com/employee-onboarding-statistics-in-2024-top-trends-and-insights))
- 🔁 **75% of cross-functional teams are dysfunctional** ([Harvard Business Review](https://hbr.org/2015/06/75-of-cross-functional-teams-are-dysfunctional))

---

## The Solution: Context-Aware Relationship Intelligence That Drives Decisions

**Small Language Model + Relationship Mapping + Multi-Perspective Context = Smart Decisions**

### How It Works

1. **Capture context from all perspectives** - Technical specs + customer needs + budget constraints + strategic goals
2. **AI maps relationships and agendas** - Connects people, decisions, and business context into knowledge graph
3. **Query with stakeholder lens** - "Show me vendor decision from Sales perspective" vs "from Engineering perspective"
4. **Generate context-aware insights** - Same information, translated for different decision-making needs:
   - **Executives** → Strategic implications and relationship capital
   - **Middle managers** → Operational impact and resource allocation
   - **Individual contributors** → Technical details and implementation approach

### Why This Works for Enterprise

**✅ Context Layer Over Existing Tools**
- **Supplements** CRM (adds relationship intelligence), Confluence (adds decision context), Slack (adds agenda mapping)
- **Doesn't replace** anything - connects dots between systems your teams already use
- **Markdown files** = universal format works with everything (Obsidian, VS Code, SharePoint, any text editor)

**✅ Privacy & Security**
- **100% on-premise** - No data leaves your infrastructure
- **No cloud dependencies** - Legal/Compliance approved
- **Air-gapped deployment** - Can run completely offline
- **Your data stays yours** - Portable markdown files

**✅ Fast to Value**
- **5 minutes to deploy** - One Docker command
- **No IT project** - Runs on developer laptop or local server
- **Immediate ROI** - Start capturing knowledge today

**✅ Scales with Your Decision-Making Needs**
- **Individual contributor** → Map your own context and relationships for better local decisions
- **Small team (5-10)** → Share context across functions, align on priorities
- **Department/Enterprise** → Cross-functional relationship intelligence, strategic decision support

## Phased Approach

### Phase 1: Chatbot (Start Here) ⭐
Simple chatbot with Ollama. Chat history, natural language interface.

**Components**: Ollama + Web UI
**Time to deploy**: 5 minutes
**Use case**: Get familiar with local LLM

[→ Phase 1 Guide](docs/phase-1-chatbot.md)

### Phase 2: RAG Search
Add Retrieval Augmented Generation. Chatbot can search your markdown files.

**Components**: Phase 1 + RAG search
**Time to deploy**: +10 minutes
**Use case**: "What did we discuss with Acme about PostgreSQL?"

[→ Phase 2 Guide](docs/phase-2-rag.md)

### Phase 3: Knowledge Graph (Advanced)
Full knowledge graph with Neo4j, MCP server, structured knowledge capture.

**Components**: Phase 2 + Neo4j + MCP
**Time to deploy**: +30 minutes
**Use case**: Complex queries, graph analytics, agentic workflows

[→ Phase 3 Guide](docs/phase-3-knowledge-graph.md)

## Quick Start (Phase 1)

### Prerequisites
- **Docker Desktop** installed ([Download](https://www.docker.com/products/docker-desktop))
- **16GB RAM** recommended (8GB minimum)
- **10GB free disk space** (5GB for models + 5GB for containers)
- **Windows, Mac, or Linux** with Docker support

### Deploy in 4 Steps

```bash
# 1. Clone repository
git clone https://github.com/pingwu/sme-knowledge-graph
cd sme-knowledge-graph

# 2. Start Phase 1 (Ollama + Chatbot)
cd deployments/phase-1-minimal
docker compose up -d

# 3. Download AI model (one-time, ~2 minutes)
docker exec sme-ollama ollama pull llama3.2:1b

# 4. Open browser
# http://localhost:8080
```

**That's it!** You now have a 100% local, private AI chatbot running.

### First Steps

1. **Open the chatbot**: Navigate to http://localhost:8080
2. **Verify connection**: Check sidebar shows "🟢 Connected"
3. **Send first message**: Try "Hello" or "What can you help me with?"

### Managing Models

The default model (`llama3.2:1b`) is fast but basic. For better responses:

```bash
# Download better model (4.7GB, one-time)
docker exec sme-ollama ollama pull llama3:8b

# Switch to better model (see docs/MODEL-MANAGEMENT-GUIDE.md)
# Edit docker-compose.yml: MODEL_NAME=llama3:8b
docker compose up -d --build chatbot
```

**See [Model Management Guide](docs/MODEL-MANAGEMENT-GUIDE.md) for complete instructions.**

## Architecture

### Phase 1: Minimal Chatbot
```
┌─────────────────────────────┐
│  Web UI (localhost:8080)    │
│  - Chat interface           │
│  - History in browser       │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│  Ollama (localhost:11434)   │
│  - Local LLM (llama3.2)     │
│  - No cloud, 100% private   │
└─────────────────────────────┘
```

### Phase 2: With RAG
```
Web UI → Ollama + RAG → Search Markdown Files → Answer with Sources
```

### Phase 3: Full Stack
```
Web UI → MCP Server → Ollama + Neo4j + Obsidian
```

## Use Cases

### Individual Contributor: Better Local Decisions
- **Capture context** from meetings across departments
- **Map relationships** between technical constraints, customer needs, and business goals
- **Query multi-perspective** - "What did Sales promise vs what Engineering committed?"
- **Portable intelligence** - Your context-awareness moves with you

### Small Team: Cross-Functional Alignment
- **Shared context vault** on SharePoint/OneDrive
- **Each perspective preserved** - Engineering view + Sales view + Product view in one place
- **Agenda mapping** - Understand why decisions were made from all stakeholder angles
- **No server infrastructure** needed

### Enterprise: Strategic Relationship Intelligence
- **Supplement CRM** with decision context and relationship history
- **Cross-department insights** - Connect dots between isolated systems
- **Multi-level queries** - Same information, different lenses (exec/manager/IC)
- **Decision pattern recognition** - What worked before when similar agendas aligned?

## What Makes This Different?

| Feature | Enterprise KM | Cloud AI | This Project |
|---------|--------------|----------|--------------|
| **Decision Support** | Static docs | Generic answers | ✅ Context-aware, multi-perspective |
| **Relationship Mapping** | Manual | N/A | ✅ AI-powered agenda connection |
| **Privacy** | Varies | ❌ Cloud | ✅ 100% Local |
| **Cost** | $500-2K/user/year | $20/month | ✅ ~$50/year |
| **Integration** | Replace tools | Generic | ✅ Context layer over existing |
| **Team Collaboration** | Complex setup | Individual only | ✅ SharePoint/OneDrive sync |

## Troubleshooting

### Chatbot shows "🔴 Disconnected"

```bash
# Check if containers are running
docker compose ps

# Restart services
cd deployments/phase-1-minimal
docker compose restart
```

### "Error: API returned status 404"

**Cause**: Model not found in Ollama

```bash
# Check installed models
docker exec sme-ollama ollama list

# Download the model you need
docker exec sme-ollama ollama pull llama3.2:1b

# Verify MODEL_NAME matches
docker exec sme-chatbot printenv | grep MODEL_NAME
```

**See [Model Management Guide](docs/MODEL-MANAGEMENT-GUIDE.md) for complete troubleshooting.**

### Slow responses

- Using `llama3.2:1b`? Expected on CPU (2-4 seconds)
- Want faster? Try smaller prompts or wait for GPU support
- Want better quality? Upgrade to `llama3:8b` (but slower)

### Port already in use

```bash
# Stop existing services
docker compose down

# Check what's using port 8080 or 11434
# Windows: netstat -ano | findstr "8080"
# Mac/Linux: lsof -i :8080
```

## Roadmap

### Completed ✅
- [x] **Phase 1**: Chatbot (Ollama + Streamlit)
- [x] **Standardized Docker Configuration** (No more hardcoded IPs!)
- [x] **Model Management** (Easy model switching)
- [x] **Teaching Materials** (Docker DNS, Configuration)

### In Progress 🚧
- [ ] Phase 2: RAG search (markdown files)
- [ ] Phase 1 Documentation (Setup guide, videos)

### Planned 📋
- [ ] Phase 3: Neo4j knowledge graph
- [ ] Phase 4: MCP server (AI agent integration)
- [ ] Phase 5: n8n workflows (CRM/CMDB sync)
- [ ] Phase 6: Agentic workflows (CrewAI, LangGraph)

## Contributing

This is an open-source project. Contributions welcome!

Areas where help is needed:
- Obsidian plugin development
- n8n workflow templates
- Documentation improvements
- Example use cases

## License

MIT License - see [LICENSE](LICENSE)

## Documentation

### Getting Started
- [Model Management Guide](docs/MODEL-MANAGEMENT-GUIDE.md) - Switch models, troubleshoot issues ⭐
- [Docker DNS Guide](docs/DOCKER-SERVICE-DNS-TEACHING-NOTE.md) - Learn Docker networking
- [Configuration Standards](docs/STANDARDIZED-DOCKER-CONFIG.md) - Technical reference

### Phase Guides
- [Phase 1: Chatbot Setup](docs/phase-1-chatbot.md) (Coming Soon)
- [Phase 2: RAG Integration](docs/phase-2-rag.md) (Coming Soon)
- [Phase 3: Knowledge Graph](docs/phase-3-knowledge-graph.md) (Coming Soon)

### Additional Resources
- [Architecture Overview](docs/architecture.md) (Coming Soon)
- [Obsidian Vault Setup](docs/obsidian-setup.md) (Coming Soon)
- [FAQ](docs/faq.md) (Coming Soon)

## Support

- 📧 Newsletter: https://ping-ai.com/contact
- 💬 Discussions: [GitHub Discussions](https://github.com/pingwu/sme-knowledge-graph/discussions)
- 🐛 Issues: [GitHub Issues](https://github.com/pingwu/sme-knowledge-graph/issues)

## Credits

Built with:
- [Ollama](https://ollama.ai) - Local LLM
- [Obsidian](https://obsidian.md) - Markdown knowledge base
- [Neo4j](https://neo4j.com) - Graph database (Phase 3)
- [Streamlit](https://streamlit.io) - Web UI
- [Docker](https://docker.com) - Containerization

---

**The irony is beautiful: "SME" means both the challenge (Subject Matter Expert with context locked in their head) and the solution (Small Language Model + Enterprise relationship mapping).**

Let's turn scattered information into context-aware intelligence that drives better decisions.

— Ping Wu
