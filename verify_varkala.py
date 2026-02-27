"""
Verify Varkala detection and check stored data
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, os.path.dirname(__file__))

from backend.data_manager import DataManager
from person_detector import PersonDetector
import cv2

def verify_varkala():
    """Verify Varkala video detection and data"""
    print("=" * 60)
    print("Verifying Varkala Detection")
    print("=" * 60)
    
    # Check stored data
    data_manager = DataManager()
    varkala_data = data_manager.get_location_data("Varkala")
    
    if varkala_data:
        print("\n[STORED DATA]")
        print(f"  Current people: {varkala_data['current_people']}")
        print(f"  Average: {varkala_data['average_people']:.1f}")
        print(f"  Max: {varkala_data['max_people']}")
        print(f"  Min: {varkala_data['min_people']}")
        print(f"  Crowd level: {varkala_data['crowd_level']}")
        print(f"  Last updated: {varkala_data['last_updated']}")
    else:
        print("\n[ERROR] No data found for Varkala!")
        return
    
    # Test detection on a few frames
    print("\n[TESTING DETECTION]")
    video_path = "city7.mp4"
    
    if not os.path.exists(video_path):
        print(f"  ERROR: Video not found at {video_path}")
        return
    
    detector = PersonDetector()
    cap = cv2.VideoCapture(video_path)
    
    frame_count = 0
    detections = []
    
    print("  Analyzing sample frames...")
    while frame_count < 10:  # Check first 10 frames
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect people in this frame
        person_count, annotated_frame, detection_data = detector.detect_people(frame)
        detections.append(person_count)
        
        print(f"  Frame {frame_count + 1}: {person_count} people detected")
        
        # Save sample annotated frame
        if frame_count == 0:
            cv2.imwrite("varkala_sample_detection.jpg", annotated_frame)
            print(f"  Saved sample detection to: varkala_sample_detection.jpg")
        
        frame_count += 1
    
    cap.release()
    
    if detections:
        print(f"\n[SUMMARY]")
        print(f"  Average in sample: {sum(detections) / len(detections):.1f}")
        print(f"  Max in sample: {max(detections)}")
        print(f"  Min in sample: {min(detections)}")
    
    print("\n" + "=" * 60)
    print("Verification complete!")
    print("=" * 60)
    print("\nIf the detection count seems low, the video might have:")
    print("  - People too small/distant for YOLO to detect")
    print("  - People partially occluded")
    print("  - Low contrast or poor lighting")
    print("\nCheck 'varkala_sample_detection.jpg' to see what YOLO detected.")

if __name__ == "__main__":
    verify_varkala()

