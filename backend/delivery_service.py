import math
import random
import logging
from mock_data import MOCK_SHOPS, DELIVERY_AGENTS
from config import Config

logger = logging.getLogger(__name__)

def calculate_distance(lat1, lng1, lat2, lng2):
    """
    Calculate distance between two points using Haversine formula
    Returns distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)
    
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    
    return distance

def find_and_rank_shops(user_location, ingredients, shops, max_distance_km=5, min_match_percent=60):
    """
    Find and rank shops based on ingredient match percentage and distance
    Returns shops within max_distance_km that have at least min_match_percent of ingredients
    """
    qualified_shops = []
    
    for shop_name, shop_data in shops.items():
        # Calculate distance to user
        distance_km = calculate_distance(
            user_location["lat"], user_location["lng"],
            shop_data["location"]["lat"], shop_data["location"]["lng"]
        )
        
        # Skip shops outside the maximum distance
        if distance_km > max_distance_km:
            continue
        
        # Match ingredients with shop inventory
        available_ingredients, missing_ingredients = match_ingredients_with_shop(ingredients, shop_data["inventory"])
        
        # Calculate match percentage
        total_ingredients = len(ingredients)
        available_count = len(available_ingredients)
        match_percent = (available_count / total_ingredients) * 100 if total_ingredients > 0 else 0
        
        # Skip shops that don't meet minimum match requirement
        if match_percent < min_match_percent:
            continue
        
        # Add shop to qualified list
        qualified_shops.append({
            "name": shop_name,
            "distance_km": round(distance_km, 1),
            "match_percent": round(match_percent, 1),
            "location": shop_data["location"],
            "inventory": shop_data["inventory"],
            "available_ingredients": available_ingredients,
            "missing_ingredients": missing_ingredients,
            "total_ingredients": total_ingredients,
            "available_count": available_count
        })
    
    # Sort shops by match percentage (descending) and then by distance (ascending)
    qualified_shops.sort(key=lambda x: (-x["match_percent"], x["distance_km"]))
    
    return qualified_shops

def match_ingredients_with_shop(ingredients, shop_inventory):
    """
    Match recipe ingredients with shop inventory
    Returns available and missing ingredients
    """
    available_ingredients = []
    missing_ingredients = []
    
    # Define ingredient substitutions for better matching
    ingredient_substitutions = {
        'heavy cream': ['heavy cream', 'whipping cream', 'double cream'],
        'whole milk': ['whole milk', 'milk', 'full fat milk'],
        'dark chocolate': ['dark chocolate', 'chocolate', 'bittersweet chocolate', 'semisweet chocolate'],
        'vanilla extract': ['vanilla extract', 'vanilla', 'vanilla essence'],
        'vanilla bean': ['vanilla bean', 'vanilla pod', 'vanilla extract'],
        'all-purpose flour': ['all-purpose flour', 'flour', 'plain flour'],
        'cocoa powder': ['cocoa powder', 'unsweetened cocoa', 'cocoa'],
        'baking soda': ['baking soda', 'sodium bicarbonate', 'bicarbonate of soda'],
        'baking powder': ['baking powder'],
        'extra virgin olive oil': ['extra virgin olive oil', 'olive oil', 'evoo'],
        'fresh mozzarella': ['fresh mozzarella', 'mozzarella', 'mozzarella cheese'],
        'tomato sauce': ['tomato sauce', 'pizza sauce', 'marinara sauce'],
        'fresh basil leaves': ['fresh basil leaves', 'basil', 'basil leaves'],
        'pepperoni slices': ['pepperoni slices', 'pepperoni', 'pepperoni sausage'],
        'parmesan cheese': ['parmesan cheese', 'parmesan', 'parmigiano reggiano'],
        'red pepper flakes': ['red pepper flakes', 'crushed red pepper', 'chili flakes']
    }
    
    for ingredient in ingredients:
        ingredient_name = ingredient.get('ingredient', '').lower().strip()
        
        # Check if ingredient is available in shop
        found = False
        
        # First, try exact match
        for shop_item in shop_inventory:
            if ingredient_name in shop_item.lower() or shop_item.lower() in ingredient_name:
                available_ingredients.append(ingredient)
                found = True
                break
        
        # If not found, try substitutions
        if not found:
            for key, substitutions in ingredient_substitutions.items():
                if ingredient_name in key or key in ingredient_name:
                    for substitution in substitutions:
                        for shop_item in shop_inventory:
                            if substitution in shop_item.lower() or shop_item.lower() in substitution:
                                available_ingredients.append(ingredient)
                                found = True
                                break
                        if found:
                            break
                if found:
                    break
        
        if not found:
            missing_ingredients.append(ingredient)
    
    return available_ingredients, missing_ingredients

def assign_delivery_agent(shop_location):
    """
    Assign the nearest available delivery agent to a shop
    """
    available_agents = [agent for agent in DELIVERY_AGENTS if agent["status"] == "available"]
    
    if not available_agents:
        return None
    
    # Find the nearest agent
    nearest_agent = None
    min_distance = float('inf')
    
    for agent in available_agents:
        distance = calculate_distance(
            shop_location["lat"], shop_location["lng"],
            agent["current_location"]["lat"], agent["current_location"]["lng"]
        )
        
        if distance < min_distance:
            min_distance = distance
            nearest_agent = agent
    
    if nearest_agent:
        return {
            "name": nearest_agent["name"],
            "distance_to_shop_km": round(min_distance, 1),
            "eta_minutes": estimate_delivery_time(min_distance, 0)
        }
    
    return None

def estimate_delivery_time(distance_km, ingredient_count):
    """
    Estimate delivery time based on distance and ingredient count
    """
    # Base time: 15 minutes for preparation
    base_time = 15
    
    # Travel time: 4 minutes per km (average city speed)
    travel_time = distance_km * 4
    
    # Additional time for ingredient count (more ingredients = more time to collect)
    ingredient_time = (ingredient_count / 5) * 2  # 2 minutes per 5 ingredients
    
    total_time = base_time + travel_time + ingredient_time
    
    return round(total_time)

def get_google_distance_matrix(origin, destination):
    """
    Mock Google Distance Matrix API call
    In a real implementation, this would call the actual Google API
    """
    # Calculate actual distance
    distance_km = calculate_distance(
        origin["lat"], origin["lng"],
        destination["lat"], destination["lng"]
    )
    
    # Mock response format similar to Google Distance Matrix API
    return {
        "status": "OK",
        "rows": [
            {
                "elements": [
                    {
                        "status": "OK",
                        "distance": {
                            "text": f"{distance_km:.1f} km",
                            "value": int(distance_km * 1000)  # Convert to meters
                        },
                        "duration": {
                            "text": f"{int(distance_km * 4)} mins",
                            "value": int(distance_km * 4 * 60)  # Convert to seconds
                        }
                    }
                ]
            }
        ]
    } 