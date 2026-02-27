# How to Test Image Crowd Recognition

## Quick Steps to Test

### Step 1: Install Python (if needed)
If you don't have Python installed:
1. Go to https://www.python.org/downloads/
2. Download Python 3.8 or higher
3. **IMPORTANT**: Check "Add Python to PATH" when installing

### Step 2: Install Packages

Open Command Prompt or PowerShell in the `yolo_person_detection` folder and run:

**Try this first:**
```batch
python -m pip install -r requirements.txt
```

**If that doesn't work, try:**
```batch
py -m pip install -r requirements.txt
```

**Or use the batch file:**
```batch
install_and_test.bat
```

### Step 3: Get a Test Image
- Find any image with people in it (jpg or png format)
- Place it in the `yolo_person_detection` folder
- Note the filename (e.g., `test_image.jpg`)

### Step 4: Run Detection

```batch
python person_detector.py --input test_image.jpg --output result.jpg --json
```

**If `python` doesn't work, try:**
```batch
py person_detector.py --input test_image.jpg --output result.jpg --json
```

### Step 5: Check Results

After running, you should see:
- ✅ A new file `result.jpg` with bounding boxes around detected people
- ✅ A file `result.json` (if you used --json) with detection data
- ✅ Console output showing: Person Count and Crowd Level

## What You Should See

**Console Output:**
```
Loading YOLOv8 model: yolov8n.pt
Processing image: test_image.jpg
Saved annotated image to: result.jpg
Person Count: 5
Crowd Level: Medium
```

**Result Image:**
- Green boxes around each detected person
- Labels showing "Person 1", "Person 2", etc.
- Total count and crowd level displayed

**JSON Output (result.json):**
```json
{
  "person_count": 5,
  "crowd_level": "Medium",
  "detections": [...]
}
```

## Test Script (Alternative Method)

You can also test using Python directly:

1. Create a file `test.py`:
```python
from person_detector import PersonDetector

detector = PersonDetector()
count, image, data = detector.detect_people("your_image.jpg")
print(f"Found {count} people")
print(f"Crowd Level: {data['crowd_level']}")

import cv2
cv2.imwrite("output.jpg", image)
print("Saved to output.jpg")
```

2. Run it:
```batch
python test.py
```

## Need Help?

- Check `INSTALL_GUIDE.md` for installation troubleshooting
- Run `python test_setup.py` to check if everything is installed correctly

