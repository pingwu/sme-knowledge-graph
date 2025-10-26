# Changelog

All notable changes to the SME Knowledge Graph project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial Phase 1 implementation (Ollama + Streamlit chatbot)
- Docker Compose configuration with standardized service DNS
- Comprehensive model management system
- Teaching materials for Docker networking concepts
- Troubleshooting guides and documentation

### Changed
- Migrated from hardcoded IP addresses to Docker service name DNS resolution
- Improved chatbot UI with connection status indicators
- Updated README with quick start guide and troubleshooting

### Fixed
- Container-to-container communication reliability
- Model configuration persistence across container restarts
- Environment variable propagation to chatbot application

## [0.1.0] - 2025-10-26

### Added
- **Phase 1: Minimal Chatbot**
  - Ollama local LLM server (port 11434)
  - Streamlit web UI chatbot (port 8080)
  - Docker Compose orchestration
  - 100% local, privacy-first architecture

- **Docker Configuration Standardization**
  - Service name DNS resolution (`http://ollama:11434`)
  - Custom bridge network (`sme-network`)
  - Health checks for service dependencies
  - Fixed port mappings for consistent access

- **Model Management**
  - Support for multiple Ollama models
  - Environment variable-based model selection
  - Quick model switching workflow
  - Model download and removal commands

- **Documentation**
  - `README.md` - Project overview and quick start
  - `docs/MODEL-MANAGEMENT-GUIDE.md` - Comprehensive model management
  - `docs/DOCKER-SERVICE-DNS-TEACHING-NOTE.md` - Docker networking teaching materials
  - `docs/STANDARDIZED-DOCKER-CONFIG.md` - Configuration standards reference
  - `LICENSE` - MIT License
  - `CHANGELOG.md` - This file

- **Chatbot Features**
  - Natural language chat interface
  - Session-based chat history
  - Connection status indicator
  - Model information display
  - Error handling with user-friendly messages

### Technical Details

**Docker Architecture:**
- Ollama container: `sme-ollama`
- Chatbot container: `sme-chatbot`
- Network: `sme-network` (bridge)
- Volumes: `ollama-data` (persistent model storage)

**Default Configuration:**
- Default model: `llama3.2:1b` (1.3 GB)
- Ollama URL: `http://ollama:11434` (from containers)
- Chatbot URL: `http://localhost:8080` (from host)

**Supported Models:**
- llama3.2:1b - Fast, basic quality (1.3 GB)
- llama3.2:3b - Balanced performance (2.0 GB)
- llama3:8b - High quality, slower (4.7 GB)

### Known Issues
- Model responses can be slow on CPU-only systems
- First response after model load takes longer
- No GPU acceleration in current version

### Security
- All processing is 100% local
- No data sent to cloud services
- No API keys or external dependencies required

---

## Release Notes

### v0.1.0 - First Public Release

This is the initial public release of the SME Knowledge Graph project, focusing on Phase 1: a fully functional local AI chatbot.

**What's Working:**
- ✅ Complete Docker-based deployment
- ✅ Local LLM with Ollama
- ✅ Web-based chat interface
- ✅ Model management system
- ✅ Comprehensive documentation

**What's Next:**
- Phase 2: RAG (Retrieval Augmented Generation) with markdown search
- Phase 3: Neo4j knowledge graph integration
- GPU acceleration support
- Additional model support

**Getting Started:**
```bash
git clone https://github.com/pingwu/sme-knowledge-graph
cd sme-knowledge-graph/deployments/phase-1-minimal
docker compose up -d
docker exec sme-ollama ollama pull llama3.2:1b
# Open http://localhost:8080
```

---

**Project Maintainer**: Ping Wu
**License**: MIT
**Repository**: https://github.com/pingwu/sme-knowledge-graph
