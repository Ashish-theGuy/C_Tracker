@echo off
echo Stopping backend...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

timeout /t 2 /nobreak >nul 2>&1

echo Starting backend...
start "Backend Server" /MIN python run_backend.py

timeout /t 3 /nobreak >nul 2>&1

echo Backend restarted!
echo The updated Varkala data (6 people) should now be available.

