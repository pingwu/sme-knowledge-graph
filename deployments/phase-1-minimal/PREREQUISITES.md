# Phase 1 Prerequisites Checklist

Before running Phase 1, verify you have everything needed.

---

## ✅ Checklist

### 1. Docker Desktop
- [ ] Docker Desktop installed
- [ ] Docker Desktop running
- [ ] Docker version 20.10+ (check with `docker --version`)
- [ ] Docker Compose available (check with `docker-compose --version`)

### 2. System Resources
- [ ] At least 8GB RAM (16GB recommended)
- [ ] At least 10GB free disk space
- [ ] Internet connection (for first-time setup only)

### 3. Port Availability
- [ ] Port 8080 available (chatbot web UI)
- [ ] Port 11434 available (Ollama API)

---

## 🔍 Quick Verification Script

Run this PowerShell script to check all prerequisites:

```powershell
# Save as: check-prerequisites.ps1
Write-Host "`n=== SME Knowledge Graph - Prerequisites Check ===" -ForegroundColor Cyan

# Check 1: Docker Desktop
Write-Host "`n[1/5] Checking Docker Desktop..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "  ✅ Docker installed: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Docker not found. Please install Docker Desktop." -ForegroundColor Red
    Write-Host "     Download: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check 2: Docker running
Write-Host "`n[2/5] Checking if Docker is running..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "  ✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check 3: Docker Compose
Write-Host "`n[3/5] Checking Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version
    Write-Host "  ✅ Docker Compose available: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Docker Compose not found." -ForegroundColor Red
    exit 1
}

# Check 4: Port availability
Write-Host "`n[4/5] Checking port availability..." -ForegroundColor Yellow

function Test-Port {
    param([int]$Port)
    $connection = Test-NetConnection -ComputerName localhost -Port $Port -WarningAction SilentlyContinue -ErrorAction SilentlyContinue
    return $connection.TcpTestSucceeded
}

$port8080 = Test-Port -Port 8080
$port11434 = Test-Port -Port 11434

if ($port8080) {
    Write-Host "  ⚠️  Port 8080 is in use (chatbot UI)" -ForegroundColor Yellow
    Write-Host "     You'll need to stop the service using this port" -ForegroundColor Yellow
} else {
    Write-Host "  ✅ Port 8080 available (chatbot UI)" -ForegroundColor Green
}

if ($port11434) {
    Write-Host "  ⚠️  Port 11434 is in use (Ollama API)" -ForegroundColor Yellow
    Write-Host "     You'll need to stop the service using this port" -ForegroundColor Yellow
} else {
    Write-Host "  ✅ Port 11434 available (Ollama API)" -ForegroundColor Green
}

# Check 5: Disk space
Write-Host "`n[5/5] Checking disk space..." -ForegroundColor Yellow
$drive = Get-PSDrive -Name C
$freeSpaceGB = [math]::Round($drive.Free / 1GB, 2)

if ($freeSpaceGB -ge 10) {
    Write-Host "  ✅ Sufficient disk space: $freeSpaceGB GB available" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Low disk space: $freeSpaceGB GB available (10GB recommended)" -ForegroundColor Yellow
}

# Summary
Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host "All critical checks passed! You're ready to run Phase 1." -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. cd sme-knowledge-graph\deployments\phase-1-minimal" -ForegroundColor White
Write-Host "  2. docker-compose up" -ForegroundColor White
Write-Host "  3. Open http://localhost:8080 in your browser`n" -ForegroundColor White
