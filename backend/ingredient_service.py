import re
import requests
import logging
from typing import List, Dict, Optional, Tuple
from config import Config

# Configure logging
logger = logging.getLogger(__name__)

# Mock data for popular dishes
POPULAR_DISHES = {
    'chicken parmesan': {
        'ingredients': [
            {'ingredient': 'Chicken breast', 'quantity': 2, 'unit': 'pounds'},
            {'ingredient': 'Italian dressing', 'quantity': 0.5, 'unit': 'cup'},
            {'ingredient': 'Breadcrumbs', 'quantity': 1, 'unit': 'cup'},
            {'ingredient': 'Garlic powder', 'quantity': 2, 'unit': 'teaspoons'},
            {'ingredient': 'Italian seasoning', 'quantity': 1, 'unit': 'teaspoon'},
            {'ingredient': 'Salt', 'quantity': 0.5, 'unit': 'teaspoon'},
            {'ingredient': 'Black pepper', 'quantity': 0.5, 'unit': 'teaspoon'},
            {'ingredient': 'Mozzarella cheese', 'quantity': 0.5, 'unit': 'cup'},
            {'ingredient': 'Parmesan cheese', 'quantity': 0.25, 'unit': 'cup'},
            {'ingredient': 'Marinara sauce', 'quantity': 1.5, 'unit': 'cups'},
            {'ingredient': 'Spaghetti', 'quantity': 1, 'unit': 'pound'}
        ]
    },
    'chicken tikka masala': {
        'ingredients': [
            {'ingredient': 'Chicken breast', 'quantity': 1.5, 'unit': 'pounds'},
            {'ingredient': 'Yogurt', 'quantity': 1, 'unit': 'cup'},
            {'ingredient': 'Garam masala', 'quantity': 2, 'unit': 'teaspoons'},
            {'ingredient': 'Turmeric powder', 'quantity': 1, 'unit': 'teaspoon'},
            {'ingredient': 'Cumin powder', 'quantity': 1, 'unit': 'teaspoon'},
            {'ingredient': 'Coriander powder', 'quantity': 1, 'unit': 'teaspoon'},
            {'ingredient': 'Red chili powder', 'quantity': 1, 'unit': 'teaspoon'},
            {'ingredient': 'Ginger paste', 'quantity': 2, 'unit': 'teaspoons'},
            {'ingredient': 'Garlic paste', 'quantity': 2, 'unit': 'teaspoons'},
            {'ingredient': 'Tomato puree', 'quantity': 2, 'unit': 'cups'},
            {'ingredient': 'Heavy cream', 'quantity': 1, 'unit': 'cup'},
            {'ingredient': 'Butter', 'quantity': 4, 'unit': 'tablespoons'},
            {'ingredient': 'Kasoori methi', 'quantity': 1, 'unit': 'teaspoon'},
            {'ingredient': 'Salt', 'quantity': 1, 'unit': 'teaspoon'},
            {'ingredient': 'Black pepper', 'quantity': 0.5, 'unit': 'teaspoon'},
            {'ingredient': 'Lemon juice', 'quantity': 2, 'unit': 'tablespoons'},
            {'ingredient': 'Cooking oil', 'quantity': 2, 'unit': 'tablespoons'}
        ]
    },
    'beef lasagna': {
        'ingredients': [
            {'ingredient': 'Lasagna noodles', 'quantity': 12, 'unit': 'pieces'},
            {'ingredient': 'Ground beef', 'quantity': 1, 'unit': 'pound'},
            {'ingredient': 'Onion', 'quantity': 1, 'unit': 'medium'},
            {'ingredient': 'Garlic', 'quantity': 3, 'unit': 'cloves'},
            {'ingredient': 'Tomato sauce', 'quantity': 2, 'unit': 'cups'},
            {'ingredient': 'Ricotta cheese', 'quantity': 1, 'unit': 'cup'},
            {'ingredient': 'Mozzarella cheese', 'quantity': 2, 'unit': 'cups'},
            {'ingredient': 'Parmesan cheese', 'quantity': 0.5, 'unit': 'cup'},
            {'ingredient': 'Egg', 'quantity': 1, 'unit': 'piece'},
            {'ingredient': 'Italian seasoning', 'quantity': 1, 'unit': 'teaspoon'},
            {'ingredient': 'Salt', 'quantity': 1, 'unit': 'teaspoon'},
            {'ingredient': 'Black pepper', 'quantity': 0.5, 'unit': 'teaspoon'},
            {'ingredient': 'Olive oil', 'quantity': 2, 'unit': 'tablespoons'}
        ]
    },
    'hyderabadi biryani': {
        'ingredients': [
            {'ingredient': 'Basmati rice', 'quantity': 200, 'unit': 'g'},
            {'ingredient': 'Bone-in mutton', 'quantity': 250, 'unit': 'g'},
            {'ingredient': 'Yogurt', 'quantity': 100, 'unit': 'g'},
            {'ingredient': 'Fried onions', 'quantity': 50, 'unit': 'g'},
            {'ingredient': 'Ginger-garlic paste', 'quantity': 1, 'unit': 'tbsp'},
            {'ingredient': 'Green chilies', 'quantity': 2, 'unit': 'pieces'},
            {'ingredient': 'Mint leaves', 'quantity': 10, 'unit': 'leaves'},
            {'ingredient': 'Coriander leaves', 'quantity': 10, 'unit': 'leaves'},
            {'ingredient': 'Lemon juice', 'quantity': 1, 'unit': 'tbsp'},
            {'ingredient': 'Biryani masala', 'quantity': 1, 'unit': 'tbsp'},
            {'ingredient': 'Saffron milk', 'quantity': 2, 'unit': 'tbsp'},
            {'ingredient': 'Ghee', 'quantity': 2, 'unit': 'tbsp'},
            {'ingredient': 'Salt', 'quantity': 1, 'unit': 'tsp'}
        ]
    },
    'kolkata biryani': {
        'ingredients': [
            {'ingredient': 'Basmati rice', 'quantity': 200, 'unit': 'g'},
            {'ingredient': 'Mutton (bone-in)', 'quantity': 250, 'unit': 'g'},
            {'ingredient': 'Potato (large)', 'quantity': 1, 'unit': 'piece'},
            {'ingredient': 'Boiled egg', 'quantity': 1, 'unit': 'piece'},
            {'ingredient': 'Yogurt', 'quantity': 75, 'unit': 'g'},
            {'ingredient': 'Ginger-garlic paste', 'quantity': 1, 'unit': 'tbsp'},
            {'ingredient': 'Biryani masala', 'quantity': 1, 'unit': 'tbsp'},
            {'ingredient': 'Kewra water', 'quantity': 1, 'unit': 'tsp'},
            {'ingredient': 'Rose water', 'quantity': 1, 'unit': 'tsp'},
            {'ingredient': 'Ghee', 'quantity': 2, 'unit': 'tbsp'},
            {'ingredient': 'Fried onions', 'quantity': 50, 'unit': 'g'},
            {'ingredient': 'Salt', 'quantity': 1, 'unit': 'tsp'}
        ]
    },
    'tiramisu': {
        'ingredients': [
            {'ingredient': 'Mascarpone cheese', 'quantity': 250, 'unit': 'g'},
            {'ingredient': 'Egg yolks', 'quantity': 3, 'unit': 'pieces'},
            {'ingredient': 'Sugar', 'quantity': 75, 'unit': 'g'},
            {'ingredient': 'Espresso coffee', 'quantity': 150, 'unit': 'ml'},
            {'ingredient': 'Ladyfinger biscuits (savoiardi)', 'quantity': 12, 'unit': 'pieces'},
            {'ingredient': 'Cocoa powder', 'quantity': 1, 'unit': 'tbsp'},
            {'ingredient': 'Whipping cream', 'quantity': 100, 'unit': 'ml'},
            {'ingredient': 'Rum or coffee liqueur (optional)', 'quantity': 1, 'unit': 'tbsp'}
        ]
    },
    'cheesecake': {
        'ingredients': [
            {'ingredient': 'Cream cheese', 'quantity': 400, 'unit': 'g'},
            {'ingredient': 'Sugar', 'quantity': 100, 'unit': 'g'},
            {'ingredient': 'Eggs', 'quantity': 2, 'unit': 'pieces'},
            {'ingredient': 'Vanilla extract', 'quantity': 1, 'unit': 'tsp'},
            {'ingredient': 'Graham cracker crumbs', 'quantity': 150, 'unit': 'g'},
            {'ingredient': 'Butter (melted)', 'quantity': 75, 'unit': 'g'},
            {'ingredient': 'Sour cream', 'quantity': 100, 'unit': 'g'}
        ]
    },
    'baklava': {
        'ingredients': [
            {'ingredient': 'Phyllo dough sheets', 'quantity': 12, 'unit': 'sheets'},
            {'ingredient': 'Chopped walnuts or pistachios', 'quantity': 200, 'unit': 'g'},
            {'ingredient': 'Butter (melted)', 'quantity': 150, 'unit': 'g'},
            {'ingredient': 'Sugar', 'quantity': 100, 'unit': 'g'},
            {'ingredient': 'Honey', 'quantity': 150, 'unit': 'ml'},
            {'ingredient': 'Lemon juice', 'quantity': 1, 'unit': 'tbsp'},
            {'ingredient': 'Cinnamon', 'quantity': 0.5, 'unit': 'tsp'},
            {'ingredient': 'Water', 'quantity': 100, 'unit': 'ml'}
        ]
    },
    'mochi ice cream': {
        'ingredients': [
            {'ingredient': 'Glutinous rice flour (mochiko)', 'quantity': 100, 'unit': 'g'},
            {'ingredient': 'Sugar', 'quantity': 50, 'unit': 'g'},
            {'ingredient': 'Water', 'quantity': 150, 'unit': 'ml'},
            {'ingredient': 'Cornstarch (for dusting)', 'quantity': 2, 'unit': 'tbsp'},
            {'ingredient': 'Ice cream (any flavor)', 'quantity': 6, 'unit': 'scoops'}
        ]
    }
}

