# Quick Start Guide

## Step 1: Install Dependencies

```bash
cd yolo_person_detection
pip install -r requirements.txt
```

## Step 2: Test with an Image

```bash
# Replace 'your_image.jpg' with your actual image file
python person_detector.py --input your_image.jpg --output result.jpg --json
```

## Step 3: Test with a Video

```bash
# Replace 'your_video.mp4' with your actual video file
python person_detector.py --input your_video.mp4 --output result.mp4 --json
```

## Step 4: Use in Your Code

```python
from person_detector import PersonDetector

# Create detector
detector = PersonDetector()

# Detect people in image
count, image, data = detector.detect_people("image.jpg")
print(f"Found {count} people - Level: {data['crowd_level']}")
```

## Common Issues

1. **Model download**: YOLOv8 will auto-download the model on first run (~6MB)
2. **CUDA/GPU**: Works on CPU by default, GPU speeds it up if available
3. **Confidence**: Lower threshold (0.2-0.3) = more detections, higher threshold (0.5+) = fewer but more accurate

## Next Steps

- Customize crowd level thresholds in `person_detector.py`
- Integrate with your backend API
- Add location/GPS data
- Connect to map UI for colored markers

