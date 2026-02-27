# YOLOv8 Person Detection System

A person detection and counting system using YOLOv8 for trip agent planning. Detects people in images/videos and classifies crowd levels (Low/Medium/High).

## Features

- ✅ Person detection using YOLOv8
- ✅ Person counting from images and videos
- ✅ Crowd level classification (Empty/Low/Medium/High)
- ✅ Annotated output with bounding boxes
- ✅ JSON export for API integration
- ✅ Video frame-by-frame analysis

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

The first time you run the script, YOLOv8 will automatically download the model (yolov8n.pt - nano version, ~6MB).

## Quick Start

### Detect people in an image:
```bash
python person_detector.py --input path/to/image.jpg --output output.jpg
```

### Detect people in a video:
```bash
python person_detector.py --input path/to/video.mp4 --output output.mp4
```

### Save detection results as JSON:
```bash
python person_detector.py --input image.jpg --output output.jpg --json
```

### Use a different YOLOv8 model:
```bash
# Available models: yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt
# Larger models = better accuracy but slower
python person_detector.py --input image.jpg --model yolov8m.pt
```

### Adjust confidence threshold:
```bash
python person_detector.py --input image.jpg --confidence 0.5
```

## Usage in Python Code

```python
from person_detector import PersonDetector

# Initialize detector
detector = PersonDetector(model_path="yolov8n.pt", confidence_threshold=0.25)

# Detect people in an image
person_count, annotated_image, detection_data = detector.detect_people("image.jpg")
print(f"People detected: {person_count}")
print(f"Crowd level: {detection_data['crowd_level']}")

# Save annotated image
import cv2
cv2.imwrite("output.jpg", annotated_image)

# Detect people in a video
stats = detector.detect_people_video("video.mp4", output_path="output.mp4")
print(f"Average people: {stats['average_people']}")
print(f"Overall crowd level: {stats['overall_crowd_level']}")
```

## Crowd Level Classification

- **Empty**: 0 people
- **Low**: 1-4 people
- **Medium**: 5-14 people
- **High**: 15+ people

You can customize the thresholds in the `_classify_crowd_level()` method.

## Integration with Backend API

The `process_and_send_to_api()` method prepares data for your backend API:

```python
detector = PersonDetector()
payload = detector.process_and_send_to_api("image.jpg", api_url="https://your-api.com/crowd-data")

# payload structure:
# {
#     "location": {"latitude": 0.0, "longitude": 0.0},
#     "person_count": 5,
#     "crowd_level": "Medium",
#     "timestamp": None,
#     "image_path": "image.jpg"
# }
```

## YOLOv8 Models

- **yolov8n.pt** (nano) - Fastest, smallest, lowest accuracy
- **yolov8s.pt** (small) - Balanced
- **yolov8m.pt** (medium) - Better accuracy
- **yolov8l.pt** (large) - High accuracy
- **yolov8x.pt** (xlarge) - Best accuracy, slowest

## Output Format

### Image Detection JSON:
```json
{
  "person_count": 5,
  "crowd_level": "Medium",
  "detections": [
    {
      "bbox": [x1, y1, x2, y2],
      "confidence": 0.95
    }
  ]
}
```

### Video Detection JSON:
```json
{
  "total_frames": 300,
  "average_people": 4.5,
  "max_people": 8,
  "min_people": 2,
  "overall_crowd_level": "Medium",
  "frame_by_frame": [...]
}
```

## Next Steps for Trip Agent Planner

1. **Add location data**: Integrate GPS/coordinates when processing images
2. **Backend API**: Implement API endpoint to receive crowd data
3. **Map UI Integration**: Use crowd levels to color markers on map
   - Green = Low
   - Yellow = Medium  
   - Red = High
4. **Real-time processing**: Add webcam/live stream support
5. **Batch processing**: Process multiple images/videos at once

## Requirements

- Python 3.8+
- ultralytics (YOLOv8)
- opencv-python
- numpy
- Pillow

## License

MIT License

# c-tracker
# C_Tracker
