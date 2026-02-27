# 🎯 How to Test Image Crowd Recognition - Step by Step

## ✅ Step-by-Step Instructions

### STEP 1: Check if Python is Installed

Open Command Prompt or PowerShell and type:
```batch
python --version
```

**If you see a version number (like Python 3.11.0):**
- ✅ Python is installed! Go to STEP 2

**If you see "Python was not found":**
- ❌ You need to install Python first:
  1. Go to: https://www.python.org/downloads/
  2. Download and install Python 3.8 or higher
  3. **IMPORTANT**: Check the box "Add Python to PATH" during installation
  4. Restart your computer or terminal after installation

---

### STEP 2: Navigate to Project Folder

Open Command Prompt or PowerShell and go to the project folder:
```batch
cd C:\Users\skittles\yolo_person_detection
```

---

### STEP 3: Install Required Packages

Run this command (try them in order until one works):

**Option 1:**
```batch
python -m pip install -r requirements.txt
```

**Option 2 (if Option 1 doesn't work):**
```batch
py -m pip install -r requirements.txt
```

**Option 3 (use the batch file):**
Double-click `install_and_test.bat` in Windows Explorer

**This will install:**
- ultralytics (YOLOv8)
- opencv-python
- numpy
- Pillow

**Note:** On first run, YOLOv8 will download a model file (~6MB) - this is normal!

---

### STEP 4: Test Installation

Run this to verify everything is installed:
```batch
python test_setup.py
```

**OR:**
```batch
py test_setup.py
```

You should see ✅ marks for all packages.

---

### STEP 5: Get a Test Image

1. Find any image file with people in it (jpg, png, etc.)
2. Copy it to the `yolo_person_detection` folder
3. Remember the filename (e.g., `my_photo.jpg`)

**Tip:** You can use any photo from your phone/computer, or download a test image from the internet.

---

### STEP 6: Run Person Detection

Replace `your_image.jpg` with your actual image filename:

```batch
python person_detector.py --input your_image.jpg --output result.jpg --json
```

**OR:**
```batch
py person_detector.py --input your_image.jpg --output result.jpg --json
```

**Example:**
```batch
python person_detector.py --input photo.jpg --output result.jpg --json
```

---

### STEP 7: Check the Results

After running, you should see:

1. **Console Output:**
   ```
   Loading YOLOv8 model: yolov8n.pt
   Processing image: your_image.jpg
   Saved annotated image to: result.jpg
   Person Count: 5
   Crowd Level: Medium
   ```

2. **New Files Created:**
   - `result.jpg` - Image with green boxes around detected people
   - `result.json` - Detection data (person count, crowd level, etc.)

3. **Open `result.jpg`** to see:
   - Green rectangles around each person
   - Labels showing person numbers
   - Total count and crowd level at the top

---

## 🎨 Understanding the Output

### Crowd Levels:
- **Empty**: 0 people
- **Low**: 1-4 people  
- **Medium**: 5-14 people
- **High**: 15+ people

### JSON File Contains:
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

---

## 🐛 Troubleshooting

### Problem: "python is not recognized"
**Solution:** Install Python and make sure "Add Python to PATH" is checked

### Problem: "pip is not recognized"  
**Solution:** Use `python -m pip` instead of just `pip`

### Problem: "No module named 'ultralytics'"
**Solution:** Run `python -m pip install ultralytics`

### Problem: Model download fails
**Solution:** Check internet connection, the model downloads automatically on first run

### Problem: No people detected in image
**Solution:** 
- Try a different image with clearer people
- Lower confidence threshold: `--confidence 0.15`
- Make sure the image has people visible

---

## 🚀 Quick Test (Alternative Method)

Create a file called `quick_test.py`:

```python
from person_detector import PersonDetector
import cv2

# Initialize detector
detector = PersonDetector()

# Detect people (replace with your image filename)
count, image, data = detector.detect_people("your_image.jpg")

# Print results
print(f"People detected: {count}")
print(f"Crowd level: {data['crowd_level']}")

# Save result
cv2.imwrite("output.jpg", image)
print("Saved to output.jpg")
```

Then run:
```batch
python quick_test.py
```

---

## 📝 Summary

1. ✅ Install Python (if needed)
2. ✅ Navigate to project folder
3. ✅ Install packages: `python -m pip install -r requirements.txt`
4. ✅ Test setup: `python test_setup.py`
5. ✅ Run detection: `python person_detector.py --input image.jpg --output result.jpg --json`
6. ✅ Check `result.jpg` and `result.json` files

**That's it!** If you see green boxes around people and get a count, it's working! 🎉