# Mock data for pizza varieties
PIZZA_RECIPES = {
    'margherita': {
        'ingredients': [
            {'ingredient': 'Pizza dough', 'quantity': 250, 'unit': 'g'},
            {'ingredient': 'Crushed tomatoes', 'quantity': 80, 'unit': 'g'},
            {'ingredient': 'Mozzarella (fresh)', 'quantity': 80, 'unit': 'g'},
            {'ingredient': 'Basil leaves', 'quantity': 4, 'unit': 'pcs'},
            {'ingredient': 'Olive oil', 'quantity': 1, 'unit': 'tbsp'}
        ]
    },
    'marinara': {
        'ingredients': [
            {'ingredient': 'Pizza dough', 'quantity': 250, 'unit': 'g'},
            {'ingredient': 'Tomato sauce', 'quantity': 100, 'unit': 'g'},
            {'ingredient': 'Garlic (sliced)', 'quantity': 2, 'unit': 'cloves'},
            {'ingredient': 'Oregano', 'quantity': 0.5, 'unit': 'tsp'},
            {'ingredient': 'Olive oil', 'quantity': 1, 'unit': 'tbsp'}
        ]
    },
    'pepperoni': {
        'ingredients': [
            {'ingredient': 'Pizza dough', 'quantity': 250, 'unit': 'g'},
            {'ingredient': 'Pepperoni slices', 'quantity': 20, 'unit': 'slices'},
            {'ingredient': 'Mozzarella cheese', 'quantity': 80, 'unit': 'g'},
            {'ingredient': 'Tomato sauce', 'quantity': 100, 'unit': 'g'},
            {'ingredient': 'Olive oil', 'quantity': 1, 'unit': 'tbsp'},
            {'ingredient': 'Oregano', 'quantity': 1, 'unit': 'tsp'},
            {'ingredient': 'Red pepper flakes', 'quantity': 0.5, 'unit': 'tsp'}
        ]
    },
    'hawaiian': {
        'ingredients': [
            {'ingredient': 'Pizza dough', 'quantity': 250, 'unit': 'g'},
            {'ingredient': 'Tomato sauce', 'quantity': 100, 'unit': 'g'},
            {'ingredient': 'Mozzarella', 'quantity': 80, 'unit': 'g'},
            {'ingredient': 'Pineapple chunks', 'quantity': 80, 'unit': 'g'},
            {'ingredient': 'Ham or bacon', 'quantity': 60, 'unit': 'g'}
        ]
    }
}

