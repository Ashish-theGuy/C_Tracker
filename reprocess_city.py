"""
Reprocess a specific city video
"""
import requests
import json
import os

API_BASE = "http://localhost:5000/api"

def reprocess_city(city_name, video_path):
    """Reprocess a specific city video"""
    print(f"Reprocessing {city_name}...")
    print(f"Video: {video_path}")
    
    if not os.path.exists(video_path):
        print(f"ERROR: Video file not found: {video_path}")
        return
    
    try:
        # Process the video
        response = requests.post(f"{API_BASE}/process-video", json={
            "video_path": video_path,
            "location_name": city_name,
            "location_coords": {}  # Will be filled from city config
        })
        
        data = response.json()
        
        if data.get('success'):
            print(f"\n[SUCCESS] {city_name} reprocessed!")
            print(f"  - People detected: {data['data']['current_people']}")
            print(f"  - Crowd level: {data['data']['crowd_level']}")
            print(f"  - Average: {data['data']['average_people']:.1f}")
            print(f"  - Max: {data['data']['max_people']}")
            print(f"  - Min: {data['data']['min_people']}")
        else:
            print(f"[ERROR] {data.get('error')}")
            
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    # Reprocess Kochi (city3)
    print("=" * 60)
    print("Reprocessing City3 (Kochi)")
    print("=" * 60)
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:5000/")
        print("Backend is running!")
    except:
        print("ERROR: Backend is not running!")
        print("Please start the backend first: python run_backend.py")
        exit(1)
    
    # Get the correct path - video is in root directory
    import os
    root_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(root_dir, "city3.mp4")
    
    # For backend, use relative path from backend directory
    backend_video_path = "../city3.mp4"
    
    # Check if file exists in root
    if os.path.exists(video_path):
        print(f"Found video at: {video_path}")
        # Reprocess Kochi using backend path
        reprocess_city("Kochi", backend_video_path)
    else:
        print(f"ERROR: Video not found at: {video_path}")
        print("Please ensure city3.mp4 is in the project root directory.")
    
    print("\n" + "=" * 60)
    print("Done! Kochi data has been updated.")
    print("You can now ask about Kochi to see the new analysis.")
    print("=" * 60)

