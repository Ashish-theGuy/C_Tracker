"""
7 Famous Tourist Spots in Kerala, India
"""
KERALA_CITIES = {
    "Munnar": {
        "name": "Munnar",
        "state": "Kerala",
        "country": "India",
        "coordinates": {"lat": 10.0889, "lng": 77.0595},
        "description": "Hill station known for tea plantations and scenic beauty",
        "video_file": "../City1.mp4"
    },
    "Alleppey": {
        "name": "Alleppey",
        "state": "Kerala",
        "country": "India",
        "coordinates": {"lat": 9.4981, "lng": 76.3388},
        "description": "Famous for backwaters and houseboat cruises",
        "video_file": "../city2.mp4"
    },
    "Kochi": {
        "name": "Kochi",
        "state": "Kerala",
        "country": "India",
        "coordinates": {"lat": 9.9312, "lng": 76.2673},
        "description": "Historic port city with colonial architecture",
        "video_file": "../city3.mp4"
    },
    "Wayanad": {
        "name": "Wayanad",
        "state": "Kerala",
        "country": "India",
        "coordinates": {"lat": 11.6854, "lng": 76.1320},
        "description": "Hill district with wildlife sanctuaries and waterfalls",
        "video_file": "../city4.mp4"
    },
    "Thekkady": {
        "name": "Thekkady",
        "state": "Kerala",
        "country": "India",
        "coordinates": {"lat": 9.5833, "lng": 77.1667},
        "description": "Home to Periyar National Park and spice plantations",
        "video_file": "../city5.mp4"
    },
    "Kovalam": {
        "name": "Kovalam",
        "state": "Kerala",
        "country": "India",
        "coordinates": {"lat": 8.3667, "lng": 76.9833},
        "description": "Beach destination with lighthouse and surfing",
        "video_file": "../city6.mp4"
    },
    "Varkala": {
        "name": "Varkala",
        "state": "Kerala",
        "country": "India",
        "coordinates": {"lat": 8.7375, "lng": 76.7167},
        "description": "Cliff beach with natural springs and temples",
        "video_file": "../city7.mp4"
    },
    "RSET": {
        "name": "RSET",
        "state": "Kerala",
        "country": "India",
        "coordinates": {"lat": 9.993311, "lng": 76.358384},
        "description": "Rajagiri School of Engineering & Technology, Kakkanad",
        "video_file": "http://10.179.26.207:8080/video"
    },
    "RSET_Library": {
        "name": "Library (RSET)",
        "state": "Kerala",
        "country": "India",
        "coordinates": {"lat": 9.993711, "lng": 76.358084},
        "description": "RSET Central Library",
        "video_file": "http://10.0.4.80:8080/video",
        "parent": "RSET"
    },
    "RSET_Canteen": {
        "name": "Canteen (RSET)",
        "state": "Kerala",
        "country": "India",
        "coordinates": {"lat": 9.993011, "lng": 76.358684},
        "description": "RSET Main Canteen",
        "video_file": "http://10.0.4.1:8080/video",
        "parent": "RSET"
    },
    "RSET_S6IT": {
        "name": "S6 IT Classroom",
        "state": "Kerala",
        "country": "India",
        "coordinates": {"lat": 9.992911, "lng": 76.358000},
        "description": "Semester 6 Information Technology Classroom",
        "video_file": "http://10.0.4.115:8080/video",
        "parent": "RSET"
    }
}

def get_city_by_name(city_name):
    """Get city info by name (case-insensitive)"""
    city_name_lower = city_name.lower().strip()
    for key, city in KERALA_CITIES.items():
        if key.lower() == city_name_lower:
            return city
    return None

def get_all_cities():
    """Get all Kerala cities"""
    return list(KERALA_CITIES.values())

def get_city_names():
    """Get list of all city names"""
    return list(KERALA_CITIES.keys())

# Resolve relative video paths to absolute paths on load
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
for city in KERALA_CITIES.values():
    video = city.get('video_file', '')
    if video.startswith('../'):
        city['video_file'] = os.path.normpath(os.path.join(current_dir, video))

