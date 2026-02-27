# PowerShell script to start the application
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Kerala Cities Crowd Detection" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found!" -ForegroundColor Red
    Write-Host "Please install Python first." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[1/3] Starting Backend Server..." -ForegroundColor Yellow
Start-Process python -ArgumentList "run_backend.py" -WindowStyle Minimized

# Wait for backend to start
Start-Sleep -Seconds 5

Write-Host "[2/3] Starting Frontend Server..." -ForegroundColor Yellow
Set-Location frontend
Start-Process python -ArgumentList "-m", "http.server", "8000" -WindowStyle Minimized
Set-Location ..

# Wait for frontend to start
Start-Sleep -Seconds 2

Write-Host "[3/3] Opening browser..." -ForegroundColor Yellow
Start-Process "http://localhost:8000"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Application Started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Backend: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Both servers are running in background." -ForegroundColor Yellow
Write-Host "Browser should open automatically." -ForegroundColor Yellow
Write-Host ""
Write-Host "To stop servers, close the minimized windows." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green

