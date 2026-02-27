# Installation Guide for Windows

## Step 1: Install Python (if not already installed)

1. Download Python from: https://www.python.org/downloads/
2. **Important**: Check "Add Python to PATH" during installation
3. Install Python 3.8 or higher

## Step 2: Install Dependencies

### Option A: Using the batch script (Easiest)
```batch
install_and_test.bat
```

### Option B: Manual installation

Try these commands in order:

```batch
python -m pip install -r requirements.txt
```

OR

```batch
py -m pip install -r requirements.txt
```

OR

```batch
python3 -m pip install -r requirements.txt
```

### Option C: If pip is not recognized

1. Update pip first:
```batch
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

2. Then install requirements:
```batch
python -m pip install -r requirements.txt
```

## Step 3: Test Installation

Run the test script:
```batch
python test_setup.py
```

OR

```batch
py test_setup.py
```

This will:
- Check if all packages are installed
- Test if YOLOv8 model can be loaded (will download ~6MB on first run)

## Step 4: Test with an Image

1. Place an image file (jpg, png) in the `yolo_person_detection` folder
2. Run:

```batch
python person_detector.py --input your_image.jpg --output result.jpg --json
```

OR

```batch
py person_detector.py --input your_image.jpg --output result.jpg --json
```

## Troubleshooting

### "Python was not found"
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH"

### "pip is not recognized"
- Use `python -m pip` instead of just `pip`
- Or use `py -m pip` (Windows Python Launcher)

### "No module named 'ultralytics'"
- Run: `python -m pip install ultralytics`
- Make sure you're in the correct directory

### Model download issues
- The model (yolov8n.pt, ~6MB) downloads automatically on first run
- Make sure you have internet connection
- Check if firewall/antivirus is blocking the download

## Quick Test (After Installation)

```python
from person_detector import PersonDetector

detector = PersonDetector()
count, image, data = detector.detect_people("your_image.jpg")
print(f"Found {count} people - Level: {data['crowd_level']}")
```