# Mock data for burger varieties
BURGER_RECIPES = {
    'classic beef burger': {
        'ingredients': [
            {'ingredient': 'Ground beef (80/20)', 'quantity': 150, 'unit': 'g'},
            {'ingredient': 'Burger bun', 'quantity': 1, 'unit': 'medium'},
            {'ingredient': 'Cheddar cheese slice', 'quantity': 1, 'unit': 'slice'},
            {'ingredient': 'Lettuce', 'quantity': 1, 'unit': 'leaf'},
            {'ingredient': 'Tomato', 'quantity': 2, 'unit': 'slices'},
            {'ingredient': 'Onion', 'quantity': 2, 'unit': 'rings'},
            {'ingredient': 'Pickles', 'quantity': 2, 'unit': 'slices'},
            {'ingredient': 'Ketchup', 'quantity': 1, 'unit': 'tbsp'},
            {'ingredient': 'Mustard', 'quantity': 1, 'unit': 'tsp'},
            {'ingredient': 'Salt', 'quantity': 0.5, 'unit': 'tsp'},
            {'ingredient': 'Black pepper', 'quantity': 0.25, 'unit': 'tsp'}
        ]
    },
    'chicken burger': {
        'ingredients': [
            {'ingredient': 'Chicken breast patty', 'quantity': 150, 'unit': 'g'},
            {'ingredient': 'Burger bun', 'quantity': 1, 'unit': 'bun'},
            {'ingredient': 'Lettuce', 'quantity': 1, 'unit': 'leaf'},
            {'ingredient': 'Tomato', 'quantity': 2, 'unit': 'slices'},
            {'ingredient': 'Mayo', 'quantity': 1, 'unit': 'tbsp'},
            {'ingredient': 'Pickles', 'quantity': 2, 'unit': 'slices'},
            {'ingredient': 'Salt', 'quantity': 1, 'unit': 'pinch'},
            {'ingredient': 'Black pepper', 'quantity': 1, 'unit': 'pinch'}
        ]
    }
}

# Mock data for pasta dishes
PASTA_RECIPES = {
    'spaghetti carbonara': {
        'ingredients': [
            {'ingredient': 'Spaghetti pasta', 'quantity': 1, 'unit': 'pound'},
            {'ingredient': 'Eggs', 'quantity': 4, 'unit': 'large'},
            {'ingredient': 'Parmesan cheese', 'quantity': 1, 'unit': 'cup'},
            {'ingredient': 'Pancetta', 'quantity': 8, 'unit': 'ounces'},
            {'ingredient': 'Black pepper', 'quantity': 1, 'unit': 'teaspoon'},
            {'ingredient': 'Salt', 'quantity': 1, 'unit': 'teaspoon'},
            {'ingredient': 'Olive oil', 'quantity': 2, 'unit': 'tablespoons'}
        ]
    },
    'linguine marinara': {
        'ingredients': [
            {'ingredient': 'Linguine pasta', 'quantity': 1, 'unit': 'pound'},
            {'ingredient': 'Tomato sauce', 'quantity': 2, 'unit': 'cups'},
            {'ingredient': 'Olive oil', 'quantity': 3, 'unit': 'tablespoons'},
            {'ingredient': 'Garlic', 'quantity': 4, 'unit': 'cloves'},
            {'ingredient': 'Fresh basil', 'quantity': 0.25, 'unit': 'cup'},
            {'ingredient': 'Parmesan cheese', 'quantity': 0.5, 'unit': 'cup'},
            {'ingredient': 'Salt', 'quantity': 1, 'unit': 'teaspoon'},
            {'ingredient': 'Black pepper', 'quantity': 0.5, 'unit': 'teaspoon'},
            {'ingredient': 'Red pepper flakes', 'quantity': 0.25, 'unit': 'teaspoon'}
        ]
    }
}

def extract_dish_type(dish_name):
    """Extract dish type from dish name for better categorization"""
    dish_lower = dish_name.lower()
    
    if any(keyword in dish_lower for keyword in ['pizza', 'margherita', 'pepperoni']):
        return 'pizza'
    elif any(keyword in dish_lower for keyword in ['ice cream', 'icecream', 'gelato']):
        return 'ice_cream'
    elif any(keyword in dish_lower for keyword in ['cake', 'birthday', 'chocolate cake']):
        return 'cake'
    elif any(keyword in dish_lower for keyword in ['pasta', 'spaghetti', 'lasagna']):
        return 'pasta'
    elif any(keyword in dish_lower for keyword in ['salad', 'caesar', 'greek']):
        return 'salad'
    elif any(keyword in dish_lower for keyword in ['soup', 'broth', 'bisque']):
        return 'soup'
    else:
        return 'general'

def validate_recipe_relevance(recipe_title, dish_name):
    """Validate if a recipe is relevant to the requested dish"""
    title_lower = recipe_title.lower()
    dish_lower = dish_name.lower()
    
    # Exact match gets highest score
    if dish_lower in title_lower:
        return True
    
    # Check for key words
    dish_words = dish_lower.split()
    title_words = title_lower.split()
    
    # Count matching words
    matches = sum(1 for word in dish_words if word in title_words)
    return matches >= len(dish_words) * 0.5

