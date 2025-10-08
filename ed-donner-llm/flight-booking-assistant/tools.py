# ============================================================================
# FILE 2: tools.py
# ============================================================================
"""
Tool definitions and handler functions for OpenAI function calling.
"""

import json
import random
from constants import MOCK_FLIGHT_DATA

# Tool definitions for OpenAI
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_flight_prices",
            "description": "Search for flight prices to a specific city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The destination city name"
                    },
                    "departure_date": {
                        "type": "string",
                        "description": "Departure date in YYYY-MM-DD format (optional)"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_cheaper_nearby_locations",
            "description": "Find Available & cheaper alternative destinations near the selected city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The original destination city"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of alternatives to return",
                        "default": 3
                    }
                },
                "required": ["city"]
            }
        }
    }
]


def search_flight_prices(city, departure_date=None):
    """
    Search for flight prices to a destination city using mock data.
    
    Args:
        city (str): Destination city name
        departure_date (str): Departure date (optional)
    
    Returns:
        dict: Flight price information
    """
    city_lower = city.lower()
    
    if city_lower in MOCK_FLIGHT_DATA:
        flight_info = MOCK_FLIGHT_DATA[city_lower].copy()
        # Add some randomness to prices for realism
        price_variation = random.randint(-50, 100)
        flight_info["price"] = flight_info["base_price"] + price_variation
        flight_info["city"] = city.title()
        flight_info["departure_date"] = departure_date or "flexible"
        return flight_info
    else:
        available_cities = ", ".join(list(MOCK_FLIGHT_DATA.keys()))
        return {
            "city": city,
            "price": None,
            "availability": False,
            "message": f"No flights found to {city}: Available Cities {available_cities}"
        }


def find_cheaper_nearby_locations(city, max_results=3):
    """
    Find cheaper alternative destinations near the specified city.
    
    Args:
        city (str): Original destination city
        max_results (int): Maximum alternatives to return
    
    Returns:
        list: List of alternative destinations with prices
    """
    city_lower = city.lower()
    
    if city_lower not in MOCK_FLIGHT_DATA:
        return []
    
    original_price = MOCK_FLIGHT_DATA[city_lower]["base_price"]
    nearby_cities = MOCK_FLIGHT_DATA[city_lower]["nearby_cities"]
    
    alternatives = []
    for nearby_city in nearby_cities[:max_results]:
        if nearby_city in MOCK_FLIGHT_DATA:
            nearby_info = MOCK_FLIGHT_DATA[nearby_city].copy()
            price_variation = random.randint(-30, 50)
            nearby_price = nearby_info["base_price"] + price_variation
            
            alternatives.append({
                "city": nearby_city.title(),
                "price": nearby_price,
                "savings": original_price - nearby_price,
                "currency": "USD"
            })
    print("=="*88)
    print(alternatives)
    # Sort by price (cheapest first)
    alternatives.sort(key=lambda x: x["price"])
    return alternatives


def execute_tool(tool_name, tool_args):
    """
    Execute a tool function by name.
    
    Args:
        tool_name (str): Name of the tool to execute
        tool_args (dict): Arguments for the tool
    
    Returns:
        str: JSON string of tool result
    """
    if tool_name == "search_flight_prices":
        result = search_flight_prices(**tool_args)
        return json.dumps(result)
    
    elif tool_name == "find_cheaper_nearby_locations":
        result = find_cheaper_nearby_locations(**tool_args)
        return json.dumps(result)
    
    else:
        return json.dumps({"error": f"Tool '{tool_name}' not found"})