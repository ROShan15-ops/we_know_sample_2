#!/usr/bin/env python3
"""
Simple test script for WeKno Food Delivery System
Tests core functionality without authentication
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5001"

def test_available_shops():
    """Test getting available shops"""
    print("\n🏪 Testing Available Shops")
    print("=" * 40)
    
    response = requests.get(f"{BASE_URL}/delivery/shops")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Found {result['total_shops']} shops:")
        
        for shop in result['shops']:
            print(f"   • {shop['name']} ({shop['inventory_count']} items)")
            print(f"     Location: {shop['location']}")
            print(f"     Sample items: {', '.join(shop['inventory'][:5])}...")
    else:
        print(f"❌ Failed to get shops: {response.status_code}")

def test_delivery_agents():
    """Test getting delivery agents"""
    print("\n🚚 Testing Delivery Agents")
    print("=" * 40)
    
    response = requests.get(f"{BASE_URL}/delivery/agents")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Found {result['total_agents']} agents ({result['available_agents']} available):")
        
        for agent in result['agents']:
            status_emoji = "🟢" if agent['status'] == 'available' else "🔴"
            print(f"   {status_emoji} {agent['name']} ({agent['status']})")
            print(f"     Location: {agent['current_location']}")
    else:
        print(f"❌ Failed to get agents: {response.status_code}")

def test_distance_calculation():
    """Test distance calculation"""
    print("\n📍 Testing Distance Calculation")
    print("=" * 40)
    
    # Test coordinates (San Francisco to different locations)
    test_data = {
        "origin": {"lat": 37.7749, "lng": -122.4194},  # San Francisco
        "destination": {"lat": 37.7849, "lng": -122.4094}  # Nearby location
    }
    
    response = requests.post(f"{BASE_URL}/delivery/calculate-distance", json=test_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Distance calculated: {result['distance_km']} km")
        print(f"📏 Distance Matrix: {result['distance_matrix']['distance']['text']}")
        print(f"⏱️  Duration: {result['distance_matrix']['duration']['text']}")
    else:
        print(f"❌ Distance calculation failed: {response.status_code}")

def test_ingredients_endpoint():
    """Test the existing ingredients endpoint to show TheMealDB integration"""
    print("\n🍽️  Testing TheMealDB Integration")
    print("=" * 40)
    
    test_dishes = ["Chicken Biryani", "Pizza", "Carbonara", "Chicken Curry"]
    
    for dish in test_dishes:
        print(f"\n📋 Testing: {dish}")
        
        response = requests.post(f"{BASE_URL}/ingredients", json={
            "dish_name": dish,
            "servings": 2
        })
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Found {len(result['ingredients'])} ingredients")
            
            # Show first 3 ingredients
            for i, ingredient in enumerate(result['ingredients'][:3]):
                print(f"   {i+1}. {ingredient['ingredient']} ({ingredient['quantity']} {ingredient['unit']})")
            
            if len(result['ingredients']) > 3:
                print(f"   ... and {len(result['ingredients']) - 3} more ingredients")
        else:
            print(f"❌ Failed: {response.json().get('error', 'Unknown error')}")

def simulate_delivery_order(dish_name, servings=2):
    """Simulate a delivery order by combining ingredients + shop matching"""
    print(f"\n🚀 Simulating Delivery Order for: {dish_name}")
    print("=" * 60)
    
    # Step 1: Get ingredients
    ingredients_response = requests.post(f"{BASE_URL}/ingredients", json={
        "dish_name": dish_name,
        "servings": servings
    })
    
    if ingredients_response.status_code != 200:
        print(f"❌ Failed to get ingredients: {ingredients_response.json().get('error', 'Unknown error')}")
        return
    
    ingredients_data = ingredients_response.json()
    ingredients = ingredients_data['ingredients']
    
    print(f"📋 Recipe Ingredients ({len(ingredients)} total):")
    for i, ingredient in enumerate(ingredients[:5]):
        print(f"   {i+1}. {ingredient['ingredient']} ({ingredient['quantity']} {ingredient['unit']})")
    if len(ingredients) > 5:
        print(f"   ... and {len(ingredients) - 5} more")
    
    # Step 2: Get shops
    shops_response = requests.get(f"{BASE_URL}/delivery/shops")
    if shops_response.status_code != 200:
        print(f"❌ Failed to get shops")
        return
    
    shops_data = shops_response.json()
    
    # Step 3: Simulate shop matching
    print(f"\n🏪 Shop Matching Analysis:")
    
    best_shop = None
    best_coverage = 0
    
    for shop in shops_data['shops']:
        available_count = 0
        missing_ingredients = []
        
        for ingredient in ingredients:
            ingredient_name = ingredient['ingredient'].lower()
            found = False
            
            for shop_item in shop['inventory']:
                if ingredient_name in shop_item.lower() or shop_item.lower() in ingredient_name:
                    found = True
                    break
            
            if found:
                available_count += 1
            else:
                missing_ingredients.append(ingredient['ingredient'])
        
        coverage_percentage = (available_count / len(ingredients)) * 100
        
        print(f"   📊 {shop['name']}: {available_count}/{len(ingredients)} ingredients ({coverage_percentage:.1f}%)")
        
        if coverage_percentage > best_coverage:
            best_coverage = coverage_percentage
            best_shop = {
                'name': shop['name'],
                'available_count': available_count,
                'missing_ingredients': missing_ingredients,
                'coverage': coverage_percentage
            }
    
    # Step 4: Show best shop
    if best_shop:
        print(f"\n🏆 Best Shop: {best_shop['name']}")
        print(f"   ✅ Coverage: {best_shop['coverage']:.1f}% ({best_shop['available_count']}/{len(ingredients)} ingredients)")
        
        if best_shop['missing_ingredients']:
            print(f"   ❌ Missing: {', '.join(best_shop['missing_ingredients'][:3])}")
            if len(best_shop['missing_ingredients']) > 3:
                print(f"      ... and {len(best_shop['missing_ingredients']) - 3} more")
    
    # Step 5: Simulate delivery time
    estimated_time = "15-25 mins" if best_shop and best_shop['coverage'] > 70 else "20-30 mins"
    print(f"   ⏰ Estimated Delivery Time: {estimated_time}")

def main():
    """Run all delivery tests"""
    print("🚀 WeKno Food Delivery System - Simple Test Suite")
    print("=" * 60)
    
    # Test basic functionality
    test_available_shops()
    test_delivery_agents()
    test_distance_calculation()
    test_ingredients_endpoint()
    
    # Test delivery simulation with different dishes
    test_dishes = [
        ("Chicken Biryani", 2),
        ("Pizza", 4),
        ("Carbonara", 2),
        ("Chicken Curry", 3)
    ]
    
    for dish_name, servings in test_dishes:
        simulate_delivery_order(dish_name, servings)
        time.sleep(1)  # Small delay between requests
    
    print("\n🎉 All tests completed!")
    print("\n💡 To test the full delivery system with authentication:")
    print("   1. Create a user account using /auth/register")
    print("   2. Login to get an access token")
    print("   3. Use the token to call /delivery endpoint")
    print("   4. Run: python3 test_delivery.py")

if __name__ == "__main__":
    main() 