def clean_dish_name(dish_name):
    """Clean and standardize dish name"""
    # Remove common prefixes/suffixes
    prefixes = ['recipe for', 'how to make', 'authentic', 'traditional', 'homemade']
    suffixes = ['recipe', 'dish', 'food', 'meal']
    
    cleaned = dish_name.lower().strip()
    
    for prefix in prefixes:
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
    
    for suffix in suffixes:
        if cleaned.endswith(suffix):
            cleaned = cleaned[:-len(suffix)].strip()
    
    return cleaned

def clean_ingredient_name(ingredient_name):
    """Clean ingredient name by removing extra text and formatting"""
    if not ingredient_name:
        return ""
    
    # Remove asterisks and special characters
    cleaned = ingredient_name.replace('*', '').strip()
    
    # Fix truncated ingredient names from TheMealDB
    ingredient_mapping = {
        'p': 'Pork',
        'c': 'Coriander',
        'w': 'Worcestershire Sauce',
        'starch': 'Cornstarch',
        'flour': 'All-Purpose Flour',
        'oil': 'Vegetable Oil',
        'salt': 'Salt',
        'sugar': 'Sugar',
        'vinegar': 'Rice Vinegar',
        'soy': 'Soy Sauce',
        'tomato': 'Tomato Puree',
        'egg': 'Egg',
        'water': 'Water'
    }
    
    # Check if the ingredient is a single letter or very short
    if len(cleaned) <= 2:
        cleaned_lower = cleaned.lower()
        if cleaned_lower in ingredient_mapping:
            return ingredient_mapping[cleaned_lower]
    
    # Remove common instruction words
    instruction_words = [
        'fresh', 'chopped', 'minced', 'diced', 'sliced', 'grated', 'crushed', 'ground',
        'whole', 'dried', 'frozen', 'canned', 'organic', 'extra virgin', 'virgin',
        'kosher', 'sea', 'table', 'black', 'white', 'brown', 'granulated', 'powdered',
        'large', 'medium', 'small', 'jumbo', 'extra large',
        'ripe', 'firm', 'soft', 'hard', 'crisp', 'tender',
        'optional', 'to taste', 'as needed', 'for garnish', 'for serving'
    ]
    
    # Remove measurement prefixes
    measurement_prefixes = [
        'tbsp.', 'tbsp', 'tablespoon', 'tablespoons',
        'tsp.', 'tsp', 'teaspoon', 'teaspoons',
        'cup', 'cups', 'oz.', 'oz', 'ounce', 'ounces',
        'lb.', 'lb', 'pound', 'pounds', 'g.', 'g', 'gram', 'grams'
    ]
    
    # Split by common separators and take the main ingredient
    separators = [',', ';', '(', ')', '-', 'or', 'and', 'plus']
    parts = cleaned
    for sep in separators:
        if sep in parts:
            parts = parts.split(sep)[0].strip()
    
    # Remove instruction words and measurement prefixes
    words = parts.split()
    if words:
        while words and len(words) > 1 and any(word.lower() in instruction_words + measurement_prefixes for word in words[:3]):
            words.pop(0)
        
        while words and len(words) > 1 and any(word.lower() in instruction_words + measurement_prefixes for word in words[-3:]):
            words.pop()
    
    cleaned = ' '.join(words).strip()
    
    # Check for truncated names again after cleaning
    if len(cleaned) <= 2:
        cleaned_lower = cleaned.lower()
        if cleaned_lower in ingredient_mapping:
            return ingredient_mapping[cleaned_lower]
    
    # Capitalize properly
    if cleaned:
        cleaned = cleaned.title()
    
    return cleaned

