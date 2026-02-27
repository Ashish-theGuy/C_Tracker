@echo off
REM Fully automated startup - no prompts
title Kerala Cities App

REM Start backend in background
start "Backend Server" /MIN python run_backend.py

REM Wait for backend
timeout /t 5 /nobreak >nul 2>&1

REM Start frontend in background
cd frontend
start "Frontend Server" /MIN python -m http.server 8000
cd ..

REM Wait for frontend
timeout /t 2 /nobreak >nul 2>&1

REM Open browser
start http://localhost:8000

REM Exit (servers run in background)
exit

