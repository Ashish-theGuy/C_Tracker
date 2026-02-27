"""
Test the /api/cities endpoint
"""
import requests
import json

try:
    print("Testing /api/cities endpoint...")
    r = requests.get('http://localhost:5000/api/cities', timeout=5)
    print(f"Status: {r.status_code}")
    print(f"Response: {json.dumps(r.json(), indent=2)}")
except requests.exceptions.ConnectionError:
    print("ERROR: Could not connect to backend. Is it running?")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()



