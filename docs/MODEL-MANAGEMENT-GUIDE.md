# Ollama Model Management - Quick Reference Guide

**Purpose**: Manage AI models in your SME Knowledge Graph chatbot
**Last Updated**: 2025-10-26

---

## Overview

Your chatbot uses Ollama to run local AI models. This guide shows you how to:
- List available models
- Download new models
- Switch between models
- Remove unused models

---

## Quick Commands

### 1. List Installed Models

```bash
docker exec sme-ollama ollama list
```

**Example output:**
```
NAME           ID              SIZE      MODIFIED
llama3.2:1b    baf6a787fdff    1.3 GB    2 hours ago
llama3:8b      a6990ed6be41    4.7 GB    1 day ago
```

---

## 2. Download Models

### Recommended Models

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| `llama3.2:1b` | 1.3 GB | ⚡⚡⚡ Fast | ⭐⭐ Basic | Testing, simple Q&A |
| `llama3.2:3b` | 2.0 GB | ⚡⚡ Good | ⭐⭐⭐ Good | Balanced performance |
| `llama3:8b` | 4.7 GB | ⚡ Slower | ⭐⭐⭐⭐ Great | Production, detailed responses |

### Download Command

```bash
# Download a specific model
docker exec sme-ollama ollama pull llama3:8b

# Download faster alternative
docker exec sme-ollama ollama pull llama3.2:3b
```

**Note:** Downloads can take 5-15 minutes depending on model size and internet speed.

---

## 3. Switch Models

### Option A: Update docker-compose.yml (Recommended)

**Step 1:** Edit the configuration file
```bash
cd C:/MASProjects/PING/MACA-Course/sme-knowledge-graph/deployments/phase-1-minimal
# Edit docker-compose.yml
```

**Step 2:** Change the MODEL_NAME line:
```yaml
environment:
  - MODEL_NAME=llama3:8b  # Change this line
```

**Step 3:** Rebuild and restart
```bash
docker compose up -d --build chatbot
```

### Option B: Quick Test (Temporary)

```bash
# Stop chatbot
docker compose stop chatbot

# Start with different model (temporary - resets on restart)
docker compose run --rm -e MODEL_NAME=llama3:8b chatbot
```

---

## 4. Remove Models

### Free up disk space by removing unused models

```bash
# List models first
docker exec sme-ollama ollama list

# Remove specific model
docker exec sme-ollama ollama rm llama3.2:1b
```

**Warning:** Make sure you're not using the model before removing it!

---

## 5. Troubleshooting

### Model Not Found (404 Error)

**Symptoms:**
- Chatbot shows "Error: API returned status 404"
- Model listed in "About" but getting errors

**Solution:**
```bash
# 1. Check what models are actually installed
docker exec sme-ollama ollama list

# 2. Download the missing model
docker exec sme-ollama ollama pull llama3.2:1b

# 3. Verify MODEL_NAME matches installed model
docker exec sme-chatbot printenv | grep MODEL_NAME

# 4. Rebuild chatbot if needed
cd deployments/phase-1-minimal
docker compose up -d --build chatbot
```

### Slow Response Times

**If chatbot is too slow:**

1. **Use smaller model** (fastest, lower quality):
   ```bash
   # Switch to 1B model
   docker exec sme-ollama ollama pull llama3.2:1b
   # Update docker-compose.yml to MODEL_NAME=llama3.2:1b
   docker compose up -d --build chatbot
   ```

2. **Use balanced model** (good compromise):
   ```bash
   # Switch to 3B model
   docker exec sme-ollama ollama pull llama3.2:3b
   # Update docker-compose.yml to MODEL_NAME=llama3.2:3b
   docker compose up -d --build chatbot
   ```

3. **Check system resources**:
   ```bash
   docker stats sme-ollama
   ```

### Connection Issues

**If chatbot can't connect to Ollama:**

```bash
# Check both containers are running
docker compose ps

# Verify Ollama is healthy
docker exec sme-ollama ollama list

# Check chatbot environment
docker exec sme-chatbot printenv | grep OLLAMA_URL

# Should show: OLLAMA_URL=http://ollama:11434
```

