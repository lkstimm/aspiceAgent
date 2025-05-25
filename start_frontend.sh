#!/bin/bash

echo "Starting Autonomous ASPICE Platform Frontend..."

# Install dependencies if not already installed
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Start the Next.js development server
echo "Starting Next.js server on port 3000..."
cd frontend && npm run dev -- --port 3000 --host 0.0.0.0