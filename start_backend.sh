#!/bin/bash

echo "Starting Autonomous ASPICE Platform Backend..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install dependencies if not already installed
if [ ! -d "venv" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Create directories if they don't exist
mkdir -p uploads chroma_db static

# Start the FastAPI server
echo "Starting FastAPI server on port 8000..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload