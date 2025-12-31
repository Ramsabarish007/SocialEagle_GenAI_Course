# Multi-stage Dockerfile optimized for RAG application
# Uses Python 3.10 slim image to minimize native compilation issues
# Optimized for Windows hosts

FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies (minimal, to avoid wheel compilation issues)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements-docker.txt .

# Install Python dependencies
# Use --no-binary for packages that have wheel issues, pre-built wheels otherwise
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements-docker.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p indexes sessions logs exports data

# Expose port for Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["streamlit", "run", "app.py"]
