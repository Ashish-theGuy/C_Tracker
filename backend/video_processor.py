"""
Video Processor for analyzing videos from different locations
"""
import sys
import os
from datetime import datetime

# Add parent directory to path to import person_detector
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from person_detector import PersonDetector

class VideoProcessor:
    """Process videos from different locations"""
    
    def __init__(self):
        self.detector = PersonDetector(model_path="yolov8n.pt", confidence_threshold=0.25)
    
    def process_location_video(self, video_path: str, location_name: str, location_coords: dict = None) -> dict:
        """
        Process a video from a specific location
        
        Args:
            video_path: Path to video file
            location_name: Name of the location
            location_coords: Coordinates {lat, lng}
        
        Returns:
            Dictionary with crowd statistics
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        print(f"📹 Processing video for location: {location_name}")
        
        # Process video using PersonDetector
        stats = self.detector.detect_people_video(video_path, output_path=None)
        
        # Add location metadata
        result = {
            "location_name": location_name,
            "coordinates": location_coords or {},
            "current_people": int(stats.get('average_people', 0)),
            "average_people": float(stats.get('average_people', 0)),
            "max_people": int(stats.get('max_people', 0)),
            "min_people": int(stats.get('min_people', 0)),
            "total_frames": int(stats.get('total_frames', 0)),
            "crowd_level": stats.get('overall_crowd_level', 'Unknown'),
            "processed_at": datetime.now().isoformat(),
            "video_path": video_path,
            "history": [{
                "timestamp": datetime.now().isoformat(),
                "people_count": int(stats.get('average_people', 0)),
                "crowd_level": stats.get('overall_crowd_level', 'Unknown')
            }]
        }
        
        print(f"✅ Processed {location_name}: {result['current_people']} people ({result['crowd_level']} crowd)")
        
        return result

