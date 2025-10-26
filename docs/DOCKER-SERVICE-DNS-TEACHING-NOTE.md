# Docker Service DNS Resolution - Teaching Note

**Category**: Docker Networking Fundamentals
**Level**: Intermediate
**Common Mistake**: Hardcoding container IP addresses
**Created**: 2025-10-26

---

## The Problem Students Face

When connecting containers together, beginners often hardcode IP addresses:

```yaml
# ❌ WRONG: Hardcoded IP address
environment:
  - OLLAMA_URL=http://172.17.0.3:11434
```

**Why this breaks:**
- Container IPs can change on restart
- IPs vary across different machines
- Requires manual reconfiguration
- Not portable across environments

---

## The Solution: Service Name DNS

Docker Compose provides **automatic DNS resolution** using service names:

```yaml
# ✅ CORRECT: Use service name
environment:
  - OLLAMA_URL=http://ollama:11434
```

### How It Works

```yaml
version: '3.8'

services:
  ollama:                    # <-- Service name becomes DNS hostname
    image: ollama/ollama:latest
    container_name: sme-ollama
    ports:
      - "11434:11434"

  chatbot:
    image: my-chatbot:latest
    environment:
      - OLLAMA_URL=http://ollama:11434  # <-- Resolves to ollama service
```

**What happens:**
1. Service name `ollama` is defined in docker-compose.yml
2. Docker creates internal DNS entry: `ollama` → current container IP
3. Any container can use `http://ollama:11434` to connect
4. Docker automatically routes to correct IP (even if it changes)

---

## Teaching Analogy

**Phone Book vs. Speed Dial:**

- **Hardcoded IP** = Memorizing someone's phone number
  - If they change numbers, you're stuck
  - Need to update everywhere you wrote it down

- **Service Name DNS** = Saving contact by name
  - Name stays same even if number changes
  - Phone automatically looks up current number
  - Works everywhere you use that contact

---

## Connection Patterns to Teach

### Pattern 1: Container-to-Container (Inside Docker Network)

```yaml
services:
  database:
    image: postgres:15

  backend:
    environment:
      - DATABASE_URL=postgresql://user:pass@database:5432/mydb
      #                                    ^^^^^^^^
      #                                    Service name, not IP!
```

**Use:** `http://service-name:port`

### Pattern 2: Host-to-Container (From Windows/Mac/Linux)

```yaml
services:
  api:
    ports:
      - "3000:3000"  # Publish to host
```

**Use:** `http://localhost:3000`

### Pattern 3: Container-to-Host Services

```yaml
services:
  app:
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      - API_URL=http://host.docker.internal:8000
```

**Use:** `http://host.docker.internal:port` (to reach services on host machine)

---

## Common Student Questions

### Q: "Where is the IP address 'ollama' mapped to?"

**A:** Nowhere! Docker's internal DNS server automatically resolves `ollama` to whatever IP the ollama container currently has. You never need to know or configure the IP.

### Q: "What if I have multiple networks?"

**A:** Service names only resolve within the same Docker network:

```yaml
networks:
  frontend:
  backend:

services:
  api:
    networks:
      - frontend
      - backend

  database:
    networks:
      - backend  # Only accessible from backend network
```

### Q: "Can I use container_name instead of service name?"

**A:** Yes, but service name is preferred:
- `ollama` (service name) ✅ Best practice
- `sme-ollama` (container name) ✅ Works but less clear
- `172.17.0.3` (IP address) ❌ Avoid

---

## Lab Exercise Design

### Exercise: Fix the Broken Configuration

**Scenario:** Student has this docker-compose.yml:

```yaml
services:
  frontend:
    environment:
      - BACKEND_URL=http://192.168.1.100:5000  # ❌ Hardcoded

  backend:
    ports:
      - "5000:5000"
```

**Task:** Make it portable using service names

**Solution:**
```yaml
services:
  frontend:
    environment:
      - BACKEND_URL=http://backend:5000  # ✅ Service name

  backend:
    ports:
      - "5000:5000"
```

### Exercise: Multi-Service Connection

**Build a 3-tier application:**
- `nginx` → connects to → `api`
- `api` → connects to → `postgres`

**Learning objective:** Chain service name references

---

## Troubleshooting Guide for Students

### "Connection refused" errors

```bash
# Check if service is running
docker compose ps

# Check if services are on same network
docker network inspect <network-name>

# Test DNS resolution inside container
docker exec -it <container> ping ollama
```

### "Name resolution failed"

**Common causes:**
1. Typo in service name (case-sensitive!)
2. Services not on same network
3. Using container name from different compose file
4. Service hasn't started yet (check `depends_on`)

---

## Key Teaching Points

1. **Service names = DNS hostnames** (automatic)
2. **Never hardcode IPs** for container-to-container communication
3. **Use localhost** only from host machine, not inside containers
4. **Networks isolate** service name resolution
5. **Portable by default** - works on any machine

---

## Advanced: Custom DNS Configuration

```yaml
services:
  app:
    dns:
      - 8.8.8.8  # Custom external DNS
      - 1.1.1.1
    dns_search:
      - example.com  # Search domain
```

---

## Reference Links

- [Docker Compose Networking](https://docs.docker.com/compose/networking/)
- [Docker DNS Resolution](https://docs.docker.com/config/containers/container-networking/#dns-services)
- [Networking in Compose](https://docs.docker.com/compose/compose-file/06-networks/)

---

## Student Outcomes

After learning this, students should:
- ✅ Use service names for all inter-container communication
- ✅ Understand when to use localhost vs service names
- ✅ Debug connection issues with DNS resolution
- ✅ Create portable docker-compose configurations
- ✅ Explain the difference between container IP and service name

---

**Real-World Impact:**
This single concept prevents hours of debugging "works on my machine" issues when deploying containerized applications.
