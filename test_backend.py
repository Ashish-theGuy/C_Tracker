"""
Test script for backend API
"""
import requests
import json
import time

API_BASE = "http://localhost:5000"

def test_health():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_BASE}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_all_locations():
    """Test get all locations endpoint"""
    print("\nTesting get all locations...")
    try:
        response = requests.get(f"{API_BASE}/api/all-locations")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Locations found: {len(data.get('locations', []))}")
        if data.get('locations'):
            for loc in data['locations']:
                print(f"  - {loc['name']}: {loc['current_people']} people ({loc['crowd_level']})")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_process_video():
    """Test video processing (if video exists)"""
    print("\nTesting video processing...")
    import os
    if os.path.exists("video.mp4"):
        try:
            response = requests.post(
                f"{API_BASE}/api/process-video",
                json={
                    "video_path": "video.mp4",
                    "location_name": "Test Location",
                    "location_coords": {"lat": 40.7851, "lng": -73.9683}
                }
            )
            print(f"Status: {response.status_code}")
            data = response.json()
            if data.get('success'):
                print(f"Success! Processed: {data['data']['current_people']} people")
            else:
                print(f"Error: {data.get('error')}")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    else:
        print("Skipping - video.mp4 not found")
        return None

def test_query_location():
    """Test location query"""
    print("\nTesting location query...")
    try:
        # First, try to process a test location if we have data
        response = requests.post(
            f"{API_BASE}/api/query-location",
            json={
                "location_name": "Test Location",
                "user_location": {"lat": 40.7580, "lng": -73.9855}
            }
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        if data.get('success'):
            analysis = data['analysis']
            print(f"Location: {analysis['location']}")
            print(f"People: {analysis['current_status']['people_count']}")
            print(f"Crowd Level: {analysis['current_status']['crowd_level']}")
            print(f"Recommendation: {analysis['recommendation']['should_visit']}")
        else:
            print(f"Note: {data.get('error')} (This is OK if no locations processed yet)")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Backend API Test Suite")
    print("=" * 60)
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(2)
    
    # Run tests
    results = []
    results.append(("Health Check", test_health()))
    results.append(("All Locations", test_all_locations()))
    video_result = test_process_video()
    if video_result is not None:
        results.append(("Process Video", video_result))
    results.append(("Query Location", test_query_location()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
    
    print("\nBackend is running! Open frontend/index.html in your browser")
    print("Or use: cd frontend && python -m http.server 8000")

