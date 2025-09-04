#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingredient_service import get_ingredients_by_dish_name

def test_ingredient_function():
    test_cases = [
        "Chicken Burger",
        "Beef Burger", 
        "Burger",
        "Margherita Pizza",
        "Spaghetti Carbonara"
    ]
    
    for dish_name in test_cases:
        print(f"\n=== Testing: {dish_name} ===")
        try:
            result = get_ingredients_by_dish_name(dish_name)
            print(f"Result type: {type(result)}")
            print(f"Result length: {len(result) if result else 0}")
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_ingredient_function() 