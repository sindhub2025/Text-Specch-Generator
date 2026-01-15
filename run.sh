#!/bin/bash

# Text-to-Speech Generator - Run Script
# This script starts the TTS web application

echo "🎙️  Starting Offline Text-to-Speech Generator..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! pip show fastapi > /dev/null 2>&1; then
    echo "📦 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

echo ""
echo "✅ Starting server on http://localhost:8000"
echo "📝 Press Ctrl+C to stop the server"
echo ""

# Run the application
python app.py
