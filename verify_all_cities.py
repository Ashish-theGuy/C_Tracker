"""
Verify all cities have accurate data and reprocess if needed
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, os.path.dirname(__file__))

from backend.data_manager import DataManager
from backend.kerala_cities import KERALA_CITIES
from backend.video_processor import VideoProcessor

def verify_all_cities():
    """Verify and update all city data"""
    print("=" * 70)
    print("VERIFYING ALL KERALA CITIES - Ensuring Accurate Data")
    print("=" * 70)
    
    data_manager = DataManager()
    processor = VideoProcessor()
    
    cities_status = []
    
    for city_name, city_info in KERALA_CITIES.items():
        print(f"\n[{city_name}]")
        print(f"  Video: {city_info['video_file']}")
        
        # Check if video exists
        video_path = city_info['video_file']
        if not os.path.exists(video_path):
            alt_path = video_path.replace('../', '')
            if os.path.exists(alt_path):
                video_path = alt_path
                print(f"  Found video at: {alt_path}")
            else:
                print(f"  ERROR: Video not found!")
                cities_status.append({
                    'city': city_name,
                    'status': 'error',
                    'message': 'Video file not found'
                })
                continue
        else:
            print(f"  Found video at: {video_path}")
        
        # Get current stored data
        stored_data = data_manager.get_location_data(city_name)
        
        if stored_data:
            print(f"  Current stored data:")
            print(f"    - People: {stored_data['current_people']}")
            print(f"    - Crowd level: {stored_data['crowd_level']}")
            print(f"    - Last updated: {stored_data['last_updated']}")
        
        # Reprocess to ensure accuracy
        print(f"  Reprocessing video to ensure accuracy...")
        try:
            stats = processor.process_location_video(
                video_path,
                city_name,
                city_info['coordinates']
            )
            
            # Store updated data
            data_manager.save_location_data(city_name, stats, city_info['coordinates'])
            
            # Get updated data
            updated_data = data_manager.get_location_data(city_name)
            
            print(f"  Updated data:")
            print(f"    - People: {updated_data['current_people']}")
            print(f"    - Crowd level: {updated_data['crowd_level']}")
            print(f"    - Average: {updated_data['average_people']:.1f}")
            print(f"    - Max: {updated_data['max_people']}")
            print(f"    - Min: {updated_data['min_people']}")
            
            cities_status.append({
                'city': city_name,
                'status': 'success',
                'people': updated_data['current_people'],
                'crowd_level': updated_data['crowd_level']
            })
            
        except Exception as e:
            print(f"  ERROR processing: {e}")
            cities_status.append({
                'city': city_name,
                'status': 'error',
                'message': str(e)
            })
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    successful = [c for c in cities_status if c['status'] == 'success']
    errors = [c for c in cities_status if c['status'] == 'error']
    
    print(f"\nSuccessfully processed: {len(successful)}/{len(cities_status)} cities")
    print("\nCity Status:")
    for city in cities_status:
        if city['status'] == 'success':
            print(f"  {city['city']:12} - {city['people']:2} people ({city['crowd_level']})")
        else:
            print(f"  {city['city']:12} - ERROR: {city.get('message', 'Unknown error')}")
    
    if errors:
        print(f"\nWARNING: {len(errors)} cities had errors!")
    else:
        print("\nAll cities processed successfully!")
    
    print("\n" + "=" * 70)
    print("IMPORTANT: Restart the backend to see updated data!")
    print("Run: restart_backend.bat or stop and start the backend manually")
    print("=" * 70)
    
    return cities_status

if __name__ == "__main__":
    verify_all_cities()

