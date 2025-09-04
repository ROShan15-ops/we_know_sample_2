import requests
import logging
from typing import Dict, Optional, List
from config import Config

# Set up logging
logger = logging.getLogger(__name__)

def normalize_ingredients_for_realistic_servings(ingredients: List[Dict]) -> List[Dict]:
    """
    Normalize ingredients to realistic home cooking portion sizes
    Converts restaurant-sized portions to typical home cooking portions
    """
    try:
        normalized_ingredients = []
        
        # Portion size adjustments for common ingredients
        portion_adjustments = {
            # Protein adjustments (restaurant vs home)
            'chicken': {'restaurant': 16, 'home': 6},  # oz per serving
            'chicken breast': {'restaurant': 16, 'home': 6},
            'chicken tenderloins': {'restaurant': 16, 'home': 6},
            'beef': {'restaurant': 12, 'home': 6},
            'ground beef': {'restaurant': 12, 'home': 6},
            'steak': {'restaurant': 12, 'home': 6},
            'pork': {'restaurant': 12, 'home': 6},
            'fish': {'restaurant': 10, 'home': 5},
            'salmon': {'restaurant': 10, 'home': 5},
            'shrimp': {'restaurant': 8, 'home': 4},
            
            # Pasta adjustments
            'pasta': {'restaurant': 8, 'home': 4},  # oz dry per serving
            'spaghetti': {'restaurant': 8, 'home': 4},
            'penne': {'restaurant': 8, 'home': 4},
            'fettuccine': {'restaurant': 8, 'home': 4},
            'linguine': {'restaurant': 8, 'home': 4},
            
            # Rice adjustments
            'rice': {'restaurant': 1, 'home': 0.5},  # cups cooked per serving
            'brown rice': {'restaurant': 1, 'home': 0.5},
            'white rice': {'restaurant': 1, 'home': 0.5},
            
            # Bread adjustments
            'bread': {'restaurant': 2, 'home': 1},  # slices per serving
            'bun': {'restaurant': 1, 'home': 1},  # buns per serving
            'tortilla': {'restaurant': 2, 'home': 1},  # tortillas per serving
            
            # Cheese adjustments
            'cheese': {'restaurant': 2, 'home': 1},  # oz per serving
            'mozzarella': {'restaurant': 2, 'home': 1},
            'parmesan': {'restaurant': 1, 'home': 0.5},
            'cheddar': {'restaurant': 2, 'home': 1},
            
            # Sauce adjustments
            'sauce': {'restaurant': 0.5, 'home': 0.25},  # cups per serving
            'marinara': {'restaurant': 0.5, 'home': 0.25},
            'alfredo': {'restaurant': 0.5, 'home': 0.25},
            'dressing': {'restaurant': 0.25, 'home': 0.125},  # cups per serving
        }
        
        for ingredient_data in ingredients:
            ingredient_name = ingredient_data.get('ingredient', '').lower().strip()
            quantity = ingredient_data.get('quantity', 0)
            unit = ingredient_data.get('unit', '').lower().strip()

            # Normalize unrealistic units for common foods into sensible forms
            volume_units = {
                'tablespoon', 'tablespoons', 'tbsp', 'tbsp.',
                'teaspoon', 'teaspoons', 'tsp', 'tsp.',
                'cup', 'cups', 'liter', 'liters', 'l', 'l.', 'ml', 'milliliter', 'milliliters', 'ml.'
            }

            def set_if(condition: bool, new_unit: str, default_qty: float = 1.0):
                nonlocal unit, quantity
                if condition:
                    unit = new_unit
                    if not quantity or quantity <= 0:
                        quantity = default_qty

            # Bread: prefer slices, never volume units
            set_if('bread' in ingredient_name and (unit in volume_units or unit == ''), 'slice', 1)

            # Bacon: prefer slices
            set_if('bacon' in ingredient_name and unit in ['piece', 'pieces', 'pc', 'pcs', ''], 'slice', 2)

            # Sausages: prefer pieces
            set_if('sausage' in ingredient_name and unit in ['slice', 'slices', ''], 'piece', 2)

            # Eggs: prefer pieces
            set_if('egg' in ingredient_name and unit not in ['piece', 'pieces'], 'piece', 2)

            # Mushrooms, Tomatoes: default to pieces when unknown/volume
            set_if('mushroom' in ingredient_name and (unit in volume_units or unit == ''), 'piece', 4)
            set_if('tomato' in ingredient_name and (unit in volume_units or unit == ''), 'piece', 2)

            # Black pudding: usually slices
            set_if('pudding' in ingredient_name and (unit in volume_units or unit == '' or unit in ['piece', 'pieces']), 'slice', 2)
            
            # Check if this ingredient needs portion adjustment
            adjustment_factor = 1.0
            for key, adjustment in portion_adjustments.items():
                if key in ingredient_name:
                    # Calculate adjustment factor
                    restaurant_size = adjustment['restaurant']
                    home_size = adjustment['home']
                    adjustment_factor = home_size / restaurant_size
                    
                    # Apply adjustment
                    adjusted_quantity = quantity * adjustment_factor
                    
                    logger.info(f"🔄 Portion adjustment: {ingredient_name} {quantity}{unit} → {adjusted_quantity:.2f}{unit} (factor: {adjustment_factor:.2f})")
                    
                    normalized_ingredients.append({
                        'ingredient': ingredient_data['ingredient'],
                        'quantity': round(adjusted_quantity, 2),
                        'unit': unit
                    })
                    break
            else:
                # No adjustment needed, keep original
                normalized_ingredients.append(ingredient_data)
        
        return normalized_ingredients
        
    except Exception as e:
        logger.error(f"Error normalizing ingredients: {e}")
        return ingredients

