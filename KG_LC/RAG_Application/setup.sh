#!/bin/bash

# RAG Application Setup Script for macOS/Linux

echo ""
echo "====================================="
echo "RAG Document Assistant Setup"
echo "====================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.9+ from https://www.python.org/"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "Please edit .env and add your OpenAI API key"
    echo ""
fi

# Create required directories
echo "Creating required directories..."
mkdir -p indexes sessions logs exports

echo ""
echo "====================================="
echo "Setup Complete!"
echo "====================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OpenAI API key"
echo "2. Run the application with:"
echo "   streamlit run app.py"
echo ""
echo "For more information, see README.md"
echo ""
