import logging
from typing import List, Dict, Set
from sqlalchemy.orm import Session
from models import UserAllergy

# Set up logging
logger = logging.getLogger(__name__)

# Common allergens with their variations and related ingredients
COMMON_ALLERGENS = {
    "peanuts": {
        "keywords": ["peanut", "peanuts", "groundnut", "groundnuts", "arachis", "arachis hypogaea"],
        "related": ["peanut butter", "peanut oil", "peanut flour", "peanut protein"]
    },
    "tree nuts": {
        "keywords": ["almond", "almonds", "walnut", "walnuts", "cashew", "cashews", "pecan", "pecans", 
                    "pistachio", "pistachios", "hazelnut", "hazelnuts", "macadamia", "macadamias", 
                    "brazil nut", "brazil nuts", "pine nut", "pine nuts", "chestnut", "chestnuts"],
        "related": ["almond milk", "cashew milk", "walnut oil", "almond flour", "nut butter", "mixed nuts"]
    },
    "shellfish": {
        "keywords": ["shrimp", "prawn", "crab", "lobster", "crayfish", "crawfish", "oyster", "mussel", 
                    "clam", "scallop", "squid", "octopus", "calamari", "abalone", "conch"],
        "related": ["shrimp paste", "fish sauce", "seafood", "crustacean", "mollusk"]
    },
    "fish": {
        "keywords": ["fish", "salmon", "tuna", "cod", "halibut", "mackerel", "sardine", "anchovy", 
                    "trout", "bass", "perch", "tilapia", "swordfish", "mahi mahi"],
        "related": ["fish oil", "fish sauce", "fish stock", "fish broth", "seafood"]
    },
    "dairy": {
        "keywords": ["milk", "cheese", "mozzarella", "cheddar", "parmesan", "yogurt", "yoghurt", "cream", "butter", "whey", "casein", 
                    "lactose", "lactose", "curd", "ghee", "buttermilk"],
        "related": ["whole milk", "skim milk", "heavy cream", "sour cream", "cream cheese", "cottage cheese"]
    },
    "eggs": {
        "keywords": ["egg", "eggs", "egg white", "egg yolk", "albumin", "ovalbumin", "lysozyme"],
        "related": ["egg white", "egg yolk", "egg powder", "egg substitute"]
    },
    "soy": {
        "keywords": ["soy", "soya", "soybean", "soybeans", "tofu", "tempeh", "miso", "edamame", 
                    "soy sauce", "soy milk", "soy protein"],
        "related": ["soy sauce", "soy milk", "soy protein", "soy flour", "soy oil", "tofu"]
    },
    "wheat": {
        "keywords": ["wheat", "gluten", "flour", "bread", "pasta", "noodle", "couscous", "bulgur", 
                    "farro", "spelt", "kamut", "durum", "semolina"],
        "related": ["wheat flour", "all-purpose flour", "bread flour", "pasta", "noodles", "gluten"]
    },
    "sesame": {
        "keywords": ["sesame", "sesamum", "tahini", "sesame oil", "sesame seed", "sesame seeds"],
        "related": ["tahini", "sesame oil", "sesame seeds", "sesame paste"]
    }
}

# Alternative ingredients for common allergens
ALLERGEN_ALTERNATIVES = {
    'dairy': {
        'buttermilk': ['almond milk + lemon juice', 'soy milk + vinegar', 'coconut milk + lemon juice'],
        'butter': ['olive oil', 'coconut oil', 'avocado oil', 'vegan butter'],
        'milk': ['almond milk', 'soy milk', 'oat milk', 'coconut milk', 'rice milk'],
        'cream': ['coconut cream', 'cashew cream', 'almond cream', 'soy cream'],
        'cheese': ['nutritional yeast', 'vegan cheese', 'cashew cheese', 'tofu ricotta'],
        'mozzarella': ['vegan mozzarella', 'cashew mozzarella', 'tofu mozzarella', 'nutritional yeast'],
        'yogurt': ['coconut yogurt', 'almond yogurt', 'soy yogurt', 'cashew yogurt']
    },
    'eggs': {
        'eggs': ['flax eggs (1 tbsp ground flax + 3 tbsp water)', 'chia eggs (1 tbsp chia + 3 tbsp water)', 'banana (1/4 cup mashed)', 'applesauce (1/4 cup)', 'silken tofu (1/4 cup)'],
        'egg whites': ['aquafaba (chickpea water)', 'flax gel', 'chia gel']
    },
    'nuts': {
        'almonds': ['sunflower seeds', 'pumpkin seeds', 'sesame seeds'],
        'peanuts': ['sunflower seeds', 'pumpkin seeds', 'soy nuts'],
        'cashews': ['sunflower seeds', 'pumpkin seeds', 'pine nuts (if no pine allergy)'],
        'walnuts': ['sunflower seeds', 'pumpkin seeds', 'hemp seeds']
    },
    'gluten': {
        'wheat flour': ['almond flour', 'coconut flour', 'rice flour', 'quinoa flour', 'buckwheat flour'],
        'bread': ['gluten-free bread', 'rice cakes', 'corn tortillas'],
        'pasta': ['rice pasta', 'quinoa pasta', 'zucchini noodles', 'spaghetti squash']
    },
    'soy': {
        'soy sauce': ['coconut aminos', 'tamari (if gluten-free needed)', 'liquid aminos'],
        'tofu': ['tempeh (if no soy allergy)', 'seitan (if no gluten allergy)', 'chickpeas'],
        'soy milk': ['almond milk', 'oat milk', 'coconut milk', 'rice milk']
    }
}

