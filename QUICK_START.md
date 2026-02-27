# 🚀 Quick Start Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Process Your 7 Videos

### Edit `process_hackathon_videos.py`:
- Update video paths in `LOCATIONS` list
- Update coordinates for each location

### Run processing:
```bash
python process_hackathon_videos.py
```

## Step 3: Start Backend

```bash
python run_backend.py
```

Backend runs on: `http://localhost:5000`

## Step 4: Open Frontend

### Option 1: Simple Server
```bash
cd frontend
python -m http.server 8000
```
Open: `http://localhost:8000`

### Option 2: VS Code Live Server
Right-click `frontend/index.html` → "Open with Live Server"

## Step 5: Use the System

1. **Query a Location**: Enter location name and get crowd analysis
2. **Get Recommendations**: Enter your location to get nearby alternatives
3. **View All Locations**: See all processed locations and their status

## 🎯 For Hackathon Demo

1. Process videos from 7 different places
2. Show real-time crowd analysis
3. Demonstrate AI recommendations
4. Show nearby alternatives with less crowd

## 📡 Test API Directly

```bash
# Get all locations
curl http://localhost:5000/api/all-locations

# Query a location
curl -X POST http://localhost:5000/api/query-location \
  -H "Content-Type: application/json" \
  -d '{"location_name": "Central Park"}'
```

## ✅ System Features

- ✅ Process videos from multiple locations
- ✅ Real-time crowd analysis
- ✅ AI-powered recommendations
- ✅ Trend detection (increasing/decreasing)
- ✅ Nearby location suggestions
- ✅ Beautiful web interface

