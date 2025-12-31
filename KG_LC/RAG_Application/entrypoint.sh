#!/bin/bash
# Entrypoint script for Docker container

# Set default values
STREAMLIT_SERVER_PORT=${STREAMLIT_SERVER_PORT:-8501}
STREAMLIT_SERVER_ADDRESS=${STREAMLIT_SERVER_ADDRESS:-0.0.0.0}

# Create necessary directories if they don't exist
mkdir -p /app/indexes
mkdir -p /app/sessions
mkdir -p /app/logs
mkdir -p /app/exports
mkdir -p /app/data

# Set Streamlit config
export STREAMLIT_SERVER_PORT=$STREAMLIT_SERVER_PORT
export STREAMLIT_SERVER_ADDRESS=$STREAMLIT_SERVER_ADDRESS

# Execute passed command
exec "$@"
