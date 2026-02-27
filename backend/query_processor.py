"""
Natural Language Query Processor
Processes user queries about Kerala cities
"""
import re
from kerala_cities import KERALA_CITIES, get_city_by_name, get_city_names

class QueryProcessor:
    """Process natural language queries about cities"""
    
    def __init__(self):
        self.city_names = get_city_names()
        self.city_names_lower = [name.lower() for name in self.city_names]
    
    def get_all_city_names(self):
        """Get all city names"""
        return self.city_names
    
    def extract_city_from_query(self, query: str) -> str:
        """
        Extract city name from user query
        
        Args:
            query: User's natural language query
        
        Returns:
            City name if found, None otherwise
        """
        query_lower = query.lower()
        
        # Check for exact city name matches
        for city_name in self.city_names:
            if city_name.lower() in query_lower:
                return city_name
        
        # Check for common variations
        city_variations = {
            "alleppey": "Alleppey",
            "alappuzha": "Alleppey",
            "cochin": "Kochi",
            "kochi": "Kochi",
            "munnar": "Munnar",
            "wayanad": "Wayanad",
            "thekkady": "Thekkady",
            "kovalam": "Kovalam",
            "varkala": "Varkala"
        }
        
        for variation, city_name in city_variations.items():
            if variation in query_lower:
                return city_name
        
        return None
    
    def is_visit_question(self, query: str) -> bool:
        """Check if query is asking about visiting a place"""
        visit_keywords = [
            "visit", "go", "travel", "should i", "can i", 
            "is it good", "crowd", "busy", "recommend"
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in visit_keywords)
    
    def process_query(self, query: str) -> dict:
        """
        Process user query and extract intent
        
        Returns:
            {
                "city": city_name or None,
                "intent": "visit_question" or "general",
                "original_query": query
            }
        """
        city = self.extract_city_from_query(query)
        intent = "visit_question" if self.is_visit_question(query) else "general"
        
        return {
            "city": city,
            "intent": intent,
            "original_query": query
        }

