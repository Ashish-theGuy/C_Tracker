"""
Simple test script to check if everything is installed correctly
"""

def test_imports():
    """Test if required packages are installed"""
    print("Testing imports...")
    
    try:
        import cv2
        print("✅ OpenCV installed")
    except ImportError:
        print("❌ OpenCV not installed")
        return False
    
    try:
        import numpy
        print("✅ NumPy installed")
    except ImportError:
        print("❌ NumPy not installed")
        return False
    
    try:
        from ultralytics import YOLO
        print("✅ Ultralytics (YOLOv8) installed")
    except ImportError:
        print("❌ Ultralytics not installed - Run: pip install ultralytics")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow installed")
    except ImportError:
        print("❌ Pillow not installed")
        return False
    
    return True

def test_yolo_model():
    """Test if YOLOv8 model can be loaded"""
    print("\nTesting YOLOv8 model loading...")
    try:
        from ultralytics import YOLO
        print("Loading YOLOv8 model (this may download ~6MB on first run)...")
        model = YOLO("yolov8n.pt")
        print("✅ YOLOv8 model loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("YOLOv8 Person Detection - Setup Test")
    print("=" * 50)
    
    if test_imports():
        test_yolo_model()
        print("\n" + "=" * 50)
        print("✅ Setup complete! You can now run person detection.")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ Please install missing packages first:")
        print("   pip install -r requirements.txt")
        print("   OR")
        print("   python -m pip install -r requirements.txt")
        print("=" * 50)

