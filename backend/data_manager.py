"""
Data Manager for storing and retrieving location crowd data using SQLite
"""
import sqlite3
import os
import json
from datetime import datetime
from typing import Dict, List, Optional

class DataManager:
    """Manage location data storage and retrieval via SQLite"""
    
    def __init__(self, db_file: str = None):
        # Use absolute path relative to project root
        if db_file is None:
            # Get the directory where this file is located (backend/)
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to project root
            project_root = os.path.dirname(backend_dir)
            # Path to db file in project root
            db_file = os.path.join(project_root, 'data', 'locations_data.db')
        self.db_file = db_file
        self.ensure_data_directory()
        self.init_db()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        data_dir = os.path.dirname(self.db_file)
        os.makedirs(data_dir, exist_ok=True)
        
    def _get_connection(self):
        # check_same_thread=False allows Flask's multi-threading to reuse connection safely in SQLite
        conn = sqlite3.connect(self.db_file, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Create necessary tables if they don't exist"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Table for latest status
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations_status (
                location_name TEXT PRIMARY KEY,
                coordinates_json TEXT,
                current_people INTEGER,
                average_people INTEGER,
                max_people INTEGER,
                min_people INTEGER,
                crowd_level TEXT,
                created_at TEXT,
                last_updated TEXT
            )
        ''')
        
        # Table for historical records (append-only)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location_name TEXT,
                timestamp TEXT,
                people_count INTEGER,
                crowd_level TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def load_data(self):
        """No-op for backward compatibility with app.py's JSON logic"""
        pass
    
    def save_data(self):
        """No-op for backward compatibility with app.py's JSON logic"""
        pass
    
    def save_location_data(self, location_name: str, stats: Dict, coordinates: Dict = None):
        """
        Save or update location data instantly to SQLite.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        now_str = datetime.now().isoformat()
        coords_str = json.dumps(coordinates or {})
        
        curr = stats.get('current_people', 0)
        avg = stats.get('average_people', 0)
        mx = stats.get('max_people', 0)
        mn = stats.get('min_people', 0)
        lvl = stats.get('crowd_level', 'Unknown')
        
        # 1. UPSERT the latest status
        cursor.execute('''
            INSERT INTO locations_status 
            (location_name, coordinates_json, current_people, average_people, max_people, min_people, crowd_level, created_at, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(location_name) DO UPDATE SET
                coordinates_json=excluded.coordinates_json,
                current_people=excluded.current_people,
                average_people=excluded.average_people,
                max_people=excluded.max_people,
                min_people=excluded.min_people,
                crowd_level=excluded.crowd_level,
                last_updated=excluded.last_updated
        ''', (location_name, coords_str, curr, avg, mx, mn, lvl, now_str, now_str))
        
        # 2. Add to history
        cursor.execute('''
            INSERT INTO locations_history (location_name, timestamp, people_count, crowd_level)
            VALUES (?, ?, ?, ?)
        ''', (location_name, now_str, curr, lvl))
        
        # 3. Prune history to keep only last 10 entries per location
        cursor.execute('''
            DELETE FROM locations_history 
            WHERE location_name = ? AND id NOT IN (
                SELECT id FROM locations_history 
                WHERE location_name = ? 
                ORDER BY timestamp DESC LIMIT 10
            )
        ''', (location_name, location_name))
        
        conn.commit()
        conn.close()
    
    def get_location_data(self, location_name: str) -> Optional[Dict]:
        """Fetch location data and format identically to old JSON style"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM locations_status WHERE location_name = ?", (location_name,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
            
        # Get history
        cursor.execute('''
            SELECT timestamp, people_count, crowd_level 
            FROM locations_history 
            WHERE location_name = ? 
            ORDER BY timestamp ASC
        ''', (location_name,))
        
        history = [dict(r) for r in cursor.fetchall()]
        
        conn.close()
        
        # Format back to expected dictionary
        return {
            "location_name": row["location_name"],
            "coordinates": json.loads(row["coordinates_json"]),
            "current_people": row["current_people"],
            "average_people": row["average_people"],
            "max_people": row["max_people"],
            "min_people": row["min_people"],
            "crowd_level": row["crowd_level"],
            "created_at": row["created_at"],
            "last_updated": row["last_updated"],
            "history": history
        }
    
    def get_all_locations(self) -> List[Dict]:
        """Get all locations with their current status for app.py API"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM locations_status")
        rows = cursor.fetchall()
        
        locations = []
        for row in rows:
            locations.append({
                "name": row["location_name"],
                "current_people": row["current_people"],
                "crowd_level": row["crowd_level"],
                "coordinates": json.loads(row["coordinates_json"]),
                "last_updated": row["last_updated"]
            })
            
        conn.close()
        return locations
    
    def delete_location(self, location_name: str) -> bool:
        """Delete a location from SQLite"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM locations_status WHERE location_name = ?", (location_name,))
        deleted = cursor.rowcount > 0
        
        if deleted:
            cursor.execute("DELETE FROM locations_history WHERE location_name = ?", (location_name,))
            conn.commit()
            
        conn.close()
        return deleted


