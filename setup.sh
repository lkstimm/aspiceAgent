#!/bin/bash

echo "Setting up Autonomous ASPICE Consulting Platform..."

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Create necessary directories
echo "Creating directories..."
mkdir -p uploads
mkdir -p chroma_db
mkdir -p static

# Initialize database (SQLite for development)
echo "Initializing database..."
python -c "
import asyncio
from app.core.database import init_db
asyncio.run(init_db())
"

echo "Setup complete!"
echo ""
echo "To start the platform:"
echo "1. Backend: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo "2. Frontend: npm run dev -- --port 3000 --host 0.0.0.0"
echo ""
echo "Don't forget to set your ANTHROPIC_API_KEY in the .env file!"