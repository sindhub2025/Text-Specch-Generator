@echo off
REM Text-to-Speech Generator - Run Script (Windows)
REM This script starts the TTS web application

echo 🎙️  Starting Offline Text-to-Speech Generator...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ⚠️  Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
)

echo.
echo ✅ Starting server on http://localhost:8000
echo 📝 Press Ctrl+C to stop the server
echo.

REM Run the application
python app.py
