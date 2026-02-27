"""
Example usage of the Person Detection System
"""

from person_detector import PersonDetector
import cv2

# Example 1: Detect people in an image
print("=" * 50)
print("Example 1: Image Detection")
print("=" * 50)

detector = PersonDetector(model_path="yolov8n.pt", confidence_threshold=0.25)

# Replace with your image path
image_path = "Image.jpeg"  # Using uploaded image

try:
    person_count, annotated_image, detection_data = detector.detect_people(image_path)
    
    print(f"Image: {image_path}")
    print(f"People detected: {person_count}")
    print(f"Crowd level: {detection_data['crowd_level']}")
    print(f"Detection confidence scores: {[d['confidence'] for d in detection_data['detections']]}")
    
    # Save the annotated image
    output_path = "output_detection.jpg"
    cv2.imwrite(output_path, annotated_image)
    print(f"Annotated image saved to: {output_path}")
    
except FileNotFoundError:
    print(f"Image file not found: {image_path}")
    print("Please provide a valid image path")

# Example 2: Detect people in a video
print("\n" + "=" * 50)
print("Example 2: Video Detection")
print("=" * 50)

video_path = "sample_video.mp4"  # Change this to your video path

try:
    stats = detector.detect_people_video(video_path, output_path="output_video.mp4")
    
    print(f"Video: {video_path}")
    print(f"Total frames processed: {stats['total_frames']}")
    print(f"Average people per frame: {stats['average_people']:.2f}")
    print(f"Maximum people in a frame: {stats['max_people']}")
    print(f"Minimum people in a frame: {stats['min_people']}")
    print(f"Overall crowd level: {stats['overall_crowd_level']}")
    
except FileNotFoundError:
    print(f"Video file not found: {video_path}")
    print("Please provide a valid video path")

# Example 3: Prepare data for API
print("\n" + "=" * 50)
print("Example 3: API Integration")
print("=" * 50)

try:
    api_payload = detector.process_and_send_to_api(
        image_path=image_path,
        api_url="https://your-backend-api.com/crowd-data"
    )
    
    print("API Payload structure:")
    print(f"  Person count: {api_payload['person_count']}")
    print(f"  Crowd level: {api_payload['crowd_level']}")
    print(f"  Location: {api_payload['location']}")
    print("\nFull payload (for API):")
    import json
    print(json.dumps(api_payload, indent=2))
    
except Exception as e:
    print(f"Error: {e}")

# Example 4: Custom crowd level thresholds
print("\n" + "=" * 50)
print("Example 4: Custom Crowd Classification")
print("=" * 50)

# Test different person counts
test_counts = [0, 3, 7, 12, 20, 30]

for count in test_counts:
    level = detector._classify_crowd_level(count)
    print(f"  {count} people → {level}")

print("\nNote: You can modify the _classify_crowd_level() method")
print("in person_detector.py to customize thresholds for your use case.")