def calculate_nutrition_from_ingredients(ingredients: List[Dict]) -> Dict:
    """
    Calculate nutrition information based on actual ingredients
    
    Args:
        ingredients (List[Dict]): List of ingredients with 'ingredient', 'quantity', 'unit'
        
    Returns:
        Dict: Calculated nutrition information
    """
    try:
        # Normalize ingredients to realistic portion sizes
        normalized_ingredients = normalize_ingredients_for_realistic_servings(ingredients)
        
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        total_fiber = 0
        total_sugar = 0
        
        # Nutrition database for common ingredients (per 100g or standard serving)
        nutrition_db = {
            'rice': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3, 'fiber': 0.4, 'sugar': 0.1},
            'brown rice': {'calories': 111, 'protein': 2.6, 'carbs': 23, 'fat': 0.9, 'fiber': 1.8, 'sugar': 0.4},
            'lemon': {'calories': 29, 'protein': 1.1, 'carbs': 9, 'fat': 0.3, 'fiber': 2.8, 'sugar': 1.5},
            'lemon juice': {'calories': 22, 'protein': 0.4, 'carbs': 7, 'fat': 0.2, 'fiber': 0.3, 'sugar': 1.2},
            'olive oil': {'calories': 884, 'protein': 0, 'carbs': 0, 'fat': 100, 'fiber': 0, 'sugar': 0},
            'onion': {'calories': 40, 'protein': 1.1, 'carbs': 9, 'fat': 0.1, 'fiber': 1.7, 'sugar': 4.7},
            'green onion': {'calories': 32, 'protein': 1.8, 'carbs': 7.3, 'fat': 0.2, 'fiber': 2.6, 'sugar': 2.3},
            'garlic': {'calories': 149, 'protein': 6.4, 'carbs': 33, 'fat': 0.5, 'fiber': 2.1, 'sugar': 1},
            'salt': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0, 'sugar': 0},
            'pepper': {'calories': 251, 'protein': 10.4, 'carbs': 64, 'fat': 3.3, 'fiber': 25.3, 'sugar': 0.6},
            'butter': {'calories': 717, 'protein': 0.9, 'carbs': 0.1, 'fat': 81, 'fiber': 0, 'sugar': 0.1},
            'chicken': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0, 'sugar': 0},
            'chicken breast': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0, 'sugar': 0},
            'almonds': {'calories': 579, 'protein': 21, 'carbs': 22, 'fat': 50, 'fiber': 12.5, 'sugar': 4.4},
            'celery': {'calories': 16, 'protein': 0.7, 'carbs': 3, 'fat': 0.2, 'fiber': 1.6, 'sugar': 1.3},
            'mayonnaise': {'calories': 680, 'protein': 1, 'carbs': 0.6, 'fat': 75, 'fiber': 0, 'sugar': 0.6},
            'paprika': {'calories': 282, 'protein': 14.1, 'carbs': 54, 'fat': 13, 'fiber': 34.9, 'sugar': 10.3},
            'grapes': {'calories': 62, 'protein': 0.6, 'carbs': 16, 'fat': 0.2, 'fiber': 0.9, 'sugar': 16},
            'milk': {'calories': 42, 'protein': 3.4, 'carbs': 5, 'fat': 1, 'fiber': 0, 'sugar': 5},
            'flour': {'calories': 364, 'protein': 10, 'carbs': 76, 'fat': 1, 'fiber': 2.7, 'sugar': 0.3},
            'sugar': {'calories': 387, 'protein': 0, 'carbs': 100, 'fat': 0, 'fiber': 0, 'sugar': 100},
            'eggs': {'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11, 'fiber': 0, 'sugar': 1.1},
            'tomatoes': {'calories': 18, 'protein': 0.9, 'carbs': 3.9, 'fat': 0.2, 'fiber': 1.2, 'sugar': 2.6},
            'cheese': {'calories': 402, 'protein': 25, 'carbs': 1.3, 'fat': 33, 'fiber': 0, 'sugar': 0.5},
            'cheddar cheese': {'calories': 402, 'protein': 25, 'carbs': 1.3, 'fat': 33, 'fiber': 0, 'sugar': 0.5},
            'parmesan cheese': {'calories': 431, 'protein': 38, 'carbs': 4.1, 'fat': 29, 'fiber': 0, 'sugar': 0.1},
            'ginger': {'calories': 80, 'protein': 1.8, 'carbs': 18, 'fat': 0.8, 'fiber': 2, 'sugar': 1.7},
            'cumin': {'calories': 375, 'protein': 18, 'carbs': 44, 'fat': 22, 'fiber': 10.5, 'sugar': 2.3},
            'cardamom': {'calories': 311, 'protein': 11, 'carbs': 68, 'fat': 6.7, 'fiber': 28, 'sugar': 0},
            'cayenne pepper': {'calories': 318, 'protein': 12, 'carbs': 56, 'fat': 17, 'fiber': 27.2, 'sugar': 10.3},
            'garam masala': {'calories': 315, 'protein': 13, 'carbs': 58, 'fat': 8, 'fiber': 25.6, 'sugar': 2.8},
            'bay leaf': {'calories': 313, 'protein': 7.6, 'carbs': 75, 'fat': 8.4, 'fiber': 26.3, 'sugar': 0},
            'cilantro': {'calories': 23, 'protein': 2.1, 'carbs': 3.7, 'fat': 0.5, 'fiber': 2.8, 'sugar': 0.9},
            'chives': {'calories': 30, 'protein': 3.3, 'carbs': 4.4, 'fat': 0.7, 'fiber': 2.5, 'sugar': 1.9},
            'parsley': {'calories': 36, 'protein': 3, 'carbs': 6.3, 'fat': 0.8, 'fiber': 3.3, 'sugar': 0.9},
            'apricots': {'calories': 48, 'protein': 1.4, 'carbs': 11, 'fat': 0.4, 'fiber': 2, 'sugar': 9.2},
            'dried apricots': {'calories': 241, 'protein': 3.4, 'carbs': 63, 'fat': 0.5, 'fiber': 7.3, 'sugar': 53.4},
            'mustard': {'calories': 66, 'protein': 4.4, 'carbs': 5.8, 'fat': 4.4, 'fiber': 4, 'sugar': 0.9},
            'dijon mustard': {'calories': 66, 'protein': 4.4, 'carbs': 5.8, 'fat': 4.4, 'fiber': 4, 'sugar': 0.9},
            'sour cream': {'calories': 198, 'protein': 2.4, 'carbs': 4.6, 'fat': 19, 'fiber': 0, 'sugar': 3.2},
            'greek yogurt': {'calories': 59, 'protein': 10, 'carbs': 3.6, 'fat': 0.4, 'fiber': 0, 'sugar': 3.2},
            'yogurt': {'calories': 59, 'protein': 10, 'carbs': 3.6, 'fat': 0.4, 'fiber': 0, 'sugar': 3.2},
            'spinach': {'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4, 'fiber': 2.2, 'sugar': 0.4},
            'baby spinach': {'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4, 'fiber': 2.2, 'sugar': 0.4},
            'green onions': {'calories': 32, 'protein': 1.8, 'carbs': 7.3, 'fat': 0.2, 'fiber': 2.6, 'sugar': 2.3},
            'parmesan': {'calories': 431, 'protein': 38, 'carbs': 4.1, 'fat': 29, 'fiber': 0, 'sugar': 0.1},
            # Add specific mappings for problematic ingredients
            'servings of': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0, 'sugar': 0},
            'squeezes of': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0, 'sugar': 0},
            'zest of': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0, 'sugar': 0},
            'sticks': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0, 'sugar': 0},
            # Add missing ingredients for Lemon Rice
            'lemon zest': {'calories': 29, 'protein': 1.1, 'carbs': 9, 'fat': 0.3, 'fiber': 2.8, 'sugar': 1.5},
            'mustard seeds': {'calories': 508, 'protein': 26, 'carbs': 28, 'fat': 36, 'fiber': 12, 'sugar': 6.8},
            'curry leaves': {'calories': 108, 'protein': 16, 'carbs': 18, 'fat': 1, 'fiber': 43, 'sugar': 0},
            'green chilies': {'calories': 40, 'protein': 2, 'carbs': 9, 'fat': 0.2, 'fiber': 1.5, 'sugar': 5.1},
            'turmeric powder': {'calories': 354, 'protein': 8, 'carbs': 65, 'fat': 10, 'fiber': 21, 'sugar': 3.2},
            'peanuts': {'calories': 567, 'protein': 26, 'carbs': 16, 'fat': 49, 'fiber': 8.5, 'sugar': 4.7},
            'oil': {'calories': 884, 'protein': 0, 'carbs': 0, 'fat': 100, 'fiber': 0, 'sugar': 0},
            # Add missing ingredients for Tonkatsu and other dishes
            'pork': {'calories': 242, 'protein': 27, 'carbs': 0, 'fat': 14, 'fiber': 0, 'sugar': 0},
            'breadcrumbs': {'calories': 395, 'protein': 13, 'carbs': 72, 'fat': 5, 'fiber': 4, 'sugar': 6},
            'vegetable oil': {'calories': 884, 'protein': 0, 'carbs': 0, 'fat': 100, 'fiber': 0, 'sugar': 0},
            'tomato ketchup': {'calories': 102, 'protein': 1, 'carbs': 25, 'fat': 0, 'fiber': 0, 'sugar': 22},
            'worcestershire sauce': {'calories': 78, 'protein': 0, 'carbs': 19, 'fat': 0, 'fiber': 0, 'sugar': 19},
            'oyster sauce': {'calories': 51, 'protein': 1, 'carbs': 11, 'fat': 0, 'fiber': 0, 'sugar': 11},
            'caster sugar': {'calories': 387, 'protein': 0, 'carbs': 100, 'fat': 0, 'fiber': 0, 'sugar': 100},
            'sugar': {'calories': 387, 'protein': 0, 'carbs': 100, 'fat': 0, 'fiber': 0, 'sugar': 100},
            'piece': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0, 'sugar': 0},  # Generic piece
            'liter': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0, 'sugar': 0},  # Generic liter
        }
        
        # Unit conversion factors (to grams)
        unit_conversions = {
            'cup': 240,  # 1 cup = 240g
            'cups': 240,
            'tablespoon': 15,  # 1 tbsp = 15g
            'tablespoons': 15,
            'tbsp': 15,
            'tbsp.': 15,
            'teaspoon': 5,  # 1 tsp = 5g
            'teaspoons': 5,
            'tsp': 5,
            'tsp.': 5,
            'ounce': 28.35,  # 1 oz = 28.35g
            'ounces': 28.35,
            'oz': 28.35,
            'oz.': 28.35,
            'pound': 453.59,  # 1 lb = 453.59g
            'pounds': 453.59,
            'lb': 453.59,
            'lb.': 453.59,
            'gram': 1,
            'grams': 1,
            'g': 1,
            'g.': 1,
            'milliliter': 1,  # 1ml = 1g for most liquids
            'milliliters': 1,
            'ml': 1,
            'ml.': 1,
            'liter': 1000,
            'liters': 1000,
            'l': 1000,
            'l.': 1000,
            'clove': 3,  # 1 garlic clove ≈ 3g
            'cloves': 3,
            'piece': 50,  # default fallback; overridden below for specific foods
            'pieces': 50,
            'slice': 25,  # default slice weight; overridden below for specific foods
            'slices': 25,
            'bun': 70,
            'buns': 70,
            'tortilla': 50,
            'tortillas': 50,
            'leaf': 5,
            'leaves': 5,
            'ring': 10,
            'rings': 10,
            'small': 100,  # 1 small onion ≈ 100g
            'medium': 150,  # 1 medium onion ≈ 150g
            'large': 200,  # 1 large onion ≈ 200g
            'bunch': 50,  # 1 bunch herbs ≈ 50g
            'pinch': 0.5,  # 1 pinch ≈ 0.5g
            'dash': 1,  # 1 dash ≈ 1g
            'sprinkle': 0.5,  # 1 sprinkle ≈ 0.5g
            'serving': 100,  # 1 serving ≈ 100g
            'servings': 100,
            'can': 400,  # 1 can ≈ 400g
            'pint': 473,  # 1 pint ≈ 473g
            'squeeze': 5,  # 1 squeeze lemon ≈ 5g
            'squeezes': 5,
            'zest': 2,  # 1 zest ≈ 2g
        }
        
        # Per-ingredient overrides for typical weights of slices/pieces
        per_item_weights = [
            # (keyword, unit, grams_per_unit)
            ('bread', 'slice', 25),
            ('bacon', 'slice', 15),
            ('sausage', 'piece', 50),
            ('mushroom', 'piece', 18),
            ('tomato', 'piece', 100),
            ('egg', 'piece', 50),
            ('pudding', 'slice', 50),  # black pudding slice
            ('bun', 'bun', 70),
            ('tortilla', 'tortilla', 50),
        ]

        for ingredient_data in normalized_ingredients:
            ingredient_name = ingredient_data.get('ingredient', '').lower().strip()
            quantity = ingredient_data.get('quantity', 0)
            unit = ingredient_data.get('unit', '').lower().strip()
            
            # Fix unrealistic units for dry ingredients
            if unit == 'liter' and any(word in ingredient_name for word in ['sugar', 'flour', 'salt', 'spice', 'powder']):
                logger.info(f"🔧 FIXING: Converting {quantity} liter of {ingredient_name} to tablespoon")
                unit = 'tablespoon'
                # Adjust quantity for more realistic amount
                if quantity > 3:
                    quantity = 2  # Cap at 2 tablespoons for dry ingredients
            
            logger.info(f"Processing ingredient: {ingredient_name} ({quantity} {unit})")
            
            # Skip invalid ingredients
            if not ingredient_name or quantity <= 0:
                logger.info(f"Skipping invalid ingredient: {ingredient_name}")
                continue
            
            # Skip problematic ingredients that don't make sense
            skip_ingredients = [
                'servings of', 'squeezes of', 'zest of', 'sticks', 'pieces', 'bunch', 'pinch', 'dash', 'sprinkle'
            ]
            if any(skip in ingredient_name for skip in skip_ingredients):
                logger.info(f"Skipping problematic ingredient: {ingredient_name}")
                continue
            
            # Skip ingredients with very high quantities that seem wrong
            if unit == 'servings' and quantity > 4:
                logger.info(f"Skipping ingredient with high servings: {ingredient_name} ({quantity} {unit})")
                continue
                
            # Find matching ingredient in nutrition database
            matched_ingredient = None
            for db_ingredient, nutrition in nutrition_db.items():
                if db_ingredient in ingredient_name or ingredient_name in db_ingredient:
                    matched_ingredient = nutrition
                    break
            
            if not matched_ingredient:
                logger.debug(f"No nutrition data found for ingredient: {ingredient_name}")
                continue
            
            # Convert quantity to grams
            # 1) Try per-ingredient overrides for realistic piece/slice weights
            grams = None
            for keyword, match_unit, grams_per in per_item_weights:
                if keyword in ingredient_name and unit == match_unit:
                    grams = quantity * grams_per
                    break

            # 2) Fall back to general unit conversions
            if grams is None:
                grams = quantity
                if unit in unit_conversions:
                    grams = quantity * unit_conversions[unit]
                elif unit == '':  # No unit specified, assume grams
                    grams = quantity
                else:
                    logger.debug(f"Unknown unit '{unit}' for ingredient '{ingredient_name}', assuming grams")
            
            # Calculate nutrition for this ingredient (per 100g)
            factor = grams / 100
            
            total_calories += matched_ingredient['calories'] * factor
            total_protein += matched_ingredient['protein'] * factor
            total_carbs += matched_ingredient['carbs'] * factor
            total_fat += matched_ingredient['fat'] * factor
            total_fiber += matched_ingredient['fiber'] * factor
            total_sugar += matched_ingredient['sugar'] * factor
        
        # Round to 1 decimal place
        return {
            "calories": round(total_calories, 1),
            "protein": round(total_protein, 1),
            "carbs": round(total_carbs, 1),
            "fat": round(total_fat, 1),
            "fiber": round(total_fiber, 1),
            "sugar": round(total_sugar, 1),
            "dietary_tags": _get_dietary_tags_from_nutrition(total_calories, total_protein, total_carbs),
            "success": True,
            "error": None
        }
        
    except Exception as e:
        logger.error(f"Error calculating nutrition from ingredients: {e}")
        return {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0,
            "fiber": 0,
            "sugar": 0,
            "dietary_tags": [],
            "success": False,
            "error": str(e)
        }

