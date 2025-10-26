# SME Knowledge Graph - Prerequisites Checker
# Run this before starting Phase 1

Write-Host ""
Write-Host "=== SME Knowledge Graph - Prerequisites Check ===" -ForegroundColor Cyan
Write-Host "This script will verify your system is ready for Phase 1" -ForegroundColor Gray
Write-Host ""

$allPassed = $true

# Check 1: Docker Desktop
Write-Host "[1/6] Checking Docker Desktop..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    if ($dockerVersion) {
        Write-Host "  OK Docker installed: $dockerVersion" -ForegroundColor Green
    } else {
        throw "Docker not found"
    }
} catch {
    Write-Host "  ERROR Docker not found. Please install Docker Desktop." -ForegroundColor Red
    Write-Host "     Download: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    $allPassed = $false
}

# Check 2: Docker running
Write-Host ""
Write-Host "[2/6] Checking if Docker is running..." -ForegroundColor Yellow
try {
    docker ps 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK Docker daemon is running" -ForegroundColor Green
    } else {
        throw "Docker not running"
    }
} catch {
    Write-Host "  ERROR Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    $allPassed = $false
}

# Check 3: Docker Compose
Write-Host ""
Write-Host "[3/6] Checking Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version 2>$null
    if ($composeVersion) {
        Write-Host "  OK Docker Compose available: $composeVersion" -ForegroundColor Green
    } else {
        throw "Docker Compose not found"
    }
} catch {
    Write-Host "  ERROR Docker Compose not found." -ForegroundColor Red
    $allPassed = $false
}

# Check 4: Port availability
Write-Host ""
Write-Host "[4/6] Checking port availability..." -ForegroundColor Yellow

$port8080InUse = $false
$port11434InUse = $false

try {
    $port8080Connection = Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue
    if ($port8080Connection) {
        Write-Host "  WARNING Port 8080 is in use (needed for chatbot UI)" -ForegroundColor Yellow
        $port8080InUse = $true
    } else {
        Write-Host "  OK Port 8080 available (chatbot UI)" -ForegroundColor Green
    }
} catch {
    Write-Host "  OK Port 8080 available (chatbot UI)" -ForegroundColor Green
}

try {
    $port11434Connection = Get-NetTCPConnection -LocalPort 11434 -ErrorAction SilentlyContinue
    if ($port11434Connection) {
        Write-Host "  WARNING Port 11434 is in use (needed for Ollama API)" -ForegroundColor Yellow
        $port11434InUse = $true
    } else {
        Write-Host "  OK Port 11434 available (Ollama API)" -ForegroundColor Green
    }
} catch {
    Write-Host "  OK Port 11434 available (Ollama API)" -ForegroundColor Green
}

# Check 5: Disk space
Write-Host ""
Write-Host "[5/6] Checking disk space..." -ForegroundColor Yellow
try {
    $drive = Get-PSDrive -Name C
    $freeSpaceGB = [math]::Round($drive.Free / 1GB, 2)

    if ($freeSpaceGB -ge 10) {
        Write-Host "  OK Sufficient disk space: $freeSpaceGB GB available" -ForegroundColor Green
    } elseif ($freeSpaceGB -ge 5) {
        Write-Host "  WARNING Low disk space: $freeSpaceGB GB available (10GB recommended)" -ForegroundColor Yellow
    } else {
        Write-Host "  ERROR Insufficient disk space: $freeSpaceGB GB available (need 10GB)" -ForegroundColor Red
        $allPassed = $false
    }
} catch {
    Write-Host "  WARNING Could not check disk space" -ForegroundColor Yellow
}

# Check 6: Check if Ollama image exists
Write-Host ""
Write-Host "[6/6] Checking Docker images..." -ForegroundColor Yellow
try {
    $images = docker images --format "{{.Repository}}:{{.Tag}}" 2>$null
    if ($images -match "ollama/ollama") {
        Write-Host "  OK Ollama image already downloaded (saves time!)" -ForegroundColor Green
    } else {
        Write-Host "  INFO Ollama image not found (will download on first run ~500MB)" -ForegroundColor Cyan
    }
} catch {
    Write-Host "  WARNING Could not check Docker images" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan

if ($allPassed) {
    Write-Host "OK All critical checks passed!" -ForegroundColor Green

    if ($port8080InUse -or $port11434InUse) {
        Write-Host ""
        Write-Host "WARNING Some ports are in use." -ForegroundColor Yellow
        Write-Host "   You will need to stop services using these ports or modify docker-compose.yml" -ForegroundColor Yellow
    }

    Write-Host ""
    Write-Host "Ready to run Phase 1!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. docker-compose up" -ForegroundColor White
    Write-Host "  2. Wait for model download (3GB)" -ForegroundColor White
    Write-Host "  3. Open http://localhost:8080" -ForegroundColor White
    Write-Host ""
    Write-Host "Estimated time:" -ForegroundColor Cyan
    Write-Host "  First run: 10 minutes" -ForegroundColor White
    Write-Host "  Subsequent runs: 30 seconds" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "ERROR Some critical checks failed." -ForegroundColor Red
    Write-Host "   Please fix the issues above before proceeding." -ForegroundColor Yellow
    Write-Host ""
}
