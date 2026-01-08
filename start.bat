@echo off
REM Quick start script for Explainable RAG application (Windows)

echo ================================
echo Explainable RAG - Quick Start
echo ================================
echo.

REM Check for Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo X Docker not found. Please install Docker Desktop.
    pause
    exit /b 1
)

echo + Docker found

REM Check for Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo X Docker Compose not found. Please install Docker Desktop.
    pause
    exit /b 1
)

echo + Docker Compose found

REM Check for .env file
if not exist .env (
    echo ! .env file not found. Creating from template...
    copy .env.example .env
    echo Please edit .env and add your OpenAI API key if desired
    echo Then run this script again
    echo.
    echo To get your OpenAI API key:
    echo   1. Go to https://platform.openai.com/account/api-keys
    echo   2. Create a new secret key
    echo   3. Add it to .env: OPENAI_API_KEY=sk-...
    pause
    exit /b 0
)

echo + .env file found

REM Stop any existing containers
echo.
echo Stopping any existing containers...
docker-compose down --remove-orphans >nul 2>&1

REM Build images
echo.
echo Building Docker images...
echo This may take 2-5 minutes on first run...
docker-compose build

REM Start services
echo.
echo Starting services...
docker-compose up -d

REM Wait for services
echo.
echo Waiting for services to start...
timeout /t 5 /nobreak

REM Check status
echo.
echo Checking service status...

setlocal enabledelayedexpansion
set "attempts=0"

:wait_loop
if !attempts! geq 30 goto timeout
set /a attempts=!attempts!+1

echo Attempt !attempts!/30: Waiting for services...
timeout /t 2 /nobreak

goto wait_loop

:timeout
echo.
echo ================================
echo + Setup Complete!
echo ================================
echo.
echo + Backend API is running
echo   Location: http://localhost:8000
echo   Docs: http://localhost:8000/docs
echo.
echo + Frontend is running
echo   URL: http://localhost:3000
echo.
echo Next Steps:
echo   1. Open http://localhost:3000 in your browser
echo   2. Upload some documents (PDF, TXT, or MD files)
echo   3. Ask a question about the documents
echo   4. View the knowledge graph and explanations
echo.
echo Documentation:
echo   - Full guide: README.md
echo   - Getting started: GETTING_STARTED.md
echo   - View logs: docker-compose logs -f
echo.
echo To stop:
echo   docker-compose down
echo.
echo Happy exploring!
echo.
pause