def _get_dietary_tags_from_nutrition(calories, protein, carbs):
    """Get dietary tags based on nutrition values"""
    tags = []
    
    if carbs < 20:
        tags.append('low-carb')
    if carbs < 10:
        tags.append('keto')
    if protein > 20:
        tags.append('high-protein')
    if calories < 300:
        tags.append('low-calorie')
    
    return tags

def get_nutrition_info_from_spoonacular(dish_name: str) -> Dict:
    """
    Get nutrition information for a dish from Spoonacular API
    
    Args:
        dish_name (str): Name of the dish to get nutrition for
        
    Returns:
        Dict: Nutrition information with the following structure:
        {
            "calories": float or "unknown",
            "protein": float or "unknown", 
            "carbs": float or "unknown",
            "fat": float or "unknown",
            "fiber": float or "unknown",
            "sugar": float or "unknown",
            "dietary_tags": List[str],
            "recipe_servings": int,  # Number of servings the nutrition data represents
            "success": bool,
            "error": str or None
        }
    """
    try:
        # First, search for the recipe to get its ID and servings info
        recipe_info = _get_recipe_info_from_spoonacular(dish_name)
        
        if not recipe_info:
            logger.warning(f"No recipe found for dish: {dish_name}")
            return _get_default_nutrition_response()
        
        recipe_id = recipe_info.get('id')
        recipe_servings = recipe_info.get('servings', 1)
        
        # Get nutrition information using the recipe ID
        nutrition_data = _get_recipe_nutrition_from_spoonacular(recipe_id)
        
        if not nutrition_data:
            logger.warning(f"No nutrition data found for recipe ID: {recipe_id}")
            return _get_default_nutrition_response()
        
        # Add recipe servings info to nutrition data
        nutrition_data['recipe_servings'] = recipe_servings
        
        return nutrition_data
        
    except Exception as e:
        logger.error(f"Error fetching nutrition for {dish_name}: {e}")
        return _get_default_nutrition_response(error=str(e))

