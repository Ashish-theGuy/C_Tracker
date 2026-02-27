@echo off
echo ========================================
echo Stopping Kerala Cities Application
echo ========================================
echo.

echo Stopping Backend Server (port 5000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
    echo Backend server stopped.
)

echo Stopping Frontend Server (port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
    echo Frontend server stopped.
)

echo.
echo ========================================
echo All servers stopped!
echo ========================================
pause