def get_recipe_ingredients_from_spoonacular_improved(dish_name):
    """Get ingredients from Spoonacular API (simplified version)"""
    try:
        logger.info(f"🔍 Searching Spoonacular for: {dish_name}")
        
        url = f"{Config.SPOONACULAR_BASE_URL}/complexSearch"
        search_params = {
            'query': dish_name,
            'addRecipeInformation': True,
            'fillIngredients': True,
            'number': 5,
            'apiKey': Config.SPOONACULAR_API_KEY
        }
        
        response = requests.get(url, params=search_params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            if results:
                recipe = results[0]
                ingredients = []
                
                for ingredient in recipe.get('extendedIngredients', []):
                    raw_name = ingredient.get('original', ingredient.get('name', ''))
                    cleaned_name = clean_ingredient_name(raw_name)
                    
                    if cleaned_name:
                        ingredients.append({
                            'ingredient': cleaned_name,
                            'quantity': ingredient.get('amount', 1),
                            'unit': ingredient.get('unit', '')
                        })
                
                logger.info(f"✅ Found {len(ingredients)} ingredients from Spoonacular")
                return ingredients
        
        logger.warning(f"❌ No ingredients found in Spoonacular for: {dish_name}")
        return []
        
    except Exception as e:
        logger.error(f"Error fetching ingredients from Spoonacular: {e}")
        return []

def get_ingredients_from_themealdb(dish_name):
    """Get ingredients from TheMealDB API"""
    try:
        logger.info(f"🔍 Searching TheMealDB for: {dish_name}")
        
        search_url = "https://www.themealdb.com/api/json/v1/1/search.php"
        search_params = {'s': dish_name}
        
        response = requests.get(search_url, params=search_params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            meals = data.get('meals', [])
            
            if meals and len(meals) > 0:
                # Process only the first meal to avoid duplicates
                meal = meals[0]
                meal_id = meal.get('idMeal')
                
                detail_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php"
                detail_params = {'i': meal_id}
                
                detail_response = requests.get(detail_url, params=detail_params, timeout=15)
                
                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    meal_details = detail_data.get('meals', [])
                    
                    if meal_details and len(meal_details) > 0:
                        meal_detail = meal_details[0]
                        ingredients = []
                        
                        # Track seen ingredients to avoid duplicates
                        seen_ingredients = set()
                        
                        for i in range(1, 21):
                            ingredient_key = f'strIngredient{i}'
                            measure_key = f'strMeasure{i}'
                            
                            ingredient = meal_detail.get(ingredient_key, '').strip()
                            measure = meal_detail.get(measure_key, '').strip()
                            
                            if ingredient and ingredient.lower() not in ['', 'null', 'none']:
                                cleaned_ingredient = clean_ingredient_name(ingredient)
                                
                                # Skip if we've already seen this ingredient
                                if cleaned_ingredient.lower() in seen_ingredients:
                                    continue
                    
                                if cleaned_ingredient:
                                    quantity = 1
                                    unit = ''
                                    
                                    if measure:
                                        # Parse quantity and unit from measure
                                        import re
                                        
                                        # Extract numbers (including fractions)
                                        quantity_match = re.search(r'(\d+(?:\/\d+)?(?:\.\d+)?)', measure)
                                        if quantity_match:
                                            quantity_str = quantity_match.group(1)
                                            if '/' in quantity_str:
                                                # Handle fractions like "1/2"
                                                num, denom = quantity_str.split('/')
                                                quantity = float(num) / float(denom)
                                            else:
                                                quantity = float(quantity_str)
                                        else:
                                            quantity = 1
                                        
                                        # Extract unit with better logic
                                        measure_lower = measure.lower()
                                        
                                        # Remove the quantity from the measure to get clean unit
                                        clean_measure = re.sub(r'\d+(?:\/\d+)?(?:\.\d+)?', '', measure_lower).strip()
                                        
                                        # Smart unit detection with ingredient context - prioritize slice/piece first
                                        if 'slice' in clean_measure:
                                            unit = 'slice'
                                        elif 'piece' in clean_measure or 'pc' in clean_measure:
                                            unit = 'piece'
                                        elif 'cup' in clean_measure:
                                            unit = 'cup'
                                        elif 'tbsp' in clean_measure or 'tablespoon' in clean_measure:
                                            unit = 'tablespoon'
                                        elif 'tsp' in clean_measure or 'teaspoon' in clean_measure:
                                            unit = 'teaspoon'
                                        elif 'oz' in clean_measure or 'ounce' in clean_measure:
                                            unit = 'ounce'
                                        elif 'lb' in clean_measure or 'pound' in clean_measure:
                                            unit = 'pound'
                                        elif 'g' in clean_measure or 'gram' in clean_measure:
                                            unit = 'gram'
                                        elif 'kg' in clean_measure or 'kilogram' in clean_measure:
                                            unit = 'kilogram'
                                        elif 'clove' in clean_measure:
                                            unit = 'clove'
                                        elif 'bunch' in clean_measure:
                                            unit = 'bunch'
                                        elif 'sprig' in clean_measure:
                                            unit = 'sprig'
                                        elif 'pinch' in clean_measure:
                                            unit = 'pinch'
                                        elif 'dash' in clean_measure:
                                            unit = 'dash'
                                        # Now safely check milliliter/liter with word boundaries to avoid matching words like 'slice'
                                        elif re.search(r"\b(ml|milliliter|milliliters|millilitre|millilitres)\b", clean_measure):
                                            unit = 'milliliter'
                                        elif re.search(r"\b(l|liter|liters|litre|litres)\b", clean_measure):
                                            # Be more careful with liter - only use for actual liquids
                                            ingredient_lower = cleaned_ingredient.lower()
                                            if any(word in ingredient_lower for word in ['water', 'milk', 'juice', 'broth', 'stock']):
                                                unit = 'liter'
                                            else:
                                                # For dry ingredients, liter is likely a mistake - use piece instead
                                                unit = 'piece'
                                        else:
                                            # Default units based on ingredient type
                                            ingredient_lower = cleaned_ingredient.lower()
                                            if any(word in ingredient_lower for word in ['pork chop', 'chicken breast', 'beef steak', 'fish fillet']):
                                                unit = 'piece'  # Default to pieces for meat cuts
                                            elif any(word in ingredient_lower for word in ['meat', 'pork', 'beef', 'chicken', 'fish']) and quantity <= 10:
                                                unit = 'piece'  # If small number, likely pieces
                                            elif any(word in ingredient_lower for word in ['meat', 'pork', 'beef', 'chicken', 'fish']) and quantity > 10:
                                                unit = 'gram'  # If large number, likely grams
                                            elif any(word in ingredient_lower for word in ['sugar', 'salt', 'flour', 'breadcrumb']):
                                                unit = 'gram'  # Default to grams for dry ingredients
                                            elif any(word in ingredient_lower for word in ['oil', 'sauce', 'vinegar']):
                                                unit = 'tablespoon'  # Default to tablespoons for liquids
                                            elif any(word in ingredient_lower for word in ['herb', 'spice', 'seasoning']):
                                                unit = 'teaspoon'  # Default to teaspoons for spices
                                            elif 'egg' in ingredient_lower:
                                                unit = 'piece'  # Eggs are typically counted
                                            else:
                                                unit = 'piece'  # Generic default
                                    
                            ingredients.append({
                                'ingredient': cleaned_ingredient,
                                'quantity': quantity,
                                'unit': unit
                            })
                            
                            # Mark this ingredient as seen
                            seen_ingredients.add(cleaned_ingredient.lower())
                        
                        logger.info(f"✅ Found {len(ingredients)} ingredients from TheMealDB")
                return ingredients
        
        logger.warning(f"❌ No ingredients found in TheMealDB for: {dish_name}")
        return []
        
    except Exception as e:
        logger.error(f"Error fetching ingredients from TheMealDB: {e}")
        return []

def get_ingredients_by_dish_name(dish_name):
    """Get ingredients based on dish name"""
    logger.info(f"🔍 Getting ingredients for: {dish_name}")
    
    dish_name_lower = dish_name.lower()
    
    # DEBUG: Print available keys in POPULAR_DISHES
    logger.info(f"🔍 DEBUG: Available POPULAR_DISHES keys: {list(POPULAR_DISHES.keys())}")
    logger.info(f"🔍 DEBUG: Searching for: '{dish_name_lower}'")
    logger.info(f"🔍 DEBUG: Is '{dish_name_lower}' in POPULAR_DISHES? {dish_name_lower in POPULAR_DISHES}")
    
    # STEP 1: Check POPULAR_DISHES mock data first
    if dish_name_lower in POPULAR_DISHES:
        logger.info(f"🍽️ Using POPULAR_DISHES mock data for: {dish_name}")
        ingredients = POPULAR_DISHES[dish_name_lower]['ingredients']
        logger.info(f"✅ POPULAR_DISHES mock data: Found {len(ingredients)} ingredients for {dish_name}")
        return ingredients
    
    # STEP 2: Check PIZZA_RECIPES mock data
    if 'pizza' in dish_name_lower:
        logger.info(f"🍕 Checking PIZZA_RECIPES for: {dish_name}")
        if 'margherita' in dish_name_lower:
            ingredients = PIZZA_RECIPES['margherita']['ingredients']
        elif 'marinara' in dish_name_lower:
            ingredients = PIZZA_RECIPES['marinara']['ingredients']
        elif 'pepperoni' in dish_name_lower:
            ingredients = PIZZA_RECIPES['pepperoni']['ingredients']
        elif 'hawaiian' in dish_name_lower or 'pineapple' in dish_name_lower:
            ingredients = PIZZA_RECIPES['hawaiian']['ingredients']
        else:
            # Default to margherita
            ingredients = PIZZA_RECIPES['margherita']['ingredients']
        
        logger.info(f"✅ PIZZA_RECIPES mock data: Found {len(ingredients)} ingredients for {dish_name}")
        return ingredients
    
    # STEP 3: Check BURGER_RECIPES mock data
    if 'burger' in dish_name_lower:
        logger.info(f"🍔 Checking BURGER_RECIPES for: {dish_name}")
        if 'chicken' in dish_name_lower:
            ingredients = BURGER_RECIPES['chicken burger']['ingredients']
        else:
            # Default to classic beef burger
            ingredients = BURGER_RECIPES['classic beef burger']['ingredients']
        
        logger.info(f"✅ BURGER_RECIPES mock data: Found {len(ingredients)} ingredients for {dish_name}")
        return ingredients
    
    # STEP 4: Check PASTA_RECIPES mock data
    if any(keyword in dish_name_lower for keyword in ['pasta', 'spaghetti', 'linguine', 'fettuccine', 'penne']):
        logger.info(f"🍝 Checking PASTA_RECIPES for: {dish_name}")
        if 'carbonara' in dish_name_lower:
            ingredients = PASTA_RECIPES['spaghetti carbonara']['ingredients']
        elif 'marinara' in dish_name_lower:
            ingredients = PASTA_RECIPES['linguine marinara']['ingredients']
        else:
            # Default to carbonara
            ingredients = PASTA_RECIPES['spaghetti carbonara']['ingredients']
        
        logger.info(f"✅ PASTA_RECIPES mock data: Found {len(ingredients)} ingredients for {dish_name}")
        return ingredients
    
    # STEP 5: Try TheMealDB API
    try:
        themaldb_ingredients = get_ingredients_from_themealdb(dish_name)
        if themaldb_ingredients and len(themaldb_ingredients) > 0:
            # Deduplicate ingredients before returning
            unique_ingredients = deduplicate_ingredients(themaldb_ingredients)
            logger.info(f"✅ TheMealDB SUCCESS: Found {len(unique_ingredients)} unique ingredients for {dish_name}")
            return unique_ingredients
    except Exception as e:
        logger.error(f"❌ TheMealDB failed: {e}")
    
    # STEP 6: Try Spoonacular API
    try:
        spoonacular_ingredients = get_recipe_ingredients_from_spoonacular_improved(dish_name)
        if spoonacular_ingredients and len(spoonacular_ingredients) > 0:
            # Deduplicate ingredients before returning
            unique_ingredients = deduplicate_ingredients(spoonacular_ingredients)
            logger.info(f"✅ Spoonacular SUCCESS: Found {len(unique_ingredients)} unique ingredients for {dish_name}")
            return unique_ingredients
    except Exception as e:
        logger.error(f"❌ Spoonacular failed: {e}")
    
    # STEP 7: Return empty list if no ingredients found
    logger.warning(f"❌ No ingredients found for: {dish_name}")
    return []

def deduplicate_ingredients(ingredients):
    """Remove duplicate ingredients from a list"""
    seen_ingredients = set()
    unique_ingredients = []
    
    for ingredient in ingredients:
        ingredient_name = ingredient.get('ingredient', '').lower().strip()
        if ingredient_name and ingredient_name not in seen_ingredients:
            seen_ingredients.add(ingredient_name)
            unique_ingredients.append(ingredient)
    
    return unique_ingredients

def scale_api_ingredients(ingredients, original_servings, target_servings):
    """Scale ingredients based on serving size"""
    if original_servings <= 0:
        return ingredients
    
    scale_factor = target_servings / original_servings
    scaled_ingredients = []
    
    for ingredient in ingredients:
        name = ingredient.get('ingredient', 'Unknown ingredient')
        quantity = ingredient.get('quantity', 0)
        unit = ingredient.get('unit', '')
        
        if quantity is not None and isinstance(quantity, (int, float)):
            scaled_quantity = quantity * scale_factor
            if scaled_quantity >= 1:
                scaled_quantity = round(scaled_quantity, 1)
            else:
                scaled_quantity = round(scaled_quantity, 2)
        else:
            scaled_quantity = quantity
        
        scaled_ingredients.append({
            'ingredient': name,
            'quantity': scaled_quantity,
            'unit': unit
        })
    
    return scaled_ingredients 