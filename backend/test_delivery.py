#!/usr/bin/env python3
"""
Test script for WeKno Food Delivery System
Demonstrates the delivery functionality with various dishes
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5001"
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword123"

def login_user():
    """Login and get authentication token"""
    login_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.json()}")
        return None

def test_delivery_order(dish_name, servings=2, user_location=None):
    """Test creating a delivery order for a specific dish"""
    
    # Get auth token
    token = login_user()
    if not token:
        print("❌ Authentication failed")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Prepare delivery request
    delivery_data = {
        "dish_name": dish_name,
        "servings": servings
    }
    
    if user_location:
        delivery_data["user_location"] = user_location
    
    print(f"\n🍽️  Testing delivery for: {dish_name} ({servings} servings)")
    print("=" * 60)
    
    # Make delivery request
    response = requests.post(f"{BASE_URL}/delivery", json=delivery_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"✅ Delivery order created successfully!")
        print(f"📋 Order ID: {result['order_details']['order_id']}")
        print(f"🏪 Shop: {result['shop']['name']}")
        print(f"📍 Distance: {result['shop']['distance_km']} km")
        print(f"🚚 Delivery Agent: {result['assigned_delivery_agent']['name']}")
        print(f"⏰ Estimated Time: {result['estimated_delivery_time']}")
        print(f"📦 Ingredients: {result['order_details']['total_ingredients']} total")
        print(f"✅ Available: {result['order_details']['available_ingredients_count']}")
        print(f"❌ Missing: {result['order_details']['missing_ingredients_count']}")
        
        # Show ingredient coverage
        print(f"\n📊 Ingredient Coverage: {result['shop']['ingredient_coverage']}")
        
        if result['shop']['missing_ingredients']:
            print(f"\n❌ Missing Ingredients:")
            for ingredient in result['shop']['missing_ingredients']:
                print(f"   • {ingredient['ingredient']} ({ingredient['quantity']} {ingredient['unit']})")
        
        print(f"\n✅ Available Ingredients:")
        for ingredient in result['shop']['available_ingredients'][:5]:  # Show first 5
            print(f"   • {ingredient['ingredient']} ({ingredient['quantity']} {ingredient['unit']})")
        
        if len(result['shop']['available_ingredients']) > 5:
            print(f"   ... and {len(result['shop']['available_ingredients']) - 5} more")
            
    else:
        print(f"❌ Delivery order failed: {response.status_code}")
        print(f"Error: {response.json().get('error', 'Unknown error')}")

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

def main():
    """Run all delivery tests"""
    print("🚀 WeKno Food Delivery System - Test Suite")
    print("=" * 60)
    
    # Test basic functionality
    test_available_shops()
    test_delivery_agents()
    test_distance_calculation()
    
    # Test delivery orders with different dishes
    test_dishes = [
        ("Chicken Biryani", 2),
        ("Pizza", 4),
        ("Carbonara", 2),
        ("Chicken Curry", 3),
        ("Beef Stew", 2)
    ]
    
    # Test with different user locations
    test_locations = [
        {"lat": 37.7749, "lng": -122.4194},  # San Francisco
        {"lat": 37.7849, "lng": -122.4094},  # Nearby
        {"lat": 37.7649, "lng": -122.4294},  # Another location
    ]
    
    for dish_name, servings in test_dishes:
        for i, location in enumerate(test_locations):
            print(f"\n📍 Test {i+1} with location: {location}")
            test_delivery_order(dish_name, servings, location)
            time.sleep(1)  # Small delay between requests
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main() 