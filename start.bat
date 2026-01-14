@echo off
REM Start Dataforge Development Environment (Python 3.14+ Compatible)
REM For local development without Docker

echo.
echo ========================================
echo   Dataforge - Application Startup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.12+
    pause
    exit /b 1
)

echo + Python found

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 20+
    pause
    exit /b 1
)

echo + Node.js found
echo.

REM Start Backend
echo [1/2] Starting Backend Server (port 8000)...
start "Dataforge Backend" cmd /k "cd backend && set PYTHONPATH=. && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

REM Wait for backend
timeout /t 4 /nobreak

REM Start Frontend
echo [2/2] Starting Frontend Server (port 5173)...
start "Dataforge Frontend" cmd /k "cd frontend && npm run dev"

REM Wait for frontend
timeout /t 3 /nobreak

echo.
echo ========================================
echo    ✓ Application Ready!
echo ========================================
echo.
echo Frontend:  http://localhost:5173
echo Backend:   http://localhost:8000
echo API Docs:  http://localhost:8000/docs
echo.
echo Close the terminal windows to stop.
echo.
pause
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
