"""
Quick check of all cities' stored data
"""
import json

with open('data/locations_data.json', 'r') as f:
    data = json.load(f)

print("=" * 60)
print("CURRENT STORED DATA FOR ALL CITIES")
print("=" * 60)
print()

for city_name in sorted(data.keys()):
    city_data = data[city_name]
    print(f"{city_name:12} - {city_data['current_people']:2} people ({city_data['crowd_level']:6})")
    print(f"              Average: {city_data['average_people']:.1f}, Max: {city_data['max_people']}, Min: {city_data['min_people']}")
    print(f"              Last updated: {city_data['last_updated']}")
    print()

print("=" * 60)
print("If the app shows different numbers, refresh the page")
print("or restart the backend to clear any browser cache.")
print("=" * 60)

