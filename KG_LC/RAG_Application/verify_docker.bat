@echo off
REM Docker Verification Script
REM Checks Docker setup before launching RAG application

echo.
echo ============================================
echo  RAG Application - Docker Verification
echo ============================================
echo.

REM Check if Python is available
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Run verification script
python verify_docker.py
if %errorlevel% neq 0 (
    echo.
    echo Some checks failed. Please review the issues above.
    echo.
    pause
    exit /b 1
)

echo.
echo Ready to launch! Starting Docker...
echo.
pause

docker-compose up --build
