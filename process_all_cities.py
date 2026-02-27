"""
Process all 7 city videos and analyze crowd density
"""
import requests
import json
import os

API_BASE = "http://localhost:5000/api"

def process_all_cities():
    """Process all Kerala city videos"""
    print("=" * 60)
    print("Processing All Kerala City Videos")
    print("=" * 60)
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:5000/")
        print("Backend is running!")
    except:
        print("ERROR: Backend is not running!")
        print("Please start the backend first: python run_backend.py")
        return
    
    # Check if videos exist
    videos = {
        "Munnar": "City1.mp4",
        "Alleppey": "city2.mp4",
        "Kochi": "city3.mp4",
        "Wayanad": "city4.mp4",
        "Thekkady": "city5.mp4",
        "Kovalam": "city6.mp4",
        "Varkala": "city7.mp4"
    }
    
    print("\nChecking video files...")
    missing = []
    for city, video in videos.items():
        if os.path.exists(video):
            print(f"[OK] {city}: {video}")
        else:
            print(f"[MISSING] {city}: {video} - NOT FOUND")
            missing.append(city)
    
    if missing:
        print(f"\n[WARNING] {len(missing)} videos not found!")
        print("Please ensure all videos are in the project root directory.")
    
    # Process videos
    print("\n" + "=" * 60)
    print("Processing videos with YOLO person detection...")
    print("=" * 60)
    
    try:
        response = requests.post(f"{API_BASE}/process-kerala-videos")
        data = response.json()
        
        if data.get('success'):
            print(f"\n[SUCCESS] Processed: {data['processed']}/{data['total']} cities\n")
            
            for result in data['results']:
                city = result['city']
                status = result['status']
                
                if status == 'processed':
                    print(f"[OK] {city}:")
                    print(f"  - People detected: {result['people_count']}")
                    print(f"  - Crowd level: {result['crowd_level']}")
                    print()
                elif status == 'skipped':
                    print(f"[SKIP] {city}: {result['reason']}")
                elif status == 'error':
                    print(f"[ERROR] {city}: Error - {result['error']}")
        else:
            print(f"[ERROR] Error: {data.get('error')}")
            
    except Exception as e:
        print(f"[ERROR] Error processing videos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    process_all_cities()
    
    print("=" * 60)
    print("[SUCCESS] Processing complete!")
    print("=" * 60)
    print("\nYou can now ask questions about the cities:")
    print("  - 'Should I visit Munnar?'")
    print("  - 'Is Kochi crowded?'")
    print("  - 'What's the crowd like in Alleppey?'")
    print("\nThe system will show live YOLO detection analysis!")

