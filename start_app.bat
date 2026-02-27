@echo off
echo ========================================
echo Starting Kerala Cities Crowd Detection
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python first.
    pause
    exit /b 1
)

echo [1/3] Starting Backend Server...
start "Backend Server" /MIN python run_backend.py

REM Wait for backend to start
timeout /t 5 /nobreak >nul 2>&1

echo [2/3] Starting Frontend Server...
cd frontend
start "Frontend Server" /MIN python -m http.server 8000
cd ..

REM Wait for frontend to start
timeout /t 2 /nobreak >nul 2>&1

echo [3/3] Opening browser...
start http://localhost:8000

echo.
echo ========================================
echo Application Started!
echo ========================================
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8000
echo.
echo Both servers are running in background.
echo Close this window to keep servers running.
echo.
echo To stop servers, close the "Backend Server" 
echo and "Frontend Server" windows.
echo ========================================
pause