def _get_recipe_info_from_spoonacular(dish_name: str) -> Optional[Dict]:
    """
    Search for a recipe and return its ID and servings info from Spoonacular API
    
    Args:
        dish_name (str): Name of the dish to search for
        
    Returns:
        Optional[Dict]: Recipe info with 'id' and 'servings' if found, None otherwise
    """
    try:
        url = f"{Config.SPOONACULAR_BASE_URL}/complexSearch"
        
        # Search parameters for Spoonacular API
        search_params = {
            'apiKey': Config.SPOONACULAR_API_KEY,
            'query': dish_name,
            'addRecipeInformation': True,
            'number': 1,  # We only need the first result
            'instructionsRequired': False,
            'fillIngredients': False  # We don't need ingredients for nutrition
        }
        
        # Add cuisine filters for better results
        dish_lower = dish_name.lower()
        if any(keyword in dish_lower for keyword in ['rice', 'biryani', 'pulao', 'curry', 'masala']):
            search_params['cuisine'] = 'Asian'
        elif any(keyword in dish_lower for keyword in ['pasta', 'spaghetti', 'lasagna', 'risotto']):
            search_params['cuisine'] = 'Italian'
        elif any(keyword in dish_lower for keyword in ['taco', 'burrito', 'enchilada', 'quesadilla']):
            search_params['cuisine'] = 'Mexican'
        elif any(keyword in dish_lower for keyword in ['sushi', 'ramen', 'tempura', 'teriyaki']):
            search_params['cuisine'] = 'Japanese'
        elif any(keyword in dish_lower for keyword in ['kebab', 'falafel', 'hummus', 'shawarma']):
            search_params['cuisine'] = 'Middle Eastern'
        
        logger.info(f"Searching for recipe info: {dish_name}")
        response = requests.get(url, params=search_params, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            if results and len(results) > 0:
                recipe = results[0]
                recipe_id = recipe.get('id')
                recipe_servings = recipe.get('servings', 1)
                logger.info(f"Found recipe ID: {recipe_id} with {recipe_servings} servings for dish: {dish_name}")
                return {
                    'id': recipe_id,
                    'servings': recipe_servings
                }
        
        logger.warning(f"No recipe info found for dish: {dish_name}")
        return None
        
    except Exception as e:
        logger.error(f"Error searching for recipe info: {e}")
        return None

def _get_recipe_nutrition_from_spoonacular(recipe_id: int) -> Optional[Dict]:
    """
    Get nutrition information for a specific recipe ID from Spoonacular API
    
    Args:
        recipe_id (int): Spoonacular recipe ID
        
    Returns:
        Optional[Dict]: Nutrition information if found, None otherwise
    """
    try:
        # Try the nutrition widget endpoint first (more detailed)
        url = f"{Config.SPOONACULAR_BASE_URL}/{recipe_id}/nutritionWidget.json"
        
        params = {
            'apiKey': Config.SPOONACULAR_API_KEY
        }
        
        logger.info(f"Fetching nutrition for recipe ID: {recipe_id}")
        response = requests.get(url, params=params, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            return _parse_nutrition_widget_data(data)
        
        # If nutrition widget fails, try the guess nutrition endpoint
        logger.info(f"Nutrition widget failed, trying guess nutrition for recipe ID: {recipe_id}")
        return _get_guess_nutrition_from_spoonacular(recipe_id)
        
    except Exception as e:
        logger.error(f"Error fetching nutrition for recipe ID {recipe_id}: {e}")
        return None

def _get_guess_nutrition_from_spoonacular(recipe_id: int) -> Optional[Dict]:
    """
    Get nutrition information using the guess nutrition endpoint
    
    Args:
        recipe_id (int): Spoonacular recipe ID
        
    Returns:
        Optional[Dict]: Nutrition information if found, None otherwise
    """
    try:
        url = f"{Config.SPOONACULAR_BASE_URL}/{recipe_id}/guessNutrition"
        
        params = {
            'apiKey': Config.SPOONACULAR_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            return _parse_guess_nutrition_data(data)
        
        return None
        
    except Exception as e:
        logger.error(f"Error fetching guess nutrition for recipe ID {recipe_id}: {e}")
        return None

def _parse_nutrition_widget_data(data: Dict) -> Dict:
    """
    Parse nutrition data from the nutrition widget endpoint
    
    Args:
        data (Dict): Raw nutrition widget data from Spoonacular
        
    Returns:
        Dict: Parsed nutrition information
    """
    try:
        # Extract nutrition values
        calories = _extract_numeric_value(data.get('calories', ''))
        protein = _extract_numeric_value(data.get('protein', ''))
        carbs = _extract_numeric_value(data.get('carbs', ''))
        fat = _extract_numeric_value(data.get('fat', ''))
        fiber = _extract_numeric_value(data.get('fiber', ''))
        sugar = _extract_numeric_value(data.get('sugar', ''))
        
        # Extract dietary tags
        dietary_tags = _extract_dietary_tags(data)
        
        return {
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "fiber": fiber,
            "sugar": sugar,
            "dietary_tags": dietary_tags,
            "success": True,
            "error": None
        }
        
    except Exception as e:
        logger.error(f"Error parsing nutrition widget data: {e}")
        return _get_default_nutrition_response(error=f"Failed to parse nutrition data: {e}")

def _parse_guess_nutrition_data(data: Dict) -> Dict:
    """
    Parse nutrition data from the guess nutrition endpoint
    
    Args:
        data (Dict): Raw guess nutrition data from Spoonacular
        
    Returns:
        Dict: Parsed nutrition information
    """
    try:
        # Extract nutrition values from guess nutrition response
        calories = _extract_numeric_value(data.get('calories', {}).get('value', ''))
        protein = _extract_numeric_value(data.get('protein', {}).get('value', ''))
        carbs = _extract_numeric_value(data.get('carbs', {}).get('value', ''))
        fat = _extract_numeric_value(data.get('fat', {}).get('value', ''))
        fiber = _extract_numeric_value(data.get('fiber', {}).get('value', ''))
        sugar = _extract_numeric_value(data.get('sugar', {}).get('value', ''))
        
        # Extract dietary tags
        dietary_tags = _extract_dietary_tags(data)
        
        return {
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "fiber": fiber,
            "sugar": sugar,
            "dietary_tags": dietary_tags,
            "success": True,
            "error": None
        }
        
    except Exception as e:
        logger.error(f"Error parsing guess nutrition data: {e}")
        return _get_default_nutrition_response(error=f"Failed to parse nutrition data: {e}")

def _extract_numeric_value(value: str):
    """
    Extract numeric value from a string that may contain units
    
    Args:
        value (str): String containing numeric value (e.g., "250 kcal", "15g")
        
    Returns:
        float or str: Extracted numeric value, or "unknown" if extraction fails
    """
    try:
        if not value or value == "unknown":
            return "unknown"
        
        # Remove common units and extract number
        import re
        # Match numbers (including decimals) followed by optional units
        match = re.search(r'(\d+(?:\.\d+)?)', str(value))
        
        if match:
            return float(match.group(1))
        else:
            return "unknown"
            
    except Exception as e:
        logger.error(f"Error extracting numeric value from '{value}': {e}")
        return "unknown"

def _extract_dietary_tags(data: Dict) -> List[str]:
    """
    Extract dietary tags from nutrition data
    
    Args:
        data (Dict): Nutrition data from Spoonacular
        
    Returns:
        List[str]: List of dietary tags
    """
    try:
        tags = []
        
        # Check for common dietary indicators in the data
        if data.get('vegetarian'):
            tags.append('vegetarian')
        if data.get('vegan'):
            tags.append('vegan')
        if data.get('glutenFree'):
            tags.append('gluten-free')
        if data.get('dairyFree'):
            tags.append('dairy-free')
        
        # Check for low-carb/keto indicators
        carbs = _extract_numeric_value(data.get('carbs', ''))
        if isinstance(carbs, (int, float)) and carbs < 20:
            tags.append('low-carb')
        if isinstance(carbs, (int, float)) and carbs < 10:
            tags.append('keto')
        
        # Check for high-protein indicators
        protein = _extract_numeric_value(data.get('protein', ''))
        if isinstance(protein, (int, float)) and protein > 20:
            tags.append('high-protein')
        
        # Check for low-calorie indicators
        calories = _extract_numeric_value(data.get('calories', ''))
        if isinstance(calories, (int, float)) and calories < 300:
            tags.append('low-calorie')
        
        return tags
        
    except Exception as e:
        logger.error(f"Error extracting dietary tags: {e}")
        return []

def _get_default_nutrition_response(error: str = None) -> Dict:
    """
    Get default nutrition response when data is not available
    
    Args:
        error (str): Error message if applicable
        
    Returns:
        Dict: Default nutrition response
    """
    return {
        "calories": "unknown",
        "protein": "unknown",
        "carbs": "unknown",
        "fat": "unknown",
        "fiber": "unknown",
        "sugar": "unknown",
        "dietary_tags": [],
        "recipe_servings": 1,
        "success": False,
        "error": error or "Nutrition data not available"
    }

def get_nutrition_info(dish_name: str, servings: int = 1, ingredients: List[Dict] = None) -> Dict:
    """
    Main function to get nutrition information for a dish
    This is the primary function to be called from other modules
    
    Args:
        dish_name (str): Name of the dish to get nutrition for
        servings (int): Number of servings (not used for scaling, handled by caller)
        ingredients (List[Dict]): List of ingredients to calculate nutrition from
        
    Returns:
        Dict: Clean JSON ready for frontend consumption
    """
    logger.info(f"Getting nutrition info for dish: {dish_name}")
    
    # If we have ingredients, use Spoonacular's ingredient nutrition endpoint (most accurate)
    if ingredients and len(ingredients) > 0:
        logger.info(f"Getting nutrition from Spoonacular for {len(ingredients)} ingredients for {dish_name}")
        logger.info(f"Ingredients: {ingredients}")
        
        # Try Spoonacular ingredient nutrition first (most accurate)
        nutrition_data = get_nutrition_from_spoonacular_ingredients(ingredients)
        
        # If Spoonacular fails, fall back to local calculation
        if not nutrition_data.get('success'):
            logger.info(f"Spoonacular ingredient nutrition failed, using local calculation for {dish_name}")
            logger.info(f"Local calculation ingredients: {ingredients}")
            nutrition_data = calculate_nutrition_from_ingredients(ingredients)
            logger.info(f"Local calculation result: {nutrition_data}")
        
        logger.info(f"Calculated nutrition: {nutrition_data}")
    else:
        # Fallback to Spoonacular recipe nutrition API
        logger.info(f"No ingredients provided, using Spoonacular recipe API for {dish_name}")
        nutrition_data = get_nutrition_info_from_spoonacular(dish_name)
    
    # Ensure we return clean JSON
    return {
        "success": nutrition_data.get("success", False),
        "nutrition": {
            "calories": nutrition_data.get("calories", "unknown"),
            "protein": nutrition_data.get("protein", "unknown"),
            "carbs": nutrition_data.get("carbs", "unknown"),
            "fat": nutrition_data.get("fat", "unknown"),
            "fiber": nutrition_data.get("fiber", "unknown"),
            "sugar": nutrition_data.get("sugar", "unknown"),
            "dietary_tags": nutrition_data.get("dietary_tags", [])
        },
        "error": nutrition_data.get("error")
    } 

def get_nutrition_from_spoonacular_ingredients(ingredients: List[Dict]) -> Dict:
    """
    Get nutrition information from Spoonacular's ingredient nutrition endpoint
    This is more accurate than our local database
    """
    try:
        # Normalize ingredients to realistic portion sizes
        normalized_ingredients = normalize_ingredients_for_realistic_servings(ingredients)
        
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        total_fiber = 0
        total_sugar = 0
        
        logger.info(f"Getting nutrition from Spoonacular for {len(normalized_ingredients)} normalized ingredients")
        
        for ingredient_data in normalized_ingredients:
            ingredient_name = ingredient_data.get('ingredient', '').lower()
            quantity = ingredient_data.get('quantity', 0)
            unit = ingredient_data.get('unit', 'g')
            
            # Convert to grams for Spoonacular API
            grams = _convert_to_grams(quantity, unit)
            
            if grams > 0:
                # Use Spoonacular's ingredient nutrition endpoint
                url = "https://api.spoonacular.com/food/ingredients/search"
                params = {
                    'query': ingredient_name,
                    'apiKey': Config.SPOONACULAR_API_KEY,
                    'number': 1
                }
                
                response = requests.get(url, params=params, timeout=2)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('results') and len(data['results']) > 0:
                        ingredient_id = data['results'][0]['id']
                        
                        # Get nutrition for this ingredient
                        nutrition_url = f"https://api.spoonacular.com/food/ingredients/{ingredient_id}/information"
                        nutrition_params = {
                            'amount': grams,
                            'unit': 'g',
                            'apiKey': Config.SPOONACULAR_API_KEY
                        }
                        
                        nutrition_response = requests.get(nutrition_url, params=nutrition_params, timeout=2)
                        
                        if nutrition_response.status_code == 200:
                            nutrition_data = nutrition_response.json()
                            nutrients = nutrition_data.get('nutrition', {}).get('nutrients', [])
                            
                            # Extract nutrition values
                            calories = next((n['amount'] for n in nutrients if n['name'] == 'Calories'), 0)
                            protein = next((n['amount'] for n in nutrients if n['name'] == 'Protein'), 0)
                            carbs = next((n['amount'] for n in nutrients if n['name'] == 'Carbohydrates'), 0)
                            fat = next((n['amount'] for n in nutrients if n['name'] == 'Total Fat'), 0)
                            fiber = next((n['amount'] for n in nutrients if n['name'] == 'Fiber'), 0)
                            sugar = next((n['amount'] for n in nutrients if n['name'] == 'Sugar'), 0)
                            
                            total_calories += calories
                            total_protein += protein
                            total_carbs += carbs
                            total_fat += fat
                            total_fiber += fiber
                            total_sugar += sugar
                            
                            logger.info(f"✅ Got nutrition for {ingredient_name}: {calories} cal, {protein}g protein")
                        else:
                            logger.warning(f"❌ Failed to get nutrition for {ingredient_name}")
                    else:
                        logger.warning(f"❌ No ingredient found for {ingredient_name}")
                else:
                    logger.warning(f"❌ Failed to search for {ingredient_name}")
        
        # Generate dietary tags
        dietary_tags = _get_dietary_tags_from_nutrition(total_calories, total_protein, total_carbs)
        
        # Check if we got any nutrition data
        if total_calories == 0 and total_protein == 0 and total_carbs == 0:
            logger.warning("❌ All Spoonacular API calls failed, returning failure response")
            return {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0,
                'fiber': 0,
                'sugar': 0,
                'dietary_tags': [],
                'success': False,
                'error': 'All Spoonacular API calls failed'
            }
        
        return {
            'calories': round(total_calories, 1),
            'protein': round(total_protein, 1),
            'carbs': round(total_carbs, 1),
            'fat': round(total_fat, 1),
            'fiber': round(total_fiber, 1),
            'sugar': round(total_sugar, 1),
            'dietary_tags': dietary_tags,
            'success': True,
            'error': None
        }
        
    except Exception as e:
        logger.error(f"Error getting nutrition from Spoonacular ingredients: {e}")
        return {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'fiber': 0,
            'sugar': 0,
            'dietary_tags': [],
            'success': False,
            'error': str(e)
        }

def _convert_to_grams(quantity: float, unit: str) -> float:
    """
    Convert various units to grams for Spoonacular API
    """
    unit_lower = unit.lower()
    
    if unit_lower in ['g', 'gram', 'grams']:
        return quantity
    elif unit_lower in ['kg', 'kilogram', 'kilograms']:
        return quantity * 1000
    elif unit_lower in ['oz', 'ounce', 'ounces']:
        return quantity * 28.35
    elif unit_lower in ['lb', 'pound', 'pounds']:
        return quantity * 453.6
    elif unit_lower in ['cup', 'cups']:
        return quantity * 240  # Approximate
    elif unit_lower in ['tbsp', 'tablespoon', 'tablespoons']:
        return quantity * 15
    elif unit_lower in ['tsp', 'teaspoon', 'teaspoons']:
        return quantity * 5
    elif unit_lower in ['ml', 'milliliter', 'milliliters']:
        return quantity
    elif unit_lower in ['l', 'liter', 'liters']:
        return quantity * 1000
    else:
        # Default assumption: 1 unit = 1 gram
        return quantity 