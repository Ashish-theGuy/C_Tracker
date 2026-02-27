"""Quick API test script"""
import requests
import json

API = "http://localhost:5000/api"

print("=" * 60)
print("Testing Backend API")
print("=" * 60)

# Test 1: All Locations
print("\n1. Getting all locations...")
r = requests.get(f"{API}/all-locations")
data = r.json()
print(f"   Found {len(data['locations'])} locations")
for loc in data['locations']:
    print(f"   - {loc['name']}: {loc['current_people']} people ({loc['crowd_level']})")

# Test 2: Query Location
if data['locations']:
    location_name = data['locations'][0]['name']
    print(f"\n2. Querying location: {location_name}...")
    r = requests.post(f"{API}/query-location", json={
        "location_name": location_name,
        "user_location": {"lat": 40.7580, "lng": -73.9855}
    })
    result = r.json()
    if result.get('success'):
        analysis = result['analysis']
        print(f"   People: {analysis['current_status']['people_count']}")
        print(f"   Crowd Level: {analysis['current_status']['crowd_level']}")
        print(f"   Trend: {analysis['current_status']['trend']}")
        print(f"   Should Visit: {analysis['recommendation']['should_visit']}")
        print(f"   Reason: {analysis['recommendation']['reason']}")

# Test 3: Recommendations
if data['locations']:
    print(f"\n3. Getting recommendations for: {location_name}...")
    r = requests.post(f"{API}/get-recommendations", json={
        "target_location": location_name,
        "user_location": {"lat": 40.7580, "lng": -73.9855}
    })
    rec = r.json()
    if rec.get('success'):
        summary = rec['recommendations']['summary']
        # Remove emojis for Windows console
        summary = summary.encode('ascii', 'ignore').decode('ascii')
        print(f"   Summary: {summary}")
        print(f"   Alternatives: {len(rec['recommendations'].get('alternatives', []))}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
print("\nBackend is running on: http://localhost:5000")
print("To start frontend: cd frontend && python -m http.server 8000")
print("Or double-click: start_frontend.bat")

