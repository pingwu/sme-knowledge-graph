# Standardized Docker Configuration

**Purpose**: Eliminate manual reconfiguration of Ollama connection across sessions
**Created**: 2025-10-26
**Status**: Production Standard

---

## Problem Solved

**Before**: Hardcoded IP addresses broke on container restart
```yaml
# ❌ OLD: Required reconfiguration every restart
environment:
  - OLLAMA_URL=http://172.17.0.3:11434
```

**After**: Service name resolution works automatically
```yaml
# ✅ NEW: Works every time, no reconfiguration
environment:
  - OLLAMA_URL=http://ollama:11434
```

---

## Configuration Standard

### Fixed Ports (Never Change)

| Service | Port | Access Pattern |
|---------|------|----------------|
| Ollama | 11434 | `http://ollama:11434` (containers)<br>`http://localhost:11434` (host) |
| Chatbot UI | 8080 | `http://localhost:8080` (host) |

### Network Architecture

```yaml
networks:
  sme-network:
    driver: bridge
```

All services connect to `sme-network` for reliable service discovery.

---

## How to Use

### Starting Services

```bash
cd C:/MASProjects/PING/MACA-Course/sme-knowledge-graph/deployments/phase-1-minimal
docker compose up -d
```

### Accessing Services

**From Host Machine (Windows):**
- Ollama API: `http://localhost:11434`
- Chatbot UI: `http://localhost:8080`

**From Inside Containers:**
- Ollama API: `http://ollama:11434`

### Verifying Connection

```bash
# Check Ollama is responding
curl http://localhost:11434/api/tags

# Check chatbot can reach Ollama
docker compose logs chatbot | grep -i "ollama"
```

---

## Restart Procedure (Zero Reconfiguration)

```bash
# Stop everything
docker compose down

# Start everything
docker compose up -d

# Connection automatically works - no IP address updates needed!
```

---

## Key Changes from Original

1. **Service Name DNS**: `http://ollama:11434` instead of `http://172.17.0.3:11434`
2. **Custom Network**: Added `sme-network` for isolation and reliability
3. **Documentation**: Comments explain access patterns
4. **Portability**: Works on any machine without modification

---

## Troubleshooting

### "Connection refused" to Ollama

```bash
# Check Ollama is running and healthy
docker compose ps

# Should show:
# sme-ollama    running (healthy)
# sme-chatbot   running
```

### Test DNS Resolution

```bash
# From inside chatbot container
docker exec -it sme-chatbot ping ollama

# Should resolve to container IP automatically
```

### Check Network Configuration

```bash
# Verify both containers on same network
docker network inspect phase-1-minimal_sme-network

# Should show both ollama and chatbot
```

---

## Best Practices Enforced

✅ **No hardcoded IPs** - All inter-container communication uses service names
✅ **Fixed ports** - 11434 for Ollama, 8080 for Chatbot
✅ **Custom network** - Isolated from other Docker services
✅ **Health checks** - Chatbot waits for Ollama to be healthy
✅ **Portable** - Works on any machine without configuration changes

---

## Future-Proofing

When adding new services that need Ollama:

```yaml
services:
  new-service:
    environment:
      - OLLAMA_URL=http://ollama:11434  # Standard pattern
    networks:
      - sme-network  # Join the network
```

**Never use:**
- ❌ IP addresses (172.17.0.x)
- ❌ localhost (won't work from containers)
- ❌ Container names from other compose files

**Always use:**
- ✅ Service names (ollama, chatbot, etc.)
- ✅ Fixed ports (11434 for Ollama)
- ✅ Custom network (sme-network)

---

## Teaching Integration

This configuration demonstrates:
- Docker Compose networking fundamentals
- Service discovery via DNS
- Production-ready container configuration
- Zero-configuration deployment patterns

See `DOCKER-SERVICE-DNS-TEACHING-NOTE.md` for detailed teaching materials.

---

**Configuration File**: `deployments/phase-1-minimal/docker-compose.yml`
**Last Updated**: 2025-10-26
**Tested On**: Windows 11, Docker Desktop 4.x
