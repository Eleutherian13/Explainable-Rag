# Start Dataforge Development Environment

Write-Host "🚀 Starting Dataforge Application..." -ForegroundColor Green
Write-Host ""

# Start Backend
Write-Host "📦 Starting Backend (FastAPI)..." -ForegroundColor Cyan
$backendProcess = Start-Process powershell -ArgumentList @"
    `$env:PYTHONPATH = 'c:\Users\manas\OneDrive\Desktop\Dataforge\backend'
    cd 'c:\Users\manas\OneDrive\Desktop\Dataforge\backend'
    python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
"@ -PassThru -WindowStyle Normal

Start-Sleep -Seconds 3

# Start Frontend
Write-Host "🎨 Starting Frontend (React + Vite)..." -ForegroundColor Cyan
$frontendProcess = Start-Process powershell -ArgumentList @"
    cd 'c:\Users\manas\OneDrive\Desktop\Dataforge\frontend'
    npm run dev
"@ -PassThru -WindowStyle Normal

Start-Sleep -Seconds 5

Write-Host ""
Write-Host "✅ Application Started!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 URLs:" -ForegroundColor Yellow
Write-Host "   Frontend:  http://localhost:5173" -ForegroundColor Cyan
Write-Host "   Backend:   http://localhost:8000" -ForegroundColor Cyan
Write-Host "   API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "To stop the application, close the terminal windows." -ForegroundColor Yellow
Write-Host ""

# Keep this window open
Read-Host "Press Enter to exit"