---

## 6. Model Comparison

### Performance Expectations (on typical laptop)

| Model | First Response | Tokens/Second | Quality Rating |
|-------|---------------|---------------|----------------|
| llama3.2:1b | 2-4 seconds | 15-25 | ⭐⭐ Basic |
| llama3.2:3b | 4-8 seconds | 8-15 | ⭐⭐⭐ Good |
| llama3:8b | 8-15 seconds | 4-8 | ⭐⭐⭐⭐ Great |

**Note:** Times vary based on CPU, RAM, and query complexity.

---

## 7. Complete Model Switch Workflow

**Example: Switching from llama3.2:1b to llama3:8b**

```bash
# Step 1: Download the new model (one-time, ~10 minutes)
docker exec sme-ollama ollama pull llama3:8b

# Step 2: Verify download
docker exec sme-ollama ollama list

# Step 3: Navigate to deployment directory
cd C:/MASProjects/PING/MACA-Course/sme-knowledge-graph/deployments/phase-1-minimal

# Step 4: Edit docker-compose.yml
# Change: MODEL_NAME=llama3.2:1b
# To:     MODEL_NAME=llama3:8b

# Step 5: Rebuild and restart chatbot
docker compose up -d --build chatbot

# Step 6: Verify in browser
# Open http://localhost:8080
# Check "About" section shows: Model: llama3:8b

# Step 7: (Optional) Remove old model to save space
docker exec sme-ollama ollama rm llama3.2:1b
```

---

## 8. Disk Space Management

### Check Model Storage

```bash
# See all models and their sizes
docker exec sme-ollama ollama list

# Check Docker disk usage
docker system df
```

### Clean Up Strategy

**If running low on disk space:**

1. **Keep only one model**:
   ```bash
   # Remove models you're not using
   docker exec sme-ollama ollama rm llama3.2:1b
   docker exec sme-ollama ollama rm llama3.2:3b
   ```

2. **Use the smallest model that meets your needs**:
   - Quick testing? → `llama3.2:1b` (1.3 GB)
   - Daily use? → `llama3.2:3b` (2.0 GB)
   - Best quality? → `llama3:8b` (4.7 GB)

---

## 9. Advanced: Custom Models

### Using Other Ollama Models

Browse available models: https://ollama.com/library

**Example: Using Mistral**
```bash
# Download Mistral
docker exec sme-ollama ollama pull mistral

# Update docker-compose.yml
# MODEL_NAME=mistral

# Rebuild
docker compose up -d --build chatbot
```

---

## 10. Best Practices

✅ **Do:**
- Keep at least one model installed
- Verify downloads complete before switching
- Update docker-compose.yml for persistent changes
- Test new models before removing old ones

❌ **Don't:**
- Remove the currently active model
- Modify environment variables directly in running container (changes won't persist)
- Download multiple large models if disk space is limited

---

## Quick Reference Card

```bash
# Most Common Operations

# List models
docker exec sme-ollama ollama list

# Download model
docker exec sme-ollama ollama pull <model-name>

# Remove model
docker exec sme-ollama ollama rm <model-name>

# Switch model (edit docker-compose.yml first)
docker compose up -d --build chatbot

# Check what model is active
docker exec sme-chatbot printenv | grep MODEL_NAME

# Verify connection
curl http://localhost:11434/api/tags
```

---

## Support

**If you encounter issues:**
1. Check this troubleshooting guide
2. Verify Docker is running: `docker ps`
3. Check logs: `docker compose logs chatbot`
4. Restart services: `docker compose restart`

**Documentation:**
- Main README: `../README.md`
- Docker DNS Guide: `DOCKER-SERVICE-DNS-TEACHING-NOTE.md`
- Configuration Standards: `STANDARDIZED-DOCKER-CONFIG.md`

---

**Last Updated**: 2025-10-26
**Maintainer**: SME Knowledge Graph Project
