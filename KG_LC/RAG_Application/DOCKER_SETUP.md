# Windows Docker Setup Guide for RAG Application

## 🐳 Docker for Windows Setup

This guide helps you run the RAG Application in Docker on Windows.

### Prerequisites

1. **Docker Desktop for Windows**
   - Download: https://www.docker.com/products/docker-desktop
   - Requires Windows 10/11 Pro, Enterprise, or Education
   - 4GB+ RAM recommended
   - WSL 2 backend (easier than Hyper-V)

2. **Verify Docker Installation**
   ```powershell
   docker --version
   docker run hello-world
   ```

### Quick Start (5 Minutes)

#### Step 1: Prepare Configuration
```powershell
# Copy environment template
Copy-Item docker.env.example docker.env

# Edit docker.env with your OpenAI API key
notepad docker.env
# Add: OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

#### Step 2: Build and Run with Docker Compose
```powershell
# Navigate to project directory
cd RAG_Application

# Build and start
docker-compose up --build

# Application starts at http://localhost:8501
```

#### Step 3: Stop Container
```powershell
# In same directory
docker-compose down
```

### Docker Compose Commands

```powershell
# Build image
docker-compose build

# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove everything (careful!)
docker-compose down -v
```

### Manual Docker Commands (Alternative)

```powershell
# Build image
docker build -t rag-app:latest .

# Run container
docker run -it `
  -p 8501:8501 `
  -v ${PWD}:/app `
  -v rag_indexes:/app/indexes `
  -v rag_sessions:/app/sessions `
  -v rag_logs:/app/logs `
  -v rag_exports:/app/exports `
  -v rag_data:/app/data `
  --env-file docker.env `
  --name rag-assistant `
  rag-app:latest

# Access logs
docker logs rag-assistant

# Stop container
docker stop rag-assistant

# Remove container
docker rm rag-assistant
```

## 📁 Docker Volumes Explained

The docker-compose.yml creates persistent volumes:

| Volume | Location | Purpose |
|--------|----------|---------|
| `rag_indexes` | `/app/indexes` | FAISS vector indexes |
| `rag_sessions` | `/app/sessions` | Conversation sessions |
| `rag_logs` | `/app/logs` | Application logs |
| `rag_exports` | `/app/exports` | Exported reports |
| `rag_data` | `/app/data` | Uploaded documents |

**Benefits:**
- Data persists between container restarts
- Multiple containers can share volumes
- Easy backup and restoration
- Independent from application updates

## 🔧 Troubleshooting

### Problem: "Docker daemon is not running"
**Solution:**
1. Open Docker Desktop application
2. Wait for it to fully initialize
3. Check system tray for Docker icon
4. Try command again

### Problem: "Port 8501 is already in use"
**Solution:**
```powershell
# Option 1: Change port in docker-compose.yml
# Change "8501:8501" to "8502:8501"

# Option 2: Kill process using port
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Option 3: Use different port with docker run
docker run -p 8502:8501 rag-app:latest
```

### Problem: "API key not recognized in container"
**Solution:**
```powershell
# 1. Verify docker.env exists
Test-Path docker.env

# 2. Check docker.env content
type docker.env

# 3. Verify OpenAI API key is correct

# 4. Rebuild with new env
docker-compose up --build
```

### Problem: "Out of memory" errors
**Solution:**
1. Increase Docker Desktop memory:
   - Docker Desktop Settings → Resources
   - Increase Memory to 4GB+ or more
2. Reduce CHUNK_SIZE in docker.env:
   - Set CHUNK_SIZE=750
3. Reduce document upload size

### Problem: "Volume permission denied"
**Solution:**
```powershell
# Recreate volumes
docker volume rm rag_indexes rag_sessions rag_logs rag_exports rag_data
docker-compose up --build
```

### Problem: Slow performance in Docker
**Solution:**
1. Check Docker Desktop resource allocation
2. Use WSL 2 backend (faster than Hyper-V)
3. Ensure your SSD has sufficient space
4. Disable Windows Defender scanning of Docker directory

## 📊 Monitoring Container

```powershell
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View container resource usage
docker stats

# View container logs
docker logs rag-assistant
docker logs -f rag-assistant  # Follow logs

# Execute command in running container
docker exec -it rag-assistant bash
docker exec -it rag-assistant python examples.py
```

## 🔐 Security Considerations

### API Key Management
```powershell
# Never commit docker.env to git
# .gitignore already includes it

# Best practice: Use Docker secrets (for production)
# Or use environment variable injection
docker-compose up --env-file docker.env.prod
```

### Container Security
```powershell
# Run as non-root (recommended for production)
# Uncomment in Dockerfile:
# RUN useradd -m appuser
# USER appuser

# Network isolation
# docker-compose.yml creates isolated network

# Resource limits (add to docker-compose.yml)
# deploy:
#   resources:
#     limits:
#       cpus: '1'
#       memory: 2G
```

## 🚀 Production Deployment

### Docker Registry
```powershell
# Tag image
docker tag rag-app:latest myregistry/rag-app:1.0.0

# Push to registry
docker push myregistry/rag-app:1.0.0
```

### Docker Swarm / Kubernetes
```powershell
# Initialize swarm
docker swarm init

# Deploy service
docker service create --name rag-app \
  -p 8501:8501 \
  --env-file docker.env \
  myregistry/rag-app:1.0.0
```

### Compose with Environment-Specific Files
```powershell
# Development
docker-compose -f docker-compose.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 📈 Performance Optimization

### Reduce Image Size
```dockerfile
# Use slim variant
FROM python:3.10-slim

# Multi-stage builds
FROM python:3.10 AS builder
FROM python:3.10-slim
COPY --from=builder /usr/local/lib /usr/local/lib
```

### Caching Strategy
```dockerfile
# Copy requirements first (caches layer)
COPY requirements-docker.txt .
RUN pip install -r requirements-docker.txt

# Then copy application
COPY . .
```

### Health Checks
Already configured in docker-compose.yml:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## 🧹 Cleanup

```powershell
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Deep clean (removes everything)
docker system prune -a --volumes
```

## 📚 Additional Resources

- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **Docker for Windows**: https://docs.docker.com/docker-for-windows/
- **Dockerfile Reference**: https://docs.docker.com/engine/reference/builder/

## ✅ Verification Checklist

- [ ] Docker Desktop installed and running
- [ ] docker.env created with API key
- [ ] docker-compose.yml exists in project
- [ ] Dockerfile exists in project
- [ ] `docker-compose up --build` succeeds
- [ ] Application accessible at http://localhost:8501
- [ ] Can upload documents
- [ ] Can ask questions
- [ ] Volumes persist after restart

## 🎯 Common Tasks

### Update Application Code
```powershell
# Changes are live (volume mount)
# Just refresh browser
```

### Update Dependencies
```powershell
# Modify requirements-docker.txt
# Rebuild
docker-compose up --build
```

### View Logs
```powershell
docker-compose logs app
docker-compose logs -f app  # Follow
```

### Backup Data
```powershell
# Export volumes
docker run --rm -v rag_sessions:/data -v ${PWD}:/backup ^
  alpine tar czf /backup/sessions.tar.gz -C /data .
```

### Restore Data
```powershell
# Import volumes
docker run --rm -v rag_sessions:/data -v ${PWD}:/backup ^
  alpine tar xzf /backup/sessions.tar.gz -C /data
```

---

**Version**: 1.0.0  
**Last Updated**: December 2024  
**Works On**: Windows 10/11 Pro+, Docker Desktop 4.0+
