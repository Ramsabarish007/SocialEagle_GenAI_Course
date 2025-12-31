# PowerShell Docker Setup Script for RAG Application
# Run with: powershell -ExecutionPolicy Bypass -File docker-launcher.ps1

param(
    [string]$Action = "menu"
)

function Show-Menu {
    Clear-Host
    Write-Host "`n"
    Write-Host "============================================"
    Write-Host "  RAG Application - Docker Manager"
    Write-Host "============================================`n"
    Write-Host "1. Build and Start Application"
    Write-Host "2. Start Application (Already Built)"
    Write-Host "3. Stop Application"
    Write-Host "4. View Logs (Follow)"
    Write-Host "5. Restart Application"
    Write-Host "6. Remove All Containers and Volumes"
    Write-Host "7. Setup Configuration (First Time)"
    Write-Host "8. Check Docker Status"
    Write-Host "9. Exit`n"
}

function Verify-Docker {
    try {
        $dockerVersion = docker --version 2>$null
        if (-not $dockerVersion) {
            throw "Docker not found"
        }
        
        # Check if daemon is running
        docker ps >$null 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Docker daemon not running"
        }
        
        return $true
    }
    catch {
        Write-Host "ERROR: Docker is not available or not running" -ForegroundColor Red
        Write-Host "Please install Docker Desktop: https://www.docker.com/products/docker-desktop"
        Read-Host "Press Enter to exit"
        exit 1
    }
}

function Build-Start {
    Clear-Host
    Write-Host "`nBuilding Docker image and starting application..." -ForegroundColor Green
    Write-Host "This may take 2-5 minutes on first run`n"
    
    docker-compose up --build
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[OK] Application is running`n" -ForegroundColor Green
        Write-Host "Access it at: http://localhost:8501" -ForegroundColor Cyan
    } else {
        Write-Host "`nERROR during build/start" -ForegroundColor Red
    }
    Read-Host "Press Enter to continue"
}

function Start-App {
    Clear-Host
    Write-Host "`nStarting application...`n" -ForegroundColor Green
    
    docker-compose up
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[OK] Application is running`n" -ForegroundColor Green
        Write-Host "Access it at: http://localhost:8501" -ForegroundColor Cyan
    } else {
        Write-Host "`nERROR during start" -ForegroundColor Red
    }
    Read-Host "Press Enter to continue"
}

function Stop-App {
    Clear-Host
    Write-Host "`nStopping application...`n" -ForegroundColor Yellow
    
    docker-compose down
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[OK] Application stopped" -ForegroundColor Green
    } else {
        Write-Host "`nERROR during stop" -ForegroundColor Red
    }
    Read-Host "Press Enter to continue"
}

function Show-Logs {
    Clear-Host
    Write-Host "`nShowing application logs (Press Ctrl+C to exit)...`n" -ForegroundColor Green
    
    docker-compose logs -f
}

function Restart-App {
    Clear-Host
    Write-Host "`nRestarting application...`n" -ForegroundColor Yellow
    
    docker-compose restart
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[OK] Application restarted" -ForegroundColor Green
        Write-Host "Access it at: http://localhost:8501" -ForegroundColor Cyan
    } else {
        Write-Host "`nERROR during restart" -ForegroundColor Red
    }
    Read-Host "Press Enter to continue"
}

function Clean-Docker {
    Clear-Host
    Write-Host "`nWARNING: This will remove all containers and data volumes!" -ForegroundColor Red
    Write-Host "You will lose: indexes, sessions, logs, exports`n"
    
    $confirm = Read-Host "Type 'yes' to confirm"
    if ($confirm -ne "yes") {
        return
    }
    
    Write-Host "`nRemoving containers and volumes...`n" -ForegroundColor Yellow
    docker-compose down -v
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[OK] All containers and volumes removed" -ForegroundColor Green
    } else {
        Write-Host "`nERROR during cleanup" -ForegroundColor Red
    }
    Read-Host "Press Enter to continue"
}

function Setup-Config {
    Clear-Host
    Write-Host "`n============================================" -ForegroundColor Green
    Write-Host "  Configuration Setup"
    Write-Host "============================================`n"
    
    if (-not (Test-Path "docker.env")) {
        if (Test-Path "docker.env.example") {
            Copy-Item "docker.env.example" "docker.env"
            Write-Host "[OK] docker.env created from template" -ForegroundColor Green
            Write-Host "`nPlease edit docker.env with your OpenAI API key:" -ForegroundColor Yellow
            Write-Host "- Open docker.env in your text editor"
            Write-Host "- Replace OPENAI_API_KEY with your actual key"
            Write-Host "- Save the file`n"
            
            if ((Read-Host "Open docker.env now? (y/n)") -eq "y") {
                notepad docker.env
            }
        } else {
            Write-Host "ERROR: docker.env.example not found" -ForegroundColor Red
        }
    } else {
        Write-Host "docker.env already exists" -ForegroundColor Green
        Write-Host "To reconfigure, edit the file directly`n"
        
        if ((Read-Host "Open docker.env now? (y/n)") -eq "y") {
            notepad docker.env
        }
    }
    Read-Host "Press Enter to continue"
}

function Show-Status {
    Clear-Host
    Write-Host "`n============================================" -ForegroundColor Green
    Write-Host "  Docker Status"
    Write-Host "============================================`n"
    
    Write-Host "Docker version:" -ForegroundColor Cyan
    docker --version
    
    Write-Host "`nDocker daemon status:" -ForegroundColor Cyan
    docker ps --quiet >$null 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Running" -ForegroundColor Green
    } else {
        Write-Host "Not running" -ForegroundColor Red
    }
    
    Write-Host "`nRunning containers:" -ForegroundColor Cyan
    $containers = docker ps --format "{{.Names}}`t{{.Status}}" 2>$null
    if ($containers) {
        $containers
    } else {
        Write-Host "None" -ForegroundColor Yellow
    }
    
    Write-Host "`nDocker images:" -ForegroundColor Cyan
    docker images --format "{{.Repository}}:{{.Tag}}`t{{.Size}}" | Select-Object -First 10
    
    Write-Host ""
    Read-Host "Press Enter to continue"
}

# Main logic
Verify-Docker

do {
    Show-Menu
    $choice = Read-Host "Enter your choice (1-9)"
    
    switch ($choice) {
        "1" { Build-Start }
        "2" { Start-App }
        "3" { Stop-App }
        "4" { Show-Logs }
        "5" { Restart-App }
        "6" { Clean-Docker }
        "7" { Setup-Config }
        "8" { Show-Status }
        "9" { exit 0 }
        default { Write-Host "Invalid choice, please try again" -ForegroundColor Red; Start-Sleep -Seconds 1 }
    }
} while ($true)
