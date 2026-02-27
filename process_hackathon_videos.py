"""
Script to process videos from 7 different locations for hackathon
"""
import os
import json
from backend.video_processor import VideoProcessor
from backend.data_manager import DataManager

# Define 7 locations with sample coordinates (update with real coordinates)
LOCATIONS = [
    {
        "name": "Central Park",
        "video_path": "videos/central_park.mp4",  # Update with actual video paths
        "coordinates": {"lat": 40.7851, "lng": -73.9683}
    },
    {
        "name": "Times Square",
        "video_path": "videos/times_square.mp4",
        "coordinates": {"lat": 40.7580, "lng": -73.9855}
    },
    {
        "name": "Brooklyn Bridge",
        "video_path": "videos/brooklyn_bridge.mp4",
        "coordinates": {"lat": 40.7061, "lng": -73.9969}
    },
    {
        "name": "Empire State Building",
        "video_path": "videos/empire_state.mp4",
        "coordinates": {"lat": 40.7484, "lng": -73.9857}
    },
    {
        "name": "Statue of Liberty",
        "video_path": "videos/statue_liberty.mp4",
        "coordinates": {"lat": 40.6892, "lng": -74.0445}
    },
    {
        "name": "High Line Park",
        "video_path": "videos/high_line.mp4",
        "coordinates": {"lat": 40.7480, "lng": -74.0048}
    },
    {
        "name": "Washington Square",
        "video_path": "videos/washington_square.mp4",
        "coordinates": {"lat": 40.7308, "lng": -73.9973}
    }
]

def process_all_videos():
    """Process all videos from the 7 locations"""
    processor = VideoProcessor()
    data_manager = DataManager()
    
    print("=" * 60)
    print("🎬 Processing Videos for 7 Locations")
    print("=" * 60)
    
    results = []
    
    for i, location in enumerate(LOCATIONS, 1):
        print(f"\n[{i}/7] Processing: {location['name']}")
        
        video_path = location['video_path']
        
        # Check if video exists
        if not os.path.exists(video_path):
            print(f"⚠️  Video not found: {video_path}")
            print(f"   Skipping {location['name']}...")
            continue
        
        try:
            # Process video
            stats = processor.process_location_video(
                video_path,
                location['name'],
                location['coordinates']
            )
            
            # Save data
            data_manager.save_location_data(
                location['name'],
                stats,
                location['coordinates']
            )
            
            results.append({
                "location": location['name'],
                "status": "success",
                "people_count": stats['current_people'],
                "crowd_level": stats['crowd_level']
            })
            
        except Exception as e:
            print(f"❌ Error processing {location['name']}: {e}")
            results.append({
                "location": location['name'],
                "status": "error",
                "error": str(e)
            })
    
    print("\n" + "=" * 60)
    print("📊 Processing Summary")
    print("=" * 60)
    
    for result in results:
        if result['status'] == 'success':
            print(f"✅ {result['location']}: {result['people_count']} people ({result['crowd_level']})")
        else:
            print(f"❌ {result['location']}: {result.get('error', 'Unknown error')}")
    
    print("\n✅ All videos processed!")
    print(f"📁 Data saved to: data/locations_data.json")
    
    return results

if __name__ == "__main__":
    # Create videos directory if it doesn't exist
    os.makedirs('videos', exist_ok=True)
    
    print("\n💡 Instructions:")
    print("1. Place your 7 video files in the 'videos' folder")
    print("2. Update the video_path in LOCATIONS list above")
    print("3. Update coordinates with real location coordinates")
    print("4. Run this script to process all videos\n")
    
    # Uncomment to run processing
    # process_all_videos()
    
    print("\n⚠️  To process videos, uncomment the last line in this script")
    print("   and update the LOCATIONS list with your video paths.")

