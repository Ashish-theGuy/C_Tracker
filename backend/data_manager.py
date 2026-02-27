"""
Data Manager for storing and retrieving location crowd data
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class DataManager:
    """Manage location data storage and retrieval"""
    
    def __init__(self, data_file: str = None):
        # Use absolute path relative to project root
        if data_file is None:
            # Get the directory where this file is located (backend/)
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to project root
            project_root = os.path.dirname(backend_dir)
            # Path to data file in project root
            data_file = os.path.join(project_root, 'data', 'locations_data.json')
        self.data_file = data_file
        self.ensure_data_directory()
        self.load_data()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        data_dir = os.path.dirname(self.data_file)
        os.makedirs(data_dir, exist_ok=True)
    
    def load_data(self):
        """Load location data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.locations_data = json.load(f)
            except:
                self.locations_data = {}
        else:
            self.locations_data = {}
    
    def save_data(self):
        """Save location data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.locations_data, f, indent=2)
    
    def save_location_data(self, location_name: str, stats: Dict, coordinates: Dict = None):
        """
        Save or update location data
        
        Args:
            location_name: Name of the location
            stats: Statistics from video processing
            coordinates: Location coordinates {lat, lng}
        """
        self.load_data()  # Reload to get latest data
        
        # Get or create location entry
        if location_name in self.locations_data:
            location = self.locations_data[location_name]
            # Update existing data
            location['current_people'] = stats.get('current_people', 0)
            location['average_people'] = stats.get('average_people', 0)
            location['max_people'] = stats.get('max_people', 0)
            location['min_people'] = stats.get('min_people', 0)
            location['crowd_level'] = stats.get('crowd_level', 'Unknown')
            location['last_updated'] = datetime.now().isoformat()
            
            # Add to history (keep last 10 entries)
            history_entry = {
                "timestamp": datetime.now().isoformat(),
                "people_count": stats.get('current_people', 0),
                "crowd_level": stats.get('crowd_level', 'Unknown')
            }
            location['history'].append(history_entry)
            if len(location['history']) > 10:
                location['history'] = location['history'][-10:]
        else:
            # Create new location entry
            self.locations_data[location_name] = {
                "location_name": location_name,
                "coordinates": coordinates or {},
                "current_people": stats.get('current_people', 0),
                "average_people": stats.get('average_people', 0),
                "max_people": stats.get('max_people', 0),
                "min_people": stats.get('min_people', 0),
                "crowd_level": stats.get('crowd_level', 'Unknown'),
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "history": stats.get('history', [])
            }
        
        self.save_data()
    
    def get_location_data(self, location_name: str) -> Optional[Dict]:
        """Get data for a specific location"""
        self.load_data()  # Reload to get latest data
        return self.locations_data.get(location_name)
    
    def get_all_locations(self) -> List[Dict]:
        """Get all locations with their current status"""
        self.load_data()  # Reload to get latest data
        
        locations = []
        for name, data in self.locations_data.items():
            locations.append({
                "name": name,
                "current_people": data.get('current_people', 0),
                "crowd_level": data.get('crowd_level', 'Unknown'),
                "coordinates": data.get('coordinates', {}),
                "last_updated": data.get('last_updated', 'Unknown')
            })
        
        return locations
    
    def delete_location(self, location_name: str) -> bool:
        """Delete a location from data"""
        self.load_data()
        if location_name in self.locations_data:
            del self.locations_data[location_name]
            self.save_data()
            return True
        return False