def get_common_allergens() -> List[str]:
    """
    Get list of common allergens for the frontend
    
    Returns:
        List[str]: List of common allergen names
    """
    return list(COMMON_ALLERGENS.keys())

def get_user_allergies(db: Session, user_id: int) -> List[Dict]:
    """
    Get all allergies for a specific user
    
    Args:
        db (Session): Database session
        user_id (int): User ID
        
    Returns:
        List[Dict]: List of user allergies
    """
    try:
        allergies = db.query(UserAllergy).filter(UserAllergy.user_id == user_id).all()
        return [
            {
                "id": allergy.id,
                "allergy_name": allergy.allergy_name,
                "allergy_type": allergy.allergy_type,
                "created_at": allergy.created_at.isoformat()
            }
            for allergy in allergies
        ]
    except Exception as e:
        logger.error(f"Error fetching user allergies: {e}")
        return []

def add_user_allergy(db: Session, user_id: int, allergy_name: str, allergy_type: str = "custom") -> Dict:
    """
    Add a new allergy for a user
    
    Args:
        db (Session): Database session
        user_id (int): User ID
        allergy_name (str): Name of the allergy
        allergy_type (str): Type of allergy (common or custom)
        
    Returns:
        Dict: Result of the operation
    """
    try:
        # Check if allergy already exists for this user
        existing = db.query(UserAllergy).filter(
            UserAllergy.user_id == user_id,
            UserAllergy.allergy_name.ilike(allergy_name)
        ).first()
        
        if existing:
            return {
                "success": False,
                "error": f"Allergy '{allergy_name}' already exists for this user"
            }
        
        # Create new allergy
        new_allergy = UserAllergy(
            user_id=user_id,
            allergy_name=allergy_name.lower(),
            allergy_type=allergy_type
        )
        
        db.add(new_allergy)
        db.commit()
        db.refresh(new_allergy)
        
        return {
            "success": True,
            "allergy": {
                "id": new_allergy.id,
                "allergy_name": new_allergy.allergy_name,
                "allergy_type": new_allergy.allergy_type,
                "created_at": new_allergy.created_at.isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Error adding user allergy: {e}")
        db.rollback()
        return {
            "success": False,
            "error": f"Failed to add allergy: {str(e)}"
        }

def remove_user_allergy(db: Session, user_id: int, allergy_id: int) -> Dict:
    """
    Remove an allergy for a user
    
    Args:
        db (Session): Database session
        user_id (int): User ID
        allergy_id (int): Allergy ID to remove
        
    Returns:
        Dict: Result of the operation
    """
    try:
        allergy = db.query(UserAllergy).filter(
            UserAllergy.id == allergy_id,
            UserAllergy.user_id == user_id
        ).first()
        
        if not allergy:
            return {
                "success": False,
                "error": "Allergy not found"
            }
        
        db.delete(allergy)
        db.commit()
        
        return {
            "success": True,
            "message": f"Allergy '{allergy.allergy_name}' removed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error removing user allergy: {e}")
        db.rollback()
        return {
            "success": False,
            "error": f"Failed to remove allergy: {str(e)}"
        }

def check_ingredients_for_allergies(ingredients: List[Dict], user_allergies: List[str]) -> Dict:
    """
    Check if any ingredients match user allergies
    """
    try:
        found_allergens = []
        allergen_details = []
        user_allergies_lower = [allergy.lower() for allergy in user_allergies]
        
        logger.info(f"Checking {len(ingredients)} ingredients for allergies: {user_allergies_lower}")
        
        for ingredient in ingredients:
            ingredient_name = ingredient.get('ingredient', '').lower()
            logger.info(f"Checking ingredient: '{ingredient_name}'")
            
            for allergen_name, allergen_data in COMMON_ALLERGENS.items():
                if allergen_name in user_allergies_lower:
                    # Check keywords
                    for keyword in allergen_data['keywords']:
                        if keyword in ingredient_name:
                            logger.info(f"Found allergen '{allergen_name}' in ingredient '{ingredient_name}' via keyword '{keyword}'")
                            if allergen_name not in found_allergens:
                                found_allergens.append(allergen_name)
                            allergen_details.append({"allergen": allergen_name, "ingredient": ingredient.get('ingredient', ''), "type": "keyword_match"})
                            break
                    
                    # Check related ingredients
                    for related in allergen_data['related']:
                        if related in ingredient_name:
                            logger.info(f"Found allergen '{allergen_name}' in ingredient '{ingredient_name}' via related '{related}'")
                            if allergen_name not in found_allergens:
                                found_allergens.append(allergen_name)
                            allergen_details.append({"allergen": allergen_name, "ingredient": ingredient.get('ingredient', ''), "type": "related_match"})
                            break
            
            # Check custom allergies
            for custom_allergy in user_allergies_lower:
                if custom_allergy not in [a for a in COMMON_ALLERGENS.keys()]:
                    if custom_allergy in ingredient_name or ingredient_name in custom_allergy:
                        logger.info(f"Found custom allergen '{custom_allergy}' in ingredient '{ingredient_name}'")
                        if custom_allergy not in found_allergens:
                            found_allergens.append(custom_allergy)
                        allergen_details.append({"allergen": custom_allergy, "ingredient": ingredient.get('ingredient', ''), "type": "custom_match"})
        
        logger.info(f"Found allergens: {found_allergens}")
        logger.info(f"Allergen details: {allergen_details}")
        
        # Generate alternative suggestions
        alternative_suggestions = generate_alternative_suggestions(found_allergens, allergen_details)
        
        return {
            "has_allergens": len(found_allergens) > 0,
            "found_allergens": found_allergens,
            "allergen_details": allergen_details,
            "alternative_suggestions": alternative_suggestions,
            "warning_message": _generate_warning_message(found_allergens) if found_allergens else None
        }
    except Exception as e:
        logger.error(f"Error checking ingredients for allergies: {e}")
        return {"has_allergens": False, "found_allergens": [], "allergen_details": [], "alternative_suggestions": {}, "warning_message": None, "error": str(e)}

def _generate_warning_message(allergens: List[str]) -> str:
    """
    Generate a warning message for found allergens
    
    Args:
        allergens (List[str]): List of found allergens
        
    Returns:
        str: Warning message
    """
    if not allergens:
        return None
    
    if len(allergens) == 1:
        return f"⚠️ This dish contains {allergens[0]}, which is in your allergy profile."
    else:
        allergen_list = ", ".join(allergens[:-1]) + f" and {allergens[-1]}"
        return f"⚠️ This dish contains {allergen_list}, which are in your allergy profile."

def validate_allergy_name(allergy_name: str) -> Dict:
    """
    Validate an allergy name
    
    Args:
        allergy_name (str): Allergy name to validate
        
    Returns:
        Dict: Validation result
    """
    if not allergy_name or not allergy_name.strip():
        return {
            "valid": False,
            "error": "Allergy name cannot be empty"
        }
    
    if len(allergy_name.strip()) < 2:
        return {
            "valid": False,
            "error": "Allergy name must be at least 2 characters long"
        }
    
    if len(allergy_name.strip()) > 50:
        return {
            "valid": False,
            "error": "Allergy name cannot exceed 50 characters"
        }
    
    return {
        "valid": True,
        "error": None
    } 

def get_alternative_ingredients(allergen_name: str, ingredient_name: str) -> List[str]:
    """
    Get alternative ingredients for a specific allergen and ingredient
    """
    try:
        allergen_alternatives = ALLERGEN_ALTERNATIVES.get(allergen_name.lower(), {})
        
        # Try exact match first
        if ingredient_name.lower() in allergen_alternatives:
            return allergen_alternatives[ingredient_name.lower()]
        
        # Try partial matches
        alternatives = []
        for key, value in allergen_alternatives.items():
            if key in ingredient_name.lower() or ingredient_name.lower() in key:
                alternatives.extend(value)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_alternatives = []
        for alt in alternatives:
            if alt not in seen:
                seen.add(alt)
                unique_alternatives.append(alt)
        
        return unique_alternatives[:3]  # Limit to 3 suggestions
        
    except Exception as e:
        logger.error(f"Error getting alternative ingredients: {e}")
        return []

def generate_alternative_suggestions(found_allergens: List[str], allergen_details: List[Dict]) -> Dict:
    """
    Generate alternative ingredient suggestions for found allergens
    """
    try:
        suggestions = {}
        
        for allergen in found_allergens:
            allergen_suggestions = {}
            
            # Find ingredients that triggered this allergen
            for detail in allergen_details:
                if detail['allergen'] == allergen:
                    ingredient = detail['ingredient']
                    alternatives = get_alternative_ingredients(allergen, ingredient)
                    
                    if alternatives:
                        allergen_suggestions[ingredient] = alternatives
            
            if allergen_suggestions:
                suggestions[allergen] = allergen_suggestions
        
        return suggestions
        
    except Exception as e:
        logger.error(f"Error generating alternative suggestions: {e}")
        return {} 