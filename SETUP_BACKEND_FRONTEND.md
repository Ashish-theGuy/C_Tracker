# 🚀 Backend & Frontend Setup Guide

## Overview

This system includes:
- **Backend**: Flask API with AI agent for crowd analysis
- **Frontend**: Web interface for user interaction
- **AI Agent**: Analyzes crowd data and provides recommendations

## 📋 Prerequisites

1. Python 3.8+
2. All dependencies from `requirements.txt`
3. Processed videos from 7 locations (for hackathon)

## 🔧 Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Create Data Directory

```bash
mkdir data
```

### Step 3: Prepare Videos

1. Create a `videos` folder
2. Place your 7 location videos in it
3. Update `process_hackathon_videos.py` with your video paths and coordinates

## 🎬 Processing Videos for Hackathon (7 Locations)

### Option 1: Using the Script

1. Edit `process_hackathon_videos.py`:
   - Update `LOCATIONS` list with your video paths
   - Update coordinates for each location

2. Run the script:
```bash
python process_hackathon_videos.py
```

### Option 2: Using API

Use the `/api/process-multiple-videos` endpoint (see API docs below)

## 🖥️ Running the Backend

```bash
cd backend
python app.py
```

The server will start on `http://localhost:5000`

## 🌐 Running the Frontend

### Option 1: Simple HTTP Server

```bash
cd frontend
python -m http.server 8000
```

Then open: `http://localhost:8000`

### Option 2: Live Server (VS Code)

Use the Live Server extension in VS Code

### Option 3: Direct File

Just open `frontend/index.html` in your browser (CORS may be an issue)

## 📡 API Endpoints

### 1. Health Check
```
GET /
```

### 2. Process Single Video
```
POST /api/process-video
Body: {
  "video_path": "path/to/video.mp4",
  "location_name": "Central Park",
  "location_coords": {"lat": 40.7851, "lng": -73.9683}
}
```

### 3. Process Multiple Videos
```
POST /api/process-multiple-videos
Body: {
  "videos": [
    {
      "video_path": "videos/location1.mp4",
      "location_name": "Location 1",
      "location_coords": {"lat": 40.7851, "lng": -73.9683}
    },
    ...
  ]
}
```

### 4. Query Location
```
POST /api/query-location
Body: {
  "location_name": "Central Park",
  "user_location": {"lat": 40.7580, "lng": -73.9855}
}
```

### 5. Get Recommendations
```
POST /api/get-recommendations
Body: {
  "target_location": "Central Park",
  "user_location": {"lat": 40.7580, "lng": -73.9855}
}
```

### 6. Get All Locations
```
GET /api/all-locations
```

### 7. Get Location Status
```
GET /api/location-status/<location_name>
```

## 🎯 Usage Flow

### For Hackathon (7 Locations):

1. **Process Videos**:
   ```bash
   python process_hackathon_videos.py
   ```
   Or use the API endpoint `/api/process-multiple-videos`

2. **Query Locations**:
   - Use frontend UI, or
   - Use API endpoint `/api/query-location`

3. **Get Recommendations**:
   - Enter location name and your coordinates
   - AI agent will suggest nearby alternatives

## 🤖 AI Agent Features

The AI agent provides:
- ✅ Crowd trend analysis (increasing/decreasing/stable)
- ✅ Visit recommendations (should visit or avoid)
- ✅ Nearby location suggestions with less crowd
- ✅ Distance calculations
- ✅ Confidence levels for recommendations

## 📁 Project Structure

```
yolo_person_detection/
├── backend/
│   ├── app.py              # Flask API server
│   # (AI agent removed - using YOLO-based crowd detection only)
│   ├── video_processor.py  # Video processing
│   └── data_manager.py     # Data storage/retrieval
├── frontend/
│   ├── index.html          # Main UI
│   ├── styles.css          # Styling
│   └── app.js              # Frontend logic
├── data/
│   └── locations_data.json # Stored location data
├── videos/                 # Your video files
├── person_detector.py      # YOLO detection
└── process_hackathon_videos.py  # Batch processing script
```

## 🐛 Troubleshooting

### Backend won't start
- Check if port 5000 is available
- Ensure all dependencies are installed
- Check Python version (3.8+)

### Frontend can't connect to backend
- Ensure backend is running on port 5000
- Check CORS settings in `backend/app.py`
- Verify API_BASE_URL in `frontend/app.js`

### Videos not processing
- Check video file paths
- Ensure videos are in correct format (mp4, avi, etc.)
- Check file permissions

## 🎨 Frontend Features

- ✅ Location query interface
- ✅ Real-time crowd analysis display
- ✅ AI recommendations with alternatives
- ✅ All locations overview
- ✅ Video processing interface
- ✅ Responsive design

## 📝 Notes

- Location data is stored in `data/locations_data.json`
- Videos are processed using YOLOv8 person detection
- AI agent analyzes trends from historical data
- Recommendations are based on crowd levels and distance

## 🚀 Next Steps

1. Process your 7 location videos
2. Test the API endpoints
3. Use the frontend to query locations
4. Get AI recommendations for your hackathon demo!

