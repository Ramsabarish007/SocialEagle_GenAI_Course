# Docker Troubleshooting & Quick Reference Guide

## 🚀 Quick Start (Copy-Paste Commands)

### Windows Command Prompt (cmd.exe)
```cmd
cd RAG_Application
docker-compose up --build
```

### Windows PowerShell
```powershell
cd RAG_Application
docker-compose up --build
```

### Using Launcher Scripts
```cmd
REM Batch file (Windows)
docker-launcher.bat
```

```powershell
# PowerShell script
powershell -ExecutionPolicy Bypass -File docker-launcher.ps1
```

## 📋 Command Reference

| Command | Purpose |
|---------|---------|
| `docker-compose up --build` | Build image and start application |
| `docker-compose up` | Start application (no rebuild) |
| `docker-compose down` | Stop application |
| `docker-compose logs -f` | View live logs |
| `docker-compose ps` | Show running containers |
| `docker-compose restart` | Restart application |
| `docker volume ls` | List all volumes |
| `docker image ls` | List all images |
| `docker system prune -a` | Deep clean (careful!) |

## 🐛 Common Issues & Solutions

### Issue 1: "Docker daemon is not running"
```powershell
# Windows: Start Docker Desktop
# Check system tray, click Docker icon to start

# Verify it's running
docker ps
```

### Issue 2: "Port 8501 is already in use"
```powershell
# Option A: Find and stop process
netstat -ano | findstr :8501
taskkill /PID {PID} /F

# Option B: Change port in docker-compose.yml
# Change line: "8501:8501"
# To: "8502:8501"
```

### Issue 3: "API key not found" in container
```powershell
# 1. Verify docker.env exists
Test-Path docker.env

# 2. Check file content
Get-Content docker.env

# 3. Ensure OPENAI_API_KEY=<YOUR_OPENAI_API_KEY> is set

# 4. Rebuild
docker-compose up --build
```

### Issue 4: "No space left on device"
```powershell
# Clean up Docker
docker system prune -a --volumes

# Or delete specific volumes
docker volume rm rag_indexes rag_sessions
```

### Issue 5: "Permission denied" on volumes
```powershell
# Recreate volumes
docker-compose down -v
docker-compose up --build
```

### Issue 6: Out of memory errors
1. Open Docker Desktop → Settings → Resources
2. Increase memory to 4GB or more
3. Or reduce CHUNK_SIZE in docker.env to 750

### Issue 7: Slow file sync (Windows)
**Windows Containers** can be slow with volume sync:
```powershell
# Use named volumes instead of bind mounts
# Modify docker-compose.yml

volumes:
  - /app  # Named volume, much faster
  - rag_data:/app/data
```

### Issue 8: "Cannot connect to Docker daemon"
```powershell
# WSL 2 setup (Windows 11)
wsl -l -v

# If WSL 2 not running, enable it
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
```

## 🔍 Debugging Commands

```powershell
# Get detailed container info
docker-compose ps -a

# View container logs with timestamps
docker-compose logs --timestamps -f

# Execute command in running container
docker-compose exec rag-app bash
docker-compose exec rag-app python -c "import langchain; print(langchain.__version__)"

# View resource usage
docker stats

# Inspect container configuration
docker-compose config

# Validate docker-compose.yml
docker-compose config --quiet && echo "Valid"
```

## 🧪 Testing Container

```powershell
# After starting: docker-compose up

# Test API endpoint
curl http://localhost:8501/_stcore/health

# Test Python environment
docker-compose exec rag-app python -c "
import langchain
import openai
import faiss
print('✓ All imports successful')
print(f'LangChain: {langchain.__version__}')
print(f'OpenAI: {openai.__version__}')
"

# View Streamlit logs
docker-compose logs rag-app | findstr "streamlit\|Listening"
```

## 📊 Performance Monitoring

```powershell
# Real-time resource usage
docker stats --no-stream

# Container inspection
docker-compose exec rag-app top

# Disk usage
docker system df

# Image size breakdown
docker-compose images

# Volume size
docker volume inspect rag_data | findstr Mountpoint
Get-ChildItem "C:\ProgramData\Docker\volumes\{hash}\_data" -Recurse | Measure-Object -Sum Length | ForEach-Object {
    Write-Host "Total size: $([math]::Round($_.Sum/1MB)) MB"
}
```

## 🔐 Security Checks

```powershell
# View secrets in docker.env (be careful!)
Get-Content docker.env | Select-String "OPENAI_API_KEY"

# Never commit docker.env to git
git status | findstr docker.env  # Should be ignored

# Check .gitignore
Get-Content .gitignore | findstr "docker.env"

# Scan Docker images
docker scan rag-app:latest
```

## 📈 Scaling & Production

```powershell
# Run multiple replicas (requires load balancer)
docker-compose up -d --scale rag-app=3

# Stop all containers
docker-compose down

# Backup volumes
docker run --rm -v rag_sessions:/data -v $PWD:/backup alpine tar czf /backup/sessions.tar.gz -C /data .

# Restore volumes
docker run --rm -v rag_sessions:/data -v $PWD:/backup alpine tar xzf /backup/sessions.tar.gz -C /data
```

## 🎓 Learning Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## ✅ Pre-Launch Checklist

- [ ] Docker Desktop installed and running
- [ ] docker.env file created with OPENAI_API_KEY
- [ ] docker-compose.yml file exists
- [ ] Dockerfile exists in project
- [ ] At least 4GB RAM allocated to Docker
- [ ] Port 8501 not in use
- [ ] Sufficient disk space (5GB+ recommended)

## 🆘 Still Need Help?

1. Check logs: `docker-compose logs -f`
2. Review [DOCKER_SETUP.md](DOCKER_SETUP.md)
3. Run `docker-launcher.bat` or `docker-launcher.ps1` for interactive menu
4. Verify your API key: Check OpenAI dashboard (https://platform.openai.com/account/api-keys)

---

**Quick Help**: Need immediate assistance? Run:
```powershell
docker-compose exec rag-app python -c "from core import *; print('Setup OK')"
```

If this works, your Docker environment is healthy!
