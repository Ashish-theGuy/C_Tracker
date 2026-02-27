"""
Live Video Analyzer - Shows YOLO model analyzing video in real-time
"""
import cv2
import numpy as np
import sys
import os
import base64
import io
from PIL import Image

# Add parent directory to path to import person_detector
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from person_detector import PersonDetector

class LiveVideoAnalyzer:
    """Analyze video with live YOLO detection"""
    
    def __init__(self):
        self.detector = PersonDetector(model_path="yolov8n.pt", confidence_threshold=0.25)
    
    def analyze_frame(self, frame):
        """
        Analyze a single frame and return annotated frame with detections
        
        Args:
            frame: OpenCV frame (numpy array)
        
        Returns:
            annotated_frame, person_count, detections
        """
        # Run YOLOv8 inference
        results = self.detector.model(frame, conf=self.detector.confidence_threshold, classes=[self.detector.person_class_id])
        
        person_count = 0
        detections = []
        annotated_frame = frame.copy()
        
        # Process detections
        for result in results:
            boxes = result.boxes
            for box in boxes:
                if int(box.cls) == self.detector.person_class_id:
                    person_count += 1
                    confidence = float(box.conf)
                    bbox = box.xyxy[0].cpu().numpy()
                    
                    # Draw bounding box
                    x1, y1, x2, y2 = map(int, bbox)
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Draw confidence score
                    label = f"Person {person_count} ({confidence:.2f})"
                    (text_width, text_height), baseline = cv2.getTextSize(
                        label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
                    )
                    cv2.rectangle(annotated_frame, (x1, y1 - text_height - 10), 
                                (x1 + text_width, y1), (0, 255, 0), -1)
                    cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    
                    detections.append({
                        "bbox": bbox.tolist(),
                        "confidence": confidence
                    })
        
        # Add overlay text
        overlay_text = f"People: {person_count}"
        cv2.putText(annotated_frame, overlay_text, (10, 30), 
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return annotated_frame, person_count, detections
    
    def frame_to_base64(self, frame):
        """Convert OpenCV frame to base64 string for web display"""
        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        frame_bytes = buffer.tobytes()
        
        # Convert to base64
        frame_base64 = base64.b64encode(frame_bytes).decode('utf-8')
        return f"data:image/jpeg;base64,{frame_base64}"
    
    def get_sample_frames(self, video_path, num_frames=10):
        """
        Get sample frames from video for live analysis preview
        
        Args:
            video_path: Path to video file
            num_frames: Number of frames to sample
        
        Returns:
            List of (frame_base64, person_count) tuples
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return []
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_interval = max(1, total_frames // num_frames)
        
        frames_data = []
        frame_count = 0
        
        while cap.isOpened() and len(frames_data) < num_frames:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_interval == 0:
                annotated_frame, person_count, _ = self.analyze_frame(frame)
                frame_base64 = self.frame_to_base64(annotated_frame)
                frames_data.append({
                    "frame": frame_base64,
                    "person_count": person_count,
                    "frame_number": frame_count
                })
            
            frame_count += 1
        
        cap.release()
        return frames_data

