"""
Reprocess Kochi (city3) video
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, os.path.dirname(__file__))

from backend.video_processor import VideoProcessor
from backend.data_manager import DataManager
from backend.kerala_cities import KERALA_CITIES

def reprocess_kochi():
    """Reprocess Kochi video"""
    print("=" * 60)
    print("Reprocessing Kochi (city3)")
    print("=" * 60)
    
    city_name = "Kochi"
    city_info = KERALA_CITIES[city_name]
    video_path = city_info['video_file']
    
    # Check if video exists (try both relative paths)
    if not os.path.exists(video_path):
        # Try from root directory
        alt_path = "city3.mp4"
        if os.path.exists(alt_path):
            video_path = alt_path
            print(f"Found video at: {alt_path}")
        else:
            print(f"ERROR: Video not found!")
            print(f"  Tried: {city_info['video_file']}")
            print(f"  Tried: {alt_path}")
            return
    else:
        print(f"Found video at: {video_path}")
    
    print(f"\nProcessing video...")
    
    try:
        # Initialize components
        processor = VideoProcessor()
        data_manager = DataManager()
        
        # Process video
        stats = processor.process_location_video(
            video_path,
            city_name,
            city_info['coordinates']
        )
        
        # Store data
        data_manager.save_location_data(city_name, stats, city_info['coordinates'])
        
        print(f"\n[SUCCESS] Kochi reprocessed!")
        print(f"  - People detected: {stats['current_people']}")
        print(f"  - Crowd level: {stats['crowd_level']}")
        print(f"  - Average: {stats['average_people']:.1f}")
        print(f"  - Max: {stats['max_people']}")
        print(f"  - Min: {stats['min_people']}")
        print(f"  - Total frames: {stats['total_frames']}")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reprocess_kochi()
    print("\n" + "=" * 60)
    print("Done! Kochi data has been updated.")
    print("Ask about Kochi in the frontend to see the new analysis.")
    print("=" * 60)

