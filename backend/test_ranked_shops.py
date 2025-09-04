#!/usr/bin/env python3
"""
Test script for the new ranked shops functionality
Demonstrates the exact JSON structure requested by the user
"""

import requests
import json

def test_ranked_shops():
    """Test the new ranked shops endpoint"""
    
    # Test data
    test_cases = [
        {
            "dish_name": "Pizza",
            "user_location": {"lat": 37.7749, "lng": -122.4194},  # San Francisco
            "expected_ingredients": ["flour", "mozzarella", "basil", "tomato", "olive oil"]
        },
        {
            "dish_name": "Carbonara",
            "user_location": {"lat": 37.7749, "lng": -122.4194},
            "expected_ingredients": ["pasta", "eggs", "pecorino", "guanciale", "black pepper"]
        },
        {
            "dish_name": "Chicken Curry",
            "user_location": {"lat": 37.7749, "lng": -122.4194},
            "expected_ingredients": ["chicken", "onion", "garlic", "ginger", "spices"]
        }
    ]
    
    print("🚚 Testing WeKno Ranked Shops System")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['dish_name']}")
        print("-" * 30)
        
        # Make request to the new endpoint
        url = "http://localhost:5001/delivery/ranked-shops"
        payload = {
            "dish_name": test_case["dish_name"],
            "user_location": test_case["user_location"],
            "max_distance_km": 5,
            "min_match_percent": 60
        }
        
        try:
            response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Success! Found {len(data['all_qualified_shops'])} qualified shops")
                print(f"🍽️ Dish: {data['dish']}")
                print(f"📦 Total Ingredients: {len(data['ingredients'])}")
                
                # Top shop details
                top_shop = data['top_shop']
                print(f"\n🏆 TOP SHOP:")
                print(f"   🏪 Name: {top_shop['name']}")
                print(f"   📊 Match: {top_shop['match_percent']}%")
                print(f"   📍 Distance: {top_shop['distance_km']} km")
                print(f"   ✅ Available: {len(top_shop['available_ingredients'])} ingredients")
                print(f"   ❌ Missing: {len(top_shop['missing_ingredients'])} ingredients")
                
                # Delivery agent details
                agent = data['delivery_agent']
                print(f"\n🚚 DELIVERY AGENT:")
                print(f"   👤 Name: {agent['name']}")
                print(f"   📍 Distance to Shop: {agent['distance_to_shop_km']} km")
                print(f"   ⏱️ ETA: {agent['eta_minutes']} minutes")
                
                # All qualified shops
                print(f"\n🏪 ALL QUALIFIED SHOPS:")
                for j, shop in enumerate(data['all_qualified_shops'], 1):
                    print(f"   {j}. {shop['name']} - {shop['match_percent']}% match, {shop['distance_km']} km")
                
                # Show sample ingredients
                print(f"\n📋 SAMPLE INGREDIENTS:")
                print(f"   Available: {', '.join(top_shop['available_ingredients'][:3])}...")
                if top_shop['missing_ingredients']:
                    print(f"   Missing: {', '.join(top_shop['missing_ingredients'][:3])}...")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        
        print("\n" + "=" * 50)

def test_custom_parameters():
    """Test with custom distance and match parameters"""
    
    print("\n🔧 Testing Custom Parameters")
    print("=" * 50)
    
    # Test with stricter requirements
    payload = {
        "dish_name": "Pizza",
        "user_location": {"lat": 37.7749, "lng": -122.4194},
        "max_distance_km": 3,  # Stricter distance
        "min_match_percent": 80  # Higher match requirement
    }
    
    url = "http://localhost:5001/delivery/ranked-shops"
    
    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['all_qualified_shops'])} shops with 80%+ match within 3km")
            for shop in data['all_qualified_shops']:
                print(f"   🏪 {shop['name']} - {shop['match_percent']}% match, {shop['distance_km']} km")
        else:
            print(f"❌ No shops found with stricter requirements: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting WeKno Ranked Shops Test")
    print("Make sure the backend server is running on http://localhost:5001")
    print()
    
    # Test basic functionality
    test_ranked_shops()
    
    # Test custom parameters
    test_custom_parameters()
    
    print("\n🎉 Test completed!")
    print("\n📝 Expected JSON Structure:")
    print("""
{
  "dish": "Pizza",
  "ingredients": ["flour", "mozzarella", "basil", ...],
  "top_shop": {
    "name": "Super Foods",
    "match_percent": 82,
    "distance_km": 2.1,
    "available_ingredients": [...],
    "missing_ingredients": [...]
  },
  "delivery_agent": {
    "name": "Agent B",
    "distance_to_shop_km": 1.2,
    "eta_minutes": 10
  }
}
    """) 