@echo off
REM Docker Setup and Launch Script for RAG Application
REM Run this to easily manage Docker containers on Windows

setlocal enabledelayedexpansion

cls
echo.
echo ============================================
echo   RAG Application - Docker Manager
echo ============================================
echo.

REM Check if Docker is installed
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

REM Check if Docker daemon is running
docker ps >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Docker daemon is not running
    echo Please start Docker Desktop and try again
    echo.
    pause
    exit /b 1
)

:menu
cls
echo.
echo ============================================
echo   Docker Management Menu
echo ============================================
echo.
echo 1. Build and Start Application
echo 2. Start Application (Already Built)
echo 3. Stop Application
echo 4. View Logs
echo 5. Restart Application
echo 6. Remove All Containers and Volumes
echo 7. Setup Configuration (First Time)
echo 8. Check Docker Status
echo 9. Exit
echo.
set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto build_start
if "%choice%"=="2" goto start
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto restart
if "%choice%"=="6" goto clean
if "%choice%"=="7" goto setup_config
if "%choice%"=="8" goto status
if "%choice%"=="9" goto exit_menu
goto menu

:setup_config
cls
echo.
echo ============================================
echo   Configuration Setup
echo ============================================
echo.
if not exist docker.env (
    echo Creating docker.env from template...
    if exist docker.env.example (
        copy docker.env.example docker.env
        echo [OK] docker.env created
        echo.
        echo Please edit docker.env with your OpenAI API key:
        echo - Open docker.env in your text editor
        echo - Replace OPENAI_API_KEY with your actual key
        echo - Save the file
        echo.
        pause
    ) else (
        echo ERROR: docker.env.example not found
        pause
    )
) else (
    echo docker.env already exists
    echo To reconfigure, edit the file directly
    pause
)
goto menu

:build_start
cls
echo.
echo Building Docker image and starting application...
echo This may take 2-5 minutes on first run
echo.
docker-compose up --build
if %errorlevel% equ 0 (
    echo.
    echo [OK] Application is running
    echo Access it at: http://localhost:8501
) else (
    echo ERROR during build/start
    pause
)
goto menu

:start
cls
echo.
echo Starting application...
echo.
docker-compose up
if %errorlevel% equ 0 (
    echo.
    echo [OK] Application is running
    echo Access it at: http://localhost:8501
) else (
    echo ERROR during start
    pause
)
goto menu

:stop
cls
echo.
echo Stopping application...
docker-compose down
if %errorlevel% equ 0 (
    echo [OK] Application stopped
) else (
    echo ERROR during stop
)
pause
goto menu

:restart
cls
echo.
echo Restarting application...
docker-compose restart
if %errorlevel% equ 0 (
    echo [OK] Application restarted
    echo Access it at: http://localhost:8501
) else (
    echo ERROR during restart
)
pause
goto menu

:logs
cls
echo.
echo Showing application logs (Press Ctrl+C to exit)...
echo.
docker-compose logs -f
goto menu

:clean
cls
echo.
echo WARNING: This will remove all containers and data volumes!
echo You will lose: indexes, sessions, logs, exports
echo.
set /p confirm="Type 'yes' to confirm: "
if /i not "%confirm%"=="yes" goto menu

echo.
echo Removing containers and volumes...
docker-compose down -v
if %errorlevel% equ 0 (
    echo [OK] All containers and volumes removed
) else (
    echo ERROR during cleanup
)
pause
goto menu

:status
cls
echo.
echo ============================================
echo   Docker Status
echo ============================================
echo.
echo Checking Docker daemon:
docker info | findstr "Containers:"
echo.
echo Running containers:
docker ps --format "table {{.Names}}\t{{.Status}}"
echo.
echo Docker images:
docker images --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}"
echo.
pause
goto menu

:exit_menu
echo.
echo Exiting...
echo.
exit /b 0
