#!/usr/bin/env python3
"""
Test script for nutrition service
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nutrition_service import get_nutrition_info
import json

def test_nutrition_service():
    """Test the nutrition service with various dishes"""
    
    test_dishes = [
        "Chicken Tikka Masala",
        "Spaghetti Carbonara", 
        "Margherita Pizza",
        "Caesar Salad",
        "Chocolate Cake"
    ]
    
    print("🧪 Testing Nutrition Service")
    print("=" * 50)
    
    for dish in test_dishes:
        print(f"\n📋 Testing: {dish}")
        print("-" * 30)
        
        try:
            result = get_nutrition_info(dish)
            
            if result.get('success'):
                nutrition = result.get('nutrition', {})
                print(f"✅ Success!")
                print(f"   Calories: {nutrition.get('calories', 'unknown')}")
                print(f"   Protein: {nutrition.get('protein', 'unknown')}g")
                print(f"   Carbs: {nutrition.get('carbs', 'unknown')}g")
                print(f"   Fat: {nutrition.get('fat', 'unknown')}g")
                print(f"   Fiber: {nutrition.get('fiber', 'unknown')}g")
                print(f"   Sugar: {nutrition.get('sugar', 'unknown')}g")
                print(f"   Dietary Tags: {', '.join(nutrition.get('dietary_tags', []))}")
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")

if __name__ == "__main__":
    test_nutrition_service() 