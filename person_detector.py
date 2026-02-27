"""
YOLOv8 Person Detection and Counting System
Detects people in images/videos and determines crowd levels
"""

import cv2
import numpy as np
from ultralytics import YOLO
from typing import Tuple, Optional, Dict
from pathlib import Path
import json


class PersonDetector:
    """YOLOv8-based person detection and counting system"""
    
    def __init__(self, model_path: str = "yolov8n.pt", confidence_threshold: float = 0.25):
        """
        Initialize the person detector
        
        Args:
            model_path: Path to YOLOv8 model file (or model name for auto-download)
            confidence_threshold: Minimum confidence for detections (0.0-1.0)
        """
        print(f"Loading YOLOv8 model: {model_path}")
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.person_class_id = 0  # COCO dataset class ID for 'person'
        
    def detect_people(self, image_path: str) -> Tuple[int, np.ndarray, Dict]:
        """
        Detect people in an image
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Tuple of (person_count, annotated_image, detection_data)
        """
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        # Run YOLOv8 inference
        results = self.model(image, conf=self.confidence_threshold, classes=[self.person_class_id])
        
        # Extract person detections
        person_count = 0
        detection_data = {
            "person_count": 0,
            "detections": [],
            "crowd_level": None
        }
        
        # Process results
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Check if it's a person (class_id == 0)
                if int(box.cls) == self.person_class_id:
                    person_count += 1
                    confidence = float(box.conf)
                    bbox = box.xyxy[0].cpu().numpy()  # Get bounding box coordinates
                    
                    detection_data["detections"].append({
                        "bbox": bbox.tolist(),
                        "confidence": confidence
                    })
                    
                    # Draw bounding box
                    x1, y1, x2, y2 = map(int, bbox)
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(image, f"Person {person_count} ({confidence:.2f})", 
                              (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        detection_data["person_count"] = person_count
        detection_data["crowd_level"] = self._classify_crowd_level(person_count)
        
        # Add count text to image
        cv2.putText(image, f"Total People: {person_count} | Level: {detection_data['crowd_level']}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return person_count, image, detection_data
    
    def detect_people_video(self, video_path: str, output_path: Optional[str] = None) -> Dict:
        """
        Detect people in a video file
        
        Args:
            video_path: Path to the input video file
            output_path: Optional path to save annotated video
            
        Returns:
            Dictionary with detection statistics
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Video writer for output
        out = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        all_detections = []
        person_counts = []
        
        print(f"Processing video: {video_path}")
        print(f"Total frames: {total_frames}, FPS: {fps}")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Run YOLOv8 inference on frame
            results = self.model(frame, conf=self.confidence_threshold, classes=[self.person_class_id])
            
            person_count = 0
            frame_detections = []
            
            # Process detections
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    if int(box.cls) == self.person_class_id:
                        person_count += 1
                        confidence = float(box.conf)
                        bbox = box.xyxy[0].cpu().numpy()
                        
                        x1, y1, x2, y2 = map(int, bbox)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, f"{confidence:.2f}", 
                                  (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
                        frame_detections.append({
                            "bbox": bbox.tolist(),
                            "confidence": confidence
                        })
            
            person_counts.append(person_count)
            all_detections.append({
                "frame": frame_count,
                "person_count": person_count,
                "detections": frame_detections,
                "crowd_level": self._classify_crowd_level(person_count)
            })
            
            # Add overlay text
            crowd_level = self._classify_crowd_level(person_count)
            cv2.putText(frame, f"People: {person_count} | Level: {crowd_level} | Frame: {frame_count}/{total_frames}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            if out:
                out.write(frame)
            
            frame_count += 1
            if frame_count % 30 == 0:
                print(f"Processed {frame_count}/{total_frames} frames...")
        
        cap.release()
        if out:
            out.release()
        
        # Calculate statistics
        avg_people = np.mean(person_counts) if person_counts else 0
        max_people = max(person_counts) if person_counts else 0
        min_people = min(person_counts) if person_counts else 0
        
        stats = {
            "total_frames": frame_count,
            "average_people": float(avg_people),
            "max_people": int(max_people),
            "min_people": int(min_people),
            "frame_by_frame": all_detections,
            "overall_crowd_level": self._classify_crowd_level(int(avg_people))
        }
        
        return stats
    
    def _classify_crowd_level(self, person_count: int) -> str:
        """
        Classify crowd level based on person count
        
        Args:
            person_count: Number of people detected
            
        Returns:
            Crowd level: "Low", "Medium", or "High"
        """
        if person_count == 0:
            return "Empty"
        elif person_count < 5:
            return "Low"
        elif person_count < 15:
            return "Medium"
        else:
            return "High"
    
    def process_and_send_to_api(self, image_path: str, api_url: str) -> Dict:
        """
        Process image and send results to backend API
        
        Args:
            image_path: Path to image file
            api_url: Backend API endpoint URL
            
        Returns:
            API response data
        """
        person_count, annotated_image, detection_data = self.detect_people(image_path)
        
        # Prepare payload for API
        payload = {
            "location": {
                "latitude": 0.0,  # Replace with actual coordinates
                "longitude": 0.0
            },
            "person_count": person_count,
            "crowd_level": detection_data["crowd_level"],
            "timestamp": None,  # Add timestamp if needed
            "image_path": image_path
        }
        
        # Send to API (uncomment when API is ready)
        # import requests
        # response = requests.post(api_url, json=payload)
        # return response.json()
        
        return payload


def main():
    """Example usage of PersonDetector"""
    import argparse
    
    parser = argparse.ArgumentParser(description="YOLOv8 Person Detection")
    parser.add_argument("--input", "-i", required=True, help="Input image or video path")
    parser.add_argument("--output", "-o", help="Output path for annotated image/video")
    parser.add_argument("--model", "-m", default="yolov8n.pt", help="YOLOv8 model path")
    parser.add_argument("--confidence", "-c", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--json", action="store_true", help="Save detection results as JSON")
    
    args = parser.parse_args()
    
    # Initialize detector
    detector = PersonDetector(model_path=args.model, confidence_threshold=args.confidence)
    
    input_path = Path(args.input)
    
    # Check if input is image or video
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
    
    if input_path.suffix.lower() in image_extensions:
        # Process image
        print(f"Processing image: {args.input}")
        person_count, annotated_image, detection_data = detector.detect_people(args.input)
        
        # Save annotated image
        output_path = args.output or f"output_{input_path.stem}.jpg"
        cv2.imwrite(output_path, annotated_image)
        print(f"Saved annotated image to: {output_path}")
        print(f"Person Count: {person_count}")
        print(f"Crowd Level: {detection_data['crowd_level']}")
        
        # Save JSON if requested
        if args.json:
            json_path = output_path.replace('.jpg', '.json').replace('.png', '.json')
            with open(json_path, 'w') as f:
                json.dump(detection_data, f, indent=2)
            print(f"Saved detection data to: {json_path}")
    
    elif input_path.suffix.lower() in video_extensions:
        # Process video
        print(f"Processing video: {args.input}")
        stats = detector.detect_people_video(args.input, args.output)
        
        print(f"\nVideo Processing Complete!")
        print(f"Average People: {stats['average_people']:.2f}")
        print(f"Max People: {stats['max_people']}")
        print(f"Min People: {stats['min_people']}")
        print(f"Overall Crowd Level: {stats['overall_crowd_level']}")
        
        # Save JSON if requested
        if args.json:
            json_path = args.output.replace('.mp4', '.json') if args.output else f"output_{input_path.stem}.json"
            with open(json_path, 'w') as f:
                json.dump(stats, f, indent=2)
            print(f"Saved detection data to: {json_path}")
    
    else:
        print(f"Unsupported file format: {input_path.suffix}")
        print(f"Supported image formats: {image_extensions}")
        print(f"Supported video formats: {video_extensions}")


if __name__ == "__main__":
    main()

