"""
Process videos for 7 Kerala cities
Place your videos in the videos/ folder with these names:
- munnar.mp4
- alleppey.mp4
- kochi.mp4
- wayanad.mp4
- thekkady.mp4
- kovalam.mp4
- varkala.mp4
"""
import requests
import json
import os

API_BASE = "http://localhost:5000/api"

def process_all_kerala_videos():
    """Process all Kerala city videos via API"""
    print("=" * 60)
    print("Processing Kerala City Videos")
    print("=" * 60)
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:5000/")
        print("Backend is running!")
    except:
        print("ERROR: Backend is not running!")
        print("Please start the backend first: python run_backend.py")
        return
    
    # Process videos
    print("\nProcessing videos...")
    try:
        response = requests.post(f"{API_BASE}/process-kerala-videos")
        data = response.json()
        
        if data.get('success'):
            print(f"\nProcessed: {data['processed']}/{data['total']} cities\n")
            
            for result in data['results']:
                city = result['city']
                status = result['status']
                
                if status == 'processed':
                    print(f"✓ {city}: {result['people_count']} people ({result['crowd_level']})")
                elif status == 'skipped':
                    print(f"⚠ {city}: {result['reason']}")
                elif status == 'error':
                    print(f"✗ {city}: Error - {result['error']}")
        else:
            print(f"Error: {data.get('error')}")
            
    except Exception as e:
        print(f"Error processing videos: {e}")

if __name__ == "__main__":
    print("\nKerala Cities Video Processor")
    print("=" * 60)
    print("\nExpected video files in videos/ folder:")
    print("  - munnar.mp4")
    print("  - alleppey.mp4")
    print("  - kochi.mp4")
    print("  - wayanad.mp4")
    print("  - thekkady.mp4")
    print("  - kovalam.mp4")
    print("  - varkala.mp4")
    print("\n" + "=" * 60)
    
    # Create videos directory if it doesn't exist
    os.makedirs('videos', exist_ok=True)
    
    process_all_kerala_videos()
    
    print("\n" + "=" * 60)
    print("Done! You can now ask questions about these cities.")
    print("=" * 60)

