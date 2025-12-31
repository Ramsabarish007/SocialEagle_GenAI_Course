@echo off
REM RAG Application Setup Script for Windows

echo.
echo =====================================
echo RAG Document Assistant Setup
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo Please edit .env and add your OpenAI API key
    echo.
)

REM Create required directories
echo Creating required directories...
if not exist "indexes" mkdir indexes
if not exist "sessions" mkdir sessions
if not exist "logs" mkdir logs
if not exist "exports" mkdir exports

echo.
echo =====================================
echo Setup Complete!
echo =====================================
echo.
echo Next steps:
echo 1. Edit .env and add your OpenAI API key
echo 2. Run the application with:
echo    streamlit run app.py
echo.
echo For more information, see README.md
echo.
pause
