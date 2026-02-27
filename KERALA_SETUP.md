# Kerala Cities - Setup Guide

## Overview

This system analyzes crowd conditions in 7 famous Kerala tourist spots:
1. **Munnar** - Hill station with tea plantations
2. **Alleppey** - Backwaters and houseboats
3. **Kochi** - Historic port city
4. **Wayanad** - Wildlife and waterfalls
5. **Thekkady** - National park and spice plantations
6. **Kovalam** - Beach destination
7. **Varkala** - Cliff beach

## Setup Steps

### 1. Prepare Your Videos

Create a `videos/` folder and place your 7 videos with these exact names:
- `munnar.mp4`
- `alleppey.mp4`
- `kochi.mp4`
- `wayanad.mp4`
- `thekkady.mp4`
- `kovalam.mp4`
- `varkala.mp4`

### 2. Start Backend

```bash
python run_backend.py
```

Backend runs on: `http://localhost:5000`

### 3. Process Videos

In a new terminal:
```bash
python process_kerala_videos.py
```

This will process all 7 videos and analyze crowd data.

### 4. Start Frontend

```bash
cd frontend
python -m http.server 8000
```

Or double-click: `start_frontend.bat`

Open: `http://localhost:8000`

## Usage

### Ask Questions

Type natural language questions in the prompt bar:

- "Should I visit Munnar?"
- "Is Kochi crowded?"
- "What's the crowd like in Alleppey?"
- "Should I go to Wayanad?"

### What the AI Does

1. **Analyzes the city video** - Detects people count
2. **Determines crowd level** - High/Medium/Low
3. **Analyzes trend** - Increasing/Decreasing/Stable
4. **Provides recommendation** - Should visit or avoid
5. **Suggests alternatives** - Other cities with less crowd

## API Endpoint

### Ask About a City

```
POST /api/ask
Body: {
  "query": "Should I visit Munnar?"
}
```

Response includes:
- Current crowd count
- Crowd level
- Trend (increasing/decreasing/stable)
- Recommendation
- Alternative cities with less crowd

## File Structure

```
yolo_person_detection/
├── backend/
│   ├── app.py              # Main API server
│   # (AI agent removed - crowd analysis via video_processor)
│   ├── kerala_cities.py    # 7 cities configuration
│   ├── query_processor.py  # Natural language processing
│   ├── video_processor.py # Video analysis
│   └── data_manager.py     # Data storage
├── frontend/
│   ├── index.html          # Simple prompt interface
│   ├── styles.css          # Styling
│   └── app.js             # Frontend logic
├── videos/                 # Your 7 city videos
└── data/                   # Stored analysis data
```

## For Hackathon Demo

1. Upload 7 videos (one for each Kerala city)
2. Process videos using the script
3. Demo the prompt interface
4. Ask questions about different cities
5. Show AI recommendations and alternatives

The system will automatically:
- Analyze crowd density from videos
- Detect trends (increasing/decreasing)
- Calculate distances between cities
- Recommend better alternatives

