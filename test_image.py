"""
Quick test script for Image.jpeg
"""
from person_detector import PersonDetector
import cv2

print("=" * 60)
print("Testing Person Detection on Image.jpeg")
print("=" * 60)

# Initialize detector
detector = PersonDetector(model_path="yolov8n.pt", confidence_threshold=0.25)

# Detect people in the uploaded image
image_path = "Image.jpeg"

try:
    print(f"\nProcessing: {image_path}")
    person_count, annotated_image, detection_data = detector.detect_people(image_path)
    
    print(f"\n✅ Results:")
    print(f"   People detected: {person_count}")
    print(f"   Crowd level: {detection_data['crowd_level']}")
    print(f"   Detection confidence scores: {[round(d['confidence'], 2) for d in detection_data['detections']]}")
    
    # Save the annotated image
    output_path = "result_Image.jpeg"
    cv2.imwrite(output_path, annotated_image)
    print(f"\n✅ Annotated image saved to: {output_path}")
    print(f"   Open this file to see the detection boxes!")
    
    # Save JSON if needed
    import json
    json_path = "result_Image.json"
    with open(json_path, 'w') as f:
        json.dump(detection_data, f, indent=2)
    print(f"✅ Detection data saved to: {json_path}")
    
    print("\n" + "=" * 60)
    print("Test completed successfully! 🎉")
    print("=" * 60)
    
except FileNotFoundError:
    print(f"❌ Error: Image file not found: {image_path}")
    print("   Make sure Image.jpeg is in the project folder")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()






