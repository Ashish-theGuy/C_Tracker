"""
Test what the backend API returns for Varkala
"""
import requests
import json

def test_varkala():
    """Test Varkala API response"""
    print("=" * 60)
    print("Testing Varkala API Response")
    print("=" * 60)
    
    backend_url = "http://localhost:5000/api/ask"
    
    queries = [
        "What's the crowd like in Varkala?",
        "Should I visit Varkala?",
        "Is Varkala crowded?"
    ]
    
    for query in queries:
        print(f"\n[QUERY] {query}")
        try:
            response = requests.post(backend_url, json={"query": query}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('analysis', {})
                    print(f"  People detected: {analysis.get('current_people', 'N/A')}")
                    print(f"  Crowd level: {analysis.get('crowd_level', 'N/A')}")
                    print(f"  Average: {analysis.get('average_people', 'N/A')}")
                    print(f"  Max: {analysis.get('max_people', 'N/A')}")
                else:
                    print(f"  Error: {data.get('error', 'Unknown error')}")
            else:
                print(f"  HTTP {response.status_code}: {response.text[:200]}")
        except requests.exceptions.ConnectionError:
            print("  ERROR: Backend not running! Start it with: python run_backend.py")
            break
        except Exception as e:
            print(f"  ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("If it shows 3 people, the backend needs to be restarted.")
    print("=" * 60)

if __name__ == "__main__":
    test_varkala()

