# 🚀 Quick Start Guide

## One-Click Startup

### Windows (Easiest Method)

**Double-click:** `start_app.bat`

This will automatically:
1. ✅ Start the backend server (port 5000)
2. ✅ Start the frontend server (port 8000)
3. ✅ Open your browser to http://localhost:8000

### PowerShell Method

```powershell
.\start_app.ps1
```

## Manual Startup (If needed)

### Step 1: Start Backend
```bash
python run_backend.py
```

### Step 2: Start Frontend (in new terminal)
```bash
cd frontend
python -m http.server 8000
```

### Step 3: Open Browser
```
http://localhost:8000
```

## Stop the Application

**Double-click:** `stop_app.bat`

Or manually close the server windows.

## What Happens on Startup

1. **Backend starts** → Analyzes videos with YOLO
2. **Frontend starts** → Web interface loads
3. **Browser opens** → Ready to ask questions!

## Troubleshooting

### Port Already in Use
- Run `stop_app.bat` first
- Or manually close any running Python servers

### Python Not Found
- Install Python from python.org
- Make sure "Add Python to PATH" is checked

### Videos Not Found
- Ensure all 7 city videos are in the project root:
  - City1.mp4, city2.mp4, ..., city7.mp4

## Quick Commands

```bash
# Start everything
start_app.bat

# Stop everything  
stop_app.bat

# Reprocess a city video
python reprocess_kochi.py
python reprocess_varkala.py

# Process all cities
python process_all_cities.py
```

## Ready to Use!

Once started, just type questions like:
- "Should I visit Munnar?"
- "Is Kochi crowded?"
- "What's the crowd like in Varkala?"

The AI will analyze the videos and show live YOLO detection! 🎯

