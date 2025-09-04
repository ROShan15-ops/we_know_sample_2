from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import random
import jwt
import json
from datetime import datetime

# Import  modular services
from config import Config
from models import get_db, User, RecentSearch, Order, SavedAddress, UserPreference
from auth_service import create_access_token, verify_token, require_auth, create_user, authenticate_user
from ingredient_service import get_ingredients_by_dish_name, clean_dish_name, extract_dish_type, validate_recipe_relevance, scale_api_ingredients, get_recipe_ingredients_from_spoonacular_improved
from delivery_service import (
    find_and_rank_shops, assign_delivery_agent, estimate_delivery_time,
    get_google_distance_matrix
)
from mock_data import MOCK_SHOPS, DELIVERY_AGENTS


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app)

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'WeKno Food Delivery API'
    })

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        allergies = data.get('allergies', [])  # New: allergies list
        
        # Validate input
        if not all([name, email, password]):
            return jsonify({'error': 'Name, email, and password are required'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Get database session
        db = next(get_db())
        
        # Create user
        user, error = create_user(db, name, email, password)
        
        if error:
            return jsonify({'error': error}), 400
        
        # Add user allergies if provided
        if allergies:
            from allergy_service import add_user_allergy
            # Get a fresh database session for allergies
            db_allergies = next(get_db())
            try:
                for allergy_name in allergies:
                    if allergy_name.strip():  # Only add non-empty allergies
                        try:
                            add_user_allergy(db_allergies, user.id, allergy_name.strip(), "common")
                        except Exception as e:
                            logger.error(f"Error adding allergy {allergy_name}: {e}")
            finally:
                db_allergies.close()
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        })
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        # Validate input
        if not all([email, password]):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Get database session
        db = next(get_db())
        
        # Authenticate user
        user, error = authenticate_user(db, email, password)
        
        if error:
            return jsonify({'error': error}), 401
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        })
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/auth/me', methods=['GET'])
@require_auth
def get_user_profile():
    """Get current user profile"""
    try:
        user_id = request.user.get('user_id')
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'last_login': user.last_login.isoformat() if user.last_login else None
            }
        })
        
    except Exception as e:
        logger.error(f"Get profile error: {e}")
        return jsonify({'error': 'Failed to get profile'}), 500

# ============================================================================
# USER DATA ROUTES
# ============================================================================

@app.route('/user/recent-searches', methods=['GET'])
@require_auth
def get_user_recent_searches():
    """Get user's recent searches"""
    try:
        user_id = request.user.get('user_id')
        db = next(get_db())
        
        # Get recent searches for user, limit to 4 most recent
        recent_searches = db.query(RecentSearch).filter(
            RecentSearch.user_id == user_id
        ).order_by(RecentSearch.search_timestamp.desc()).limit(4).all()
        
        searches = []
        for search in recent_searches:
            searches.append({
                'id': search.id,
                'dish_name': search.dish_name,
                'timestamp': search.search_timestamp.isoformat()
            })
        
        return jsonify({
            'success': True,
            'recent_searches': searches
        })
        
    except Exception as e:
        logger.error(f"Get recent searches error: {e}")
        return jsonify({'error': 'Failed to get recent searches'}), 500

@app.route('/user/recent-searches', methods=['POST'])
@require_auth
def add_recent_search():
    """Add a new recent search for user"""
    try:
        user_id = request.user.get('user_id')
        data = request.get_json()
        dish_name = data.get('dish_name', '').strip()
        
        if not dish_name:
            return jsonify({'error': 'Dish name is required'}), 400
        
        db = next(get_db())
        
        # Check if search already exists for this user
        existing_search = db.query(RecentSearch).filter(
            RecentSearch.user_id == user_id,
            RecentSearch.dish_name == dish_name
        ).first()
        
        if existing_search:
            # Update timestamp
            existing_search.search_timestamp = datetime.utcnow()
        else:
            # Create new search
            new_search = RecentSearch(
                user_id=user_id,
                dish_name=dish_name
            )
            db.add(new_search)
        
        db.commit()
        
        return jsonify({
            'success': True,
            'message': 'Recent search added successfully'
        })
        
    except Exception as e:
        logger.error(f"Add recent search error: {e}")
        return jsonify({'error': 'Failed to add recent search'}), 500

@app.route('/user/orders', methods=['GET'])
@require_auth
def get_user_orders():
    """Get user's orders"""
    try:
        user_id = request.user.get('user_id')
        db = next(get_db())
        
        orders = db.query(Order).filter(
            Order.user_id == user_id
        ).order_by(Order.order_timestamp.desc()).all()
        
        order_list = []
        for order in orders:
            order_list.append({
                'id': order.id,
                'dish_name': order.dish_name,
                'ingredients': order.ingredients,
                'servings': order.servings,
                'status': order.status,
                'timestamp': order.order_timestamp.isoformat()
            })
        
        return jsonify({
            'success': True,
            'orders': order_list
        })
        
    except Exception as e:
        logger.error(f"Get orders error: {e}")
        return jsonify({'error': 'Failed to get orders'}), 500

@app.route('/user/orders', methods=['POST'])
@require_auth
def add_user_order():
    """Add a new order for user"""
    try:
        user_id = request.user.get('user_id')
        data = request.get_json()
        
        logger.info(f"Adding order for user_id: {user_id}")
        logger.info(f"Received data: {data}")
        
        dish_name = data.get('dish_name', '').strip()
        ingredients = data.get('ingredients', [])
        servings = data.get('servings', 2)
        
        logger.info(f"Parsed dish_name: '{dish_name}'")
        logger.info(f"Parsed ingredients: {ingredients}")
        logger.info(f"Parsed servings: {servings}")
        
        if not dish_name:
            logger.error("Dish name is missing")
            return jsonify({'error': 'Dish name is required'}), 400
        
        if not ingredients:
            logger.error("Ingredients are missing")
            return jsonify({'error': 'Ingredients are required'}), 400
        
        db = next(get_db())
        
        new_order = Order(
            user_id=user_id,
            dish_name=dish_name,
            ingredients=ingredients,
            servings=servings,
            status='pending'  # Explicitly set status
        )
        
        db.add(new_order)
        db.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order added successfully',
            'order_id': new_order.id
        })
        
    except Exception as e:
        logger.error(f"Add order error: {e}")
        return jsonify({'error': 'Failed to add order'}), 500

@app.route('/user/orders/<int:order_id>/status', methods=['PUT'])
@require_auth
def update_order_status(order_id):
    """Update order status"""
    try:
        user_id = request.user.get('user_id')
        data = request.get_json()
        new_status = data.get('status', '').strip()
        
        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
        
        db = next(get_db())
        
        order = db.query(Order).filter(
            Order.id == order_id,
            Order.user_id == user_id
        ).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        order.status = new_status
        db.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order status updated successfully'
        })
        
    except Exception as e:
        logger.error(f"Update order status error: {e}")
        return jsonify({'error': 'Failed to update order status'}), 500

@app.route('/user/orders/clear', methods=['DELETE'])
@require_auth
def clear_user_orders():
    """Clear all orders for the current user"""
    try:
        user_id = request.user.get('user_id')
        db = next(get_db())
        
        # Delete all orders for this user
        deleted_count = db.query(Order).filter(Order.user_id == user_id).delete()
        db.commit()
        
        logger.info(f"Cleared {deleted_count} orders for user {user_id}")
        
        return jsonify({
            'success': True,
            'message': f'Cleared {deleted_count} orders successfully'
        })
        
    except Exception as e:
        logger.error(f"Clear orders error: {e}")
        return jsonify({'error': 'Failed to clear orders'}), 500

@app.route('/user/addresses', methods=['GET'])
@require_auth
def get_user_addresses():
    """Get user's saved addresses"""
    try:
        user_id = request.user.get('user_id')
        print(f"DEBUG: Getting addresses for user_id: {user_id}")
        
        db = next(get_db())
        
        addresses = db.query(SavedAddress).filter(
            SavedAddress.user_id == user_id
        ).order_by(SavedAddress.created_at.desc()).all()
        
        print(f"DEBUG: Found {len(addresses)} addresses for user {user_id}")
        
        address_list = []
        for address in addresses:
            address_list.append({
                'id': address.id,
                'address_type': address.address_type,
                'address_line1': address.address_line1,
                'address_line2': address.address_line2,
                'city': address.city,
                'state': address.state,
                'zip_code': address.zip_code,
                'is_default': address.is_default,
                'created_at': address.created_at.isoformat()
            })
        
        print(f"DEBUG: Returning {len(address_list)} addresses")
        return jsonify({
            'success': True,
            'addresses': address_list
        })
        
    except Exception as e:
        print(f"DEBUG: Exception in get_user_addresses: {e}")
        logger.error(f"Get addresses error: {e}")
        return jsonify({'error': 'Failed to get addresses'}), 500

@app.route('/user/addresses', methods=['POST'])
@require_auth
def add_user_address():
    """Add a new address for user"""
    try:
        user_id = request.user.get('user_id')
        data = request.get_json()
        
        print(f"DEBUG: Adding address for user_id: {user_id}")
        print(f"DEBUG: Address data: {data}")
        
        address_type = data.get('address_type', '').strip()
        address_line1 = data.get('address_line1', '').strip()
        address_line2 = data.get('address_line2', '').strip()
        city = data.get('city', '').strip()
        state = data.get('state', '').strip()
        zip_code = data.get('zip_code', '').strip()
        
        if not all([address_type, address_line1, city, state, zip_code]):
            print(f"DEBUG: Missing required fields")
            return jsonify({'error': 'All address fields are required'}), 400
        
        db = next(get_db())
        
        # If this is set as default, unset other defaults
        is_default = data.get('is_default', False)
        if is_default:
            db.query(SavedAddress).filter(
                SavedAddress.user_id == user_id,
                SavedAddress.is_default == True
            ).update({'is_default': False})
        
        new_address = SavedAddress(
            user_id=user_id,
            address_type=address_type,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            zip_code=zip_code,
            is_default=is_default
        )
        
        print(f"DEBUG: Created address object: {new_address}")
        db.add(new_address)
        db.commit()
        print(f"DEBUG: Address committed to database with ID: {new_address.id}")
        
        return jsonify({
            'success': True,
            'message': 'Address added successfully',
            'address_id': new_address.id
        })
        
    except Exception as e:
        print(f"DEBUG: Exception in add_user_address: {e}")
        logger.error(f"Add address error: {e}")
        return jsonify({'error': 'Failed to add address'}), 500

@app.route('/user/addresses/<int:address_id>', methods=['DELETE'])
@require_auth
def delete_user_address(address_id):
    """Delete a user's address"""
    try:
        user_id = request.user.get('user_id')
        db = next(get_db())
        
        # Find the address and ensure it belongs to the user
        address = db.query(SavedAddress).filter(
            SavedAddress.id == address_id,
            SavedAddress.user_id == user_id
        ).first()
        
        if not address:
            return jsonify({'error': 'Address not found'}), 404
        
        # Delete the address
        db.delete(address)
        db.commit()
        
        return jsonify({
            'success': True,
            'message': 'Address deleted successfully'
        })
        
    except Exception as e:
        logger.error(f"Delete address error: {e}")
        return jsonify({'error': 'Failed to delete address'}), 500

@app.route('/user/addresses/<int:address_id>/default', methods=['PUT'])
@require_auth
def set_default_address(address_id):
    """Set an address as default for the user"""
    try:
        user_id = request.user.get('user_id')
        db = next(get_db())
        
        # Find the address and ensure it belongs to the user
        address = db.query(SavedAddress).filter(
            SavedAddress.id == address_id,
            SavedAddress.user_id == user_id
        ).first()
        
        if not address:
            return jsonify({'error': 'Address not found'}), 404
        
        # Unset all other addresses as default
        db.query(SavedAddress).filter(
            SavedAddress.user_id == user_id,
            SavedAddress.is_default == True
        ).update({'is_default': False})
        
        # Set this address as default
        address.is_default = True
        db.commit()
        
        return jsonify({
            'success': True,
            'message': 'Default address updated successfully'
        })
        
    except Exception as e:
        logger.error(f"Set default address error: {e}")
        return jsonify({'error': 'Failed to set default address'}), 500

@app.route('/user/preferences', methods=['GET'])
@require_auth
def get_user_preferences():
    """Get user's preferences"""
    try:
        user_id = request.user.get('user_id')
        db = next(get_db())
        
        preferences = db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).first()
        
        if not preferences:
            # Create default preferences
            preferences = UserPreference(
                user_id=user_id,
                dietary_restrictions=[],
                favorite_cuisines=[],
                serving_size_preference=2,
                notifications_enabled=True
            )
            db.add(preferences)
            db.commit()
        
        return jsonify({
            'success': True,
            'preferences': {
                'dietary_restrictions': preferences.dietary_restrictions,
                'favorite_cuisines': preferences.favorite_cuisines,
                'serving_size_preference': preferences.serving_size_preference,
                'notifications_enabled': preferences.notifications_enabled
            }
        })
        
    except Exception as e:
        logger.error(f"Get preferences error: {e}")
        return jsonify({'error': 'Failed to get preferences'}), 500

@app.route('/user/preferences', methods=['PUT'])
@require_auth
def update_user_preferences():
    """Update user's preferences"""
    try:
        user_id = request.user.get('user_id')
        data = request.get_json()
        db = next(get_db())
        
        preferences = db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).first()
        
        if not preferences:
            preferences = UserPreference(user_id=user_id)
            db.add(preferences)
        
        # Update fields if provided
        if 'dietary_restrictions' in data:
            preferences.dietary_restrictions = data['dietary_restrictions']
        if 'favorite_cuisines' in data:
            preferences.favorite_cuisines = data['favorite_cuisines']
        if 'serving_size_preference' in data:
            preferences.serving_size_preference = data['serving_size_preference']
        if 'notifications_enabled' in data:
            preferences.notifications_enabled = data['notifications_enabled']
        
        db.commit()
        
        return jsonify({
            'success': True,
            'message': 'Preferences updated successfully'
        })
        
    except Exception as e:
        logger.error(f"Update preferences error: {e}")
        return jsonify({'error': 'Failed to update preferences'}), 500

# ============================================================================
# INGREDIENTS ROUTES
# ============================================================================

# ============================================================================
# ALLERGY ROUTES
# ============================================================================

@app.route('/allergies/common', methods=['GET'])
def get_common_allergens():
    """Get list of common allergens"""
    try:
        from allergy_service import get_common_allergens
        allergens = get_common_allergens()
        return jsonify({
            'success': True,
            'allergens': allergens
        })
    except Exception as e:
        logger.error(f"Error getting common allergens: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get common allergens'
        }), 500

@app.route('/user/allergies', methods=['GET'])
@require_auth
def get_user_allergies():
    """Get user's allergies"""
    try:
        user_id = request.user.get('user_id')
        db = next(get_db())
        
        from allergy_service import get_user_allergies
        allergies = get_user_allergies(db, user_id)
        
        return jsonify({
            'success': True,
            'allergies': allergies
        })
        
    except Exception as e:
        logger.error(f"Error getting user allergies: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get user allergies'
        }), 500

@app.route('/user/allergies', methods=['POST'])
@require_auth
def add_user_allergy():
    """Add a new allergy for user"""
    try:
        user_id = request.user.get('user_id')
        data = request.get_json()
        
        allergy_name = data.get('allergy_name', '').strip()
        allergy_type = data.get('allergy_type', 'custom')
        
        if not allergy_name:
            return jsonify({
                'success': False,
                'error': 'Allergy name is required'
            }), 400
        
        # Validate allergy name
        from allergy_service import validate_allergy_name
        validation = validate_allergy_name(allergy_name)
        if not validation['valid']:
            return jsonify({
                'success': False,
                'error': validation['error']
            }), 400
        
        db = next(get_db())
        
        from allergy_service import add_user_allergy
        result = add_user_allergy(db, user_id, allergy_name, allergy_type)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Error adding user allergy: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to add allergy'
        }), 500

@app.route('/user/allergies/<int:allergy_id>', methods=['DELETE'])
@require_auth
def remove_user_allergy(allergy_id):
    """Remove an allergy for user"""
    try:
        user_id = request.user.get('user_id')
        db = next(get_db())
        
        from allergy_service import remove_user_allergy
        result = remove_user_allergy(db, user_id, allergy_id)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Error removing user allergy: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to remove allergy'
        }), 500

# ============================================================================
# NUTRITION ROUTES
# ============================================================================

@app.route('/nutrition', methods=['POST'])
def get_nutrition():
    """Get nutrition information for a dish"""
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        dish_name = data.get('dish_name', '').strip()
        servings = data.get('servings', 1)
        
        # Validate input
        if not dish_name:
            return jsonify({
                'success': False,
                'error': 'Dish name is required'
            }), 400
        
        if not isinstance(servings, int) or servings < 1 or servings > 10:
            return jsonify({
                'success': False,
                'error': 'Servings must be an integer between 1 and 10'
            }), 400
        
        logger.info(f"Getting nutrition for dish: '{dish_name}' for {servings} servings")
        
        # Import nutrition service
        from nutrition_service import get_nutrition_info
        
        # Get nutrition information
        nutrition_result = get_nutrition_info(dish_name, servings)
        
        if nutrition_result.get('success'):
            return jsonify(nutrition_result)
        else:
            return jsonify({
                'success': False,
                'error': nutrition_result.get('error', 'Failed to get nutrition information')
            }), 404
        
    except Exception as e:
        logger.error(f"Nutrition error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get nutrition information'
        }), 500

@app.route('/ingredients', methods=['POST'])
def get_ingredients():
    """Main endpoint to get ingredients for a dish"""
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        dish_name = data.get('dish_name', '').strip()
        servings = data.get('servings', 2)
        include_nutrition = data.get('include_nutrition', False)
        
        # Validate input
        if not dish_name:
            return jsonify({
                'success': False,
                'error': 'Dish name is required'
            }), 400
        
        if not isinstance(servings, int) or servings < 1 or servings > 10:
            return jsonify({
                'success': False,
                'error': 'Servings must be an integer between 1 and 10'
            }), 400
        
        # Clean dish name using NLP
        cleaned_dish_name = clean_dish_name(dish_name)
        logger.info(f"Processing dish: '{dish_name}' -> '{cleaned_dish_name}'")
        
        # Extract expected dish type
        expected_dish_type = extract_dish_type(dish_name)
        
        # Try to get ingredients using the comprehensive function
        logger.info(f"Trying to get ingredients for: {dish_name}")
        print(f"PRINT: About to call get_ingredients_by_dish_name for: {dish_name}")
        try:
            ingredients = get_ingredients_by_dish_name(dish_name)
            print(f"PRINT: get_ingredients_by_dish_name returned: {ingredients}")
            logger.info(f"DEBUG: get_ingredients_by_dish_name returned: {ingredients}")
            logger.info(f"DEBUG: Type of ingredients: {type(ingredients)}")
            logger.info(f"DEBUG: Length of ingredients: {len(ingredients) if ingredients else 0}")
            logger.info(f"DEBUG: bool(ingredients): {bool(ingredients)}")
        except Exception as e:
            print(f"PRINT: Exception in get_ingredients_by_dish_name: {e}")
            logger.error(f"ERROR: Exception in get_ingredients_by_dish_name: {e}")
            ingredients = []
        
        if ingredients:
            logger.info(f"DEBUG: ingredients is truthy, creating recipe_info")
            recipe_info = {
                'id': 0,  # No specific ID for Spoonacular
                'title': dish_name.title(),
                'servings': 2,
                'dish_type': expected_dish_type,
                'confidence': 0.9,
                'source': 'spoonacular'
            }
        else:
            logger.info(f"DEBUG: ingredients is falsy, setting empty ingredients list")
            # No ingredients found
            logger.warning(f"No ingredients found for: {dish_name}")
            ingredients = []
            recipe_info = {
                'id': 0,
                'title': dish_name.title(),
                'servings': 2,
                'dish_type': expected_dish_type,
                'confidence': 0.0,
                'source': 'none'
            }
        
        logger.info(f"DEBUG: After if/else, ingredients: {ingredients}")
        logger.info(f"DEBUG: After if/else, bool(ingredients): {bool(ingredients)}")
        
        # Check if we have ingredients
        if not ingredients:
            logger.info(f"DEBUG: ingredients is empty, returning 404")
            return jsonify({
                'success': False,
                'error': f'No ingredients found for "{dish_name}". Please try a different dish name.'
            }), 404
        
        # Scale ingredients based on servings
        # TheMealDB recipes are typically for 1 serving, so we scale from 1 to target servings
        original_servings = 1  # Assume all recipes are for 1 serving
        logger.info(f"🔍 DEBUG: About to scale ingredients. Original servings: {original_servings}, Target servings: {servings}")
        logger.info(f"🔍 DEBUG: Original ingredients: {ingredients[:2]}...")  # Show first 2 ingredients
        try:
            logger.info(f"🔍 DEBUG: Calling scale_api_ingredients with: ingredients={len(ingredients)}, original_servings={original_servings}, servings={servings}")
            scaled_ingredients = scale_api_ingredients(ingredients, original_servings, servings)
            logger.info(f"🔄 Scaled ingredients from {original_servings} to {servings} servings")
            logger.info(f"🔍 DEBUG: Scaled ingredients: {scaled_ingredients[:2]}...")  # Show first 2 ingredients
            logger.info(f"🔍 DEBUG: Original first ingredient: {ingredients[0] if ingredients else 'None'}")
            logger.info(f"🔍 DEBUG: Scaled first ingredient: {scaled_ingredients[0] if scaled_ingredients else 'None'}")
        except Exception as e:
            logger.error(f"Error scaling ingredients: {e}")
            logger.error(f"Exception details: {type(e).__name__}: {str(e)}")
            logger.error(f"Exception traceback: {e.__traceback__}")
            scaled_ingredients = ingredients
        
        # Get nutrition information if requested
        nutrition_data = None
        if include_nutrition:
            try:
                from nutrition_service import get_nutrition_info
                # Calculate nutrition from actual ingredients
                nutrition_result = get_nutrition_info(dish_name, servings, scaled_ingredients)
                if nutrition_result.get('success'):
                    nutrition_data = nutrition_result
                else:
                    logger.warning(f"Failed to get nutrition for {dish_name}: {nutrition_result.get('error')}")
            except Exception as e:
                logger.error(f"Error fetching nutrition: {e}")
        
        # Format response
        response_data = {
            'success': True,
            'ingredients': scaled_ingredients,
            'recipe_info': {
                'title': recipe_info['title'],
                'original_servings': original_servings,
                'requested_servings': servings,
                'search_term': dish_name,
                'cleaned_term': cleaned_dish_name,
                'dish_type': recipe_info.get('dish_type'),
                'confidence': recipe_info.get('confidence', 0.0)
            }
        }
        
        # Add nutrition data if available
        if nutrition_data:
            response_data['nutrition'] = nutrition_data.get('nutrition', {})
            response_data['nutrition_success'] = nutrition_data.get('success', False)
            response_data['nutrition_error'] = nutrition_data.get('error')
        
        # Check for allergies if user is authenticated
        allergy_warning = None
        if request.headers.get('Authorization'):
            try:
                # Extract user from token
                auth_header = request.headers.get('Authorization')
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
                    from auth_service import verify_token
                    user_data = verify_token(token)
                    if user_data:
                        user_id = user_data.get('user_id')
                        db = next(get_db())
                        
                        # Get user's allergies
                        from allergy_service import get_user_allergies, check_ingredients_for_allergies
                        user_allergies = get_user_allergies(db, user_id)
                        allergy_names = [allergy['allergy_name'] for allergy in user_allergies]
                        
                        if allergy_names:
                            # Check ingredients for allergies
                            allergy_check = check_ingredients_for_allergies(scaled_ingredients, allergy_names)
                            logger.info(f"Allergy check result: {allergy_check}")
                            if allergy_check['has_allergens']:
                                allergy_warning = allergy_check['warning_message']
                                response_data['allergy_warning'] = allergy_warning
                                response_data['found_allergens'] = allergy_check['found_allergens']
                                response_data['allergen_details'] = allergy_check['allergen_details']
                                response_data['alternative_suggestions'] = allergy_check['alternative_suggestions']
                                logger.info(f"Added alternative suggestions: {allergy_check['alternative_suggestions']}")
                                
            except Exception as e:
                logger.error(f"Error checking allergies: {e}")
                # Don't fail the request if allergy check fails
        
        logger.info(f"Successfully processed '{dish_name}' for {servings} servings")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your request. Please try again.'
        }), 500

@app.route('/search-varieties', methods=['POST'])
def search_varieties():
    """Search for pizza varieties"""
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        dish_name = data.get('dish_name', '').strip().lower()
        
        # Validate input
        if not dish_name:
            return jsonify({
                'success': False,
                'error': 'Dish name is required'
            }), 400
        
        # Define varieties based on dish type
        varieties = []
        
        if 'pizza' in dish_name:
            varieties = [
                {
                    'id': 1,
                    'title': 'Margherita Pizza',
                    'servings': 2,
                    'confidence': 0.95,
                    'image': 'https://images.pexels.com/photos/825661/pexels-photo-825661.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 2,
                    'title': 'Marinara Pizza',
                    'servings': 2,
                    'confidence': 0.94,
                    'image': 'https://images.pexels.com/photos/1146760/pexels-photo-1146760.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 3,
                    'title': 'Quattro Formaggi Pizza',
                    'servings': 2,
                    'confidence': 0.93,
                    'image': 'https://images.pexels.com/photos/905847/pexels-photo-905847.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 4,
                    'title': 'Quattro Stagioni Pizza',
                    'servings': 2,
                    'confidence': 0.92,
                    'image': 'https://images.pexels.com/photos/1146760/pexels-photo-1146760.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 5,
                    'title': 'Romana Pizza',
                    'servings': 2,
                    'confidence': 0.91,
                    'image': 'https://images.pexels.com/photos/905847/pexels-photo-905847.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 6,
                    'title': 'Capricciosa Pizza',
                    'servings': 2,
                    'confidence': 0.90,
                    'image': 'https://images.pexels.com/photos/825661/pexels-photo-825661.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 7,
                    'title': 'Bianca Pizza',
                    'servings': 2,
                    'confidence': 0.89,
                    'image': 'https://images.pexels.com/photos/905847/pexels-photo-905847.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 8,
                    'title': 'Pizza e Fichi',
                    'servings': 2,
                    'confidence': 0.88,
                    'image': 'https://images.pexels.com/photos/825661/pexels-photo-825661.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 9,
                    'title': 'Pizza Rossini',
                    'servings': 2,
                    'confidence': 0.87,
                    'image': 'https://images.pexels.com/photos/1146760/pexels-photo-1146760.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 10,
                    'title': 'Hawaiian Pizza',
                    'servings': 2,
                    'confidence': 0.86,
                    'image': 'https://images.pexels.com/photos/905847/pexels-photo-905847.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 11,
                    'title': 'Pepperoni Pizza',
                    'servings': 2,
                    'confidence': 0.85,
                    'image': 'https://images.pexels.com/photos/825661/pexels-photo-825661.jpeg?w=200&h=150&fit=crop&crop=center'
                }
            ]
        elif 'sandwich' in dish_name:
            varieties = [
                {
                    'id': 1,
                    'title': 'Club Sandwich',
                    'servings': 2,
                    'confidence': 0.95,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 2,
                    'title': 'Grilled Cheese Sandwich',
                    'servings': 2,
                    'confidence': 0.92,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 3,
                    'title': 'BLT Sandwich',
                    'servings': 2,
                    'confidence': 0.88,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 4,
                    'title': 'Turkey Sandwich',
                    'servings': 2,
                    'confidence': 0.85,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 5,
                    'title': 'Chicken Sandwich',
                    'servings': 2,
                    'confidence': 0.83,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 6,
                    'title': 'Veggie Sandwich',
                    'servings': 2,
                    'confidence': 0.80,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 7,
                    'title': 'Tuna Sandwich',
                    'servings': 2,
                    'confidence': 0.78,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 8,
                    'title': 'Ham and Cheese Sandwich',
                    'servings': 2,
                    'confidence': 0.75,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                }
            ]
        elif 'chicken' in dish_name:
            varieties = [
                {
                    'id': 1,
                    'title': 'Chicken Wings',
                    'servings': 2,
                    'confidence': 0.95,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 2,
                    'title': 'Chicken Breast',
                    'servings': 2,
                    'confidence': 0.92,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 3,
                    'title': 'Chicken Thighs',
                    'servings': 2,
                    'confidence': 0.88,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 4,
                    'title': 'Chicken Tikka Masala',
                    'servings': 2,
                    'confidence': 0.85,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 5,
                    'title': 'Chicken Curry',
                    'servings': 2,
                    'confidence': 0.83,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 6,
                    'title': 'Chicken Stir Fry',
                    'servings': 2,
                    'confidence': 0.80,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 7,
                    'title': 'Chicken Soup',
                    'servings': 2,
                    'confidence': 0.78,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 8,
                    'title': 'Chicken Salad',
                    'servings': 2,
                    'confidence': 0.75,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                }
            ]
        elif 'burger' in dish_name:
            varieties = [
                {
                    'id': 1,
                    'title': 'Classic Beef Burger',
                    'servings': 2,
                    'confidence': 0.95,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 2,
                    'title': 'Cheeseburger',
                    'servings': 2,
                    'confidence': 0.94,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 3,
                    'title': 'Bacon Burger',
                    'servings': 2,
                    'confidence': 0.93,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 4,
                    'title': 'Chicken Burger',
                    'servings': 2,
                    'confidence': 0.92,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 5,
                    'title': 'Veggie Burger',
                    'servings': 2,
                    'confidence': 0.91,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 6,
                    'title': 'Mushroom Swiss Burger',
                    'servings': 2,
                    'confidence': 0.90,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 7,
                    'title': 'Fish Burger',
                    'servings': 2,
                    'confidence': 0.89,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 8,
                    'title': 'BBQ Burger',
                    'servings': 2,
                    'confidence': 0.88,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 9,
                    'title': 'Double Patty Burger',
                    'servings': 2,
                    'confidence': 0.87,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 10,
                    'title': 'Vegan Burger',
                    'servings': 2,
                    'confidence': 0.86,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 11,
                    'title': 'Turkey Burger',
                    'servings': 2,
                    'confidence': 0.85,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 12,
                    'title': 'Bacon Cheeseburger',
                    'servings': 2,
                    'confidence': 0.84,
                    'image': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?w=200&h=150&fit=crop&crop=center'
                }
            ]
        elif 'pasta' in dish_name or 'noodle' in dish_name:
            varieties = [
                {
                    'id': 1,
                    'title': 'Spaghetti Carbonara',
                    'servings': 2,
                    'confidence': 0.95,
                    'image': 'https://images.pexels.com/photos/1437267/pexels-photo-1437267.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 2,
                    'title': 'Fettuccine Alfredo',
                    'servings': 2,
                    'confidence': 0.92,
                    'image': 'https://images.pexels.com/photos/1437267/pexels-photo-1437267.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 3,
                    'title': 'Penne Arrabbiata',
                    'servings': 2,
                    'confidence': 0.88,
                    'image': 'https://images.pexels.com/photos/1437267/pexels-photo-1437267.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 4,
                    'title': 'Linguine Marinara',
                    'servings': 2,
                    'confidence': 0.85,
                    'image': 'https://images.pexels.com/photos/1437267/pexels-photo-1437267.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 5,
                    'title': 'Spaghetti Bolognese',
                    'servings': 2,
                    'confidence': 0.83,
                    'image': 'https://images.pexels.com/photos/1437267/pexels-photo-1437267.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 6,
                    'title': 'Penne Vodka',
                    'servings': 2,
                    'confidence': 0.80,
                    'image': 'https://images.pexels.com/photos/1437267/pexels-photo-1437267.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 7,
                    'title': 'Fettuccine Pesto',
                    'servings': 2,
                    'confidence': 0.78,
                    'image': 'https://images.pexels.com/photos/1437267/pexels-photo-1437267.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 8,
                    'title': 'Spaghetti Aglio e Olio',
                    'servings': 2,
                    'confidence': 0.75,
                    'image': 'https://images.pexels.com/photos/1437267/pexels-photo-1437267.jpeg?w=200&h=150&fit=crop&crop=center'
                }
            ]
        elif 'curry' in dish_name or 'masala' in dish_name:
            varieties = [
                {
                    'id': 1,
                    'title': 'Chicken Tikka Masala',
                    'servings': 2,
                    'confidence': 0.95,
                    'image': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 2,
                    'title': 'Butter Chicken',
                    'servings': 2,
                    'confidence': 0.92,
                    'image': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 3,
                    'title': 'Paneer Butter Masala',
                    'servings': 2,
                    'confidence': 0.88,
                    'image': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 4,
                    'title': 'Chicken Biryani',
                    'servings': 2,
                    'confidence': 0.85,
                    'image': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 5,
                    'title': 'Mutton Biryani',
                    'servings': 2,
                    'confidence': 0.83,
                    'image': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 6,
                    'title': 'Veg Biryani',
                    'servings': 2,
                    'confidence': 0.80,
                    'image': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 7,
                    'title': 'Fish Curry',
                    'servings': 2,
                    'confidence': 0.78,
                    'image': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 8,
                    'title': 'Dal Makhani',
                    'servings': 2,
                    'confidence': 0.75,
                    'image': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg?w=200&h=150&fit=crop&crop=center'
                }
            ]
        elif 'salad' in dish_name:
            varieties = [
                {
                    'id': 1,
                    'title': 'Caesar Salad',
                    'servings': 2,
                    'confidence': 0.95,
                    'image': 'https://images.pexels.com/photos/1213710/pexels-photo-1213710.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 2,
                    'title': 'Greek Salad',
                    'servings': 2,
                    'confidence': 0.92,
                    'image': 'https://images.pexels.com/photos/1213710/pexels-photo-1213710.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 3,
                    'title': 'Cobb Salad',
                    'servings': 2,
                    'confidence': 0.88,
                    'image': 'https://images.pexels.com/photos/1213710/pexels-photo-1213710.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 4,
                    'title': 'Garden Salad',
                    'servings': 2,
                    'confidence': 0.85,
                    'image': 'https://images.pexels.com/photos/1213710/pexels-photo-1213710.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 5,
                    'title': 'Nicoise Salad',
                    'servings': 2,
                    'confidence': 0.83,
                    'image': 'https://images.pexels.com/photos/1213710/pexels-photo-1213710.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 6,
                    'title': 'Waldorf Salad',
                    'servings': 2,
                    'confidence': 0.80,
                    'image': 'https://images.pexels.com/photos/1213710/pexels-photo-1213710.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 7,
                    'title': 'Caprese Salad',
                    'servings': 2,
                    'confidence': 0.78,
                    'image': 'https://images.pexels.com/photos/1213710/pexels-photo-1213710.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 8,
                    'title': 'Asian Noodle Salad',
                    'servings': 2,
                    'confidence': 0.75,
                    'image': 'https://images.pexels.com/photos/1213710/pexels-photo-1213710.jpeg?w=200&h=150&fit=crop&crop=center'
                }
            ]
        elif 'rice' in dish_name or 'biryani' in dish_name or 'pulao' in dish_name:
            varieties = [
                {
                    'id': 1,
                    'title': 'Fried Rice',
                    'servings': 2,
                    'confidence': 0.95,
                    'image': 'https://images.pexels.com/photos/723198/pexels-photo-723198.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 2,
                    'title': 'Biryani Rice',
                    'servings': 2,
                    'confidence': 0.92,
                    'image': 'https://images.pexels.com/photos/723198/pexels-photo-723198.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 3,
                    'title': 'Pulao Rice',
                    'servings': 2,
                    'confidence': 0.88,
                    'image': 'https://images.pexels.com/photos/723198/pexels-photo-723198.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 4,
                    'title': 'Jeera Rice',
                    'servings': 2,
                    'confidence': 0.85,
                    'image': 'https://images.pexels.com/photos/723198/pexels-photo-723198.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 5,
                    'title': 'Lemon Rice',
                    'servings': 2,
                    'confidence': 0.83,
                    'image': 'https://images.pexels.com/photos/723198/pexels-photo-723198.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 6,
                    'title': 'Coconut Rice',
                    'servings': 2,
                    'confidence': 0.80,
                    'image': 'https://images.pexels.com/photos/723198/pexels-photo-723198.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 7,
                    'title': 'Mushroom Rice',
                    'servings': 2,
                    'confidence': 0.78,
                    'image': 'https://images.pexels.com/photos/723198/pexels-photo-723198.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 8,
                    'title': 'Vegetable Rice',
                    'servings': 2,
                    'confidence': 0.75,
                    'image': 'https://images.pexels.com/photos/723198/pexels-photo-723198.jpeg?w=200&h=150&fit=crop&crop=center'
                }
            ]
        elif 'ice cream' in dish_name or 'icecream' in dish_name or 'dessert' in dish_name:
            varieties = [
                {
                    'id': 1,
                    'title': 'Vanilla Ice Cream',
                    'servings': 2,
                    'confidence': 0.95,
                    'image': 'https://images.pexels.com/photos/1352281/pexels-photo-1352281.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 2,
                    'title': 'Chocolate Ice Cream',
                    'servings': 2,
                    'confidence': 0.92,
                    'image': 'https://images.pexels.com/photos/1352281/pexels-photo-1352281.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 3,
                    'title': 'Strawberry Ice Cream',
                    'servings': 2,
                    'confidence': 0.88,
                    'image': 'https://images.pexels.com/photos/1352281/pexels-photo-1352281.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 4,
                    'title': 'Mint Chocolate Chip',
                    'servings': 2,
                    'confidence': 0.85,
                    'image': 'https://images.pexels.com/photos/1352281/pexels-photo-1352281.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 5,
                    'title': 'Cookie Dough Ice Cream',
                    'servings': 2,
                    'confidence': 0.83,
                    'image': 'https://images.pexels.com/photos/1352281/pexels-photo-1352281.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 6,
                    'title': 'Rocky Road Ice Cream',
                    'servings': 2,
                    'confidence': 0.80,
                    'image': 'https://images.pexels.com/photos/1352281/pexels-photo-1352281.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 7,
                    'title': 'Coffee Ice Cream',
                    'servings': 2,
                    'confidence': 0.78,
                    'image': 'https://images.pexels.com/photos/1352281/pexels-photo-1352281.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 8,
                    'title': 'Butter Pecan Ice Cream',
                    'servings': 2,
                    'confidence': 0.75,
                    'image': 'https://images.pexels.com/photos/1352281/pexels-photo-1352281.jpeg?w=200&h=150&fit=crop&crop=center'
                }
            ]
        elif 'cake' in dish_name or 'pastry' in dish_name:
            varieties = [
                {
                    'id': 1,
                    'title': 'Chocolate Cake',
                    'servings': 2,
                    'confidence': 0.95,
                    'image': 'https://images.pexels.com/photos/291528/pexels-photo-291528.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 2,
                    'title': 'Vanilla Cake',
                    'servings': 2,
                    'confidence': 0.92,
                    'image': 'https://images.pexels.com/photos/291528/pexels-photo-291528.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 3,
                    'title': 'Red Velvet Cake',
                    'servings': 2,
                    'confidence': 0.88,
                    'image': 'https://images.pexels.com/photos/291528/pexels-photo-291528.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 4,
                    'title': 'Cheesecake',
                    'servings': 2,
                    'confidence': 0.85,
                    'image': 'https://images.pexels.com/photos/291528/pexels-photo-291528.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 5,
                    'title': 'Carrot Cake',
                    'servings': 2,
                    'confidence': 0.83,
                    'image': 'https://images.pexels.com/photos/291528/pexels-photo-291528.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 6,
                    'title': 'Tiramisu',
                    'servings': 2,
                    'confidence': 0.80,
                    'image': 'https://images.pexels.com/photos/291528/pexels-photo-291528.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 7,
                    'title': 'Black Forest Cake',
                    'servings': 2,
                    'confidence': 0.78,
                    'image': 'https://images.pexels.com/photos/291528/pexels-photo-291528.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 8,
                    'title': 'Strawberry Shortcake',
                    'servings': 2,
                    'confidence': 0.75,
                    'image': 'https://images.pexels.com/photos/291528/pexels-photo-291528.jpeg?w=200&h=150&fit=crop&crop=center'
                }
            ]
        elif 'soup' in dish_name:
            varieties = [
                {
                    'id': 1,
                    'title': 'Tomato Soup',
                    'servings': 2,
                    'confidence': 0.95,
                    'image': 'https://images.pexels.com/photos/539451/pexels-photo-539451.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 2,
                    'title': 'Chicken Noodle Soup',
                    'servings': 2,
                    'confidence': 0.92,
                    'image': 'https://images.pexels.com/photos/539451/pexels-photo-539451.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 3,
                    'title': 'Vegetable Soup',
                    'servings': 2,
                    'confidence': 0.88,
                    'image': 'https://images.pexels.com/photos/539451/pexels-photo-539451.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 4,
                    'title': 'Mushroom Soup',
                    'servings': 2,
                    'confidence': 0.85,
                    'image': 'https://images.pexels.com/photos/539451/pexels-photo-539451.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 5,
                    'title': 'Lentil Soup',
                    'servings': 2,
                    'confidence': 0.83,
                    'image': 'https://images.pexels.com/photos/539451/pexels-photo-539451.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 6,
                    'title': 'Minestrone Soup',
                    'servings': 2,
                    'confidence': 0.80,
                    'image': 'https://images.pexels.com/photos/539451/pexels-photo-539451.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 7,
                    'title': 'Clam Chowder',
                    'servings': 2,
                    'confidence': 0.78,
                    'image': 'https://images.pexels.com/photos/539451/pexels-photo-539451.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 8,
                    'title': 'Gazpacho',
                    'servings': 2,
                    'confidence': 0.75,
                    'image': 'https://images.pexels.com/photos/539451/pexels-photo-539451.jpeg?w=200&h=150&fit=crop&crop=center'
                }
            ]
        elif 'steak' in dish_name or 'beef' in dish_name:
            varieties = [
                {
                    'id': 1,
                    'title': 'Ribeye Steak',
                    'servings': 2,
                    'confidence': 0.95,
                    'image': 'https://images.pexels.com/photos/3535383/pexels-photo-3535383.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 2,
                    'title': 'Filet Mignon',
                    'servings': 2,
                    'confidence': 0.92,
                    'image': 'https://images.pexels.com/photos/3535383/pexels-photo-3535383.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 3,
                    'title': 'Sirloin Steak',
                    'servings': 2,
                    'confidence': 0.88,
                    'image': 'https://images.pexels.com/photos/3535383/pexels-photo-3535383.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 4,
                    'title': 'T-Bone Steak',
                    'servings': 2,
                    'confidence': 0.85,
                    'image': 'https://images.pexels.com/photos/3535383/pexels-photo-3535383.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 5,
                    'title': 'Porterhouse Steak',
                    'servings': 2,
                    'confidence': 0.83,
                    'image': 'https://images.pexels.com/photos/3535383/pexels-photo-3535383.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 6,
                    'title': 'New York Strip',
                    'servings': 2,
                    'confidence': 0.80,
                    'image': 'https://images.pexels.com/photos/3535383/pexels-photo-3535383.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 7,
                    'title': 'Beef Tenderloin',
                    'servings': 2,
                    'confidence': 0.78,
                    'image': 'https://images.pexels.com/photos/3535383/pexels-photo-3535383.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 8,
                    'title': 'Beef Brisket',
                    'servings': 2,
                    'confidence': 0.75,
                    'image': 'https://images.pexels.com/photos/3535383/pexels-photo-3535383.jpeg?w=200&h=150&fit=crop&crop=center'
                }
            ]
        elif 'chicken' in dish_name:
            varieties = [
                {
                    'id': 1,
                    'title': 'Grilled Chicken',
                    'servings': 2,
                    'confidence': 0.95,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 2,
                    'title': 'Fried Chicken',
                    'servings': 2,
                    'confidence': 0.92,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 3,
                    'title': 'Baked Chicken',
                    'servings': 2,
                    'confidence': 0.88,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 4,
                    'title': 'Chicken Tikka',
                    'servings': 2,
                    'confidence': 0.85,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 5,
                    'title': 'Chicken Wings',
                    'servings': 2,
                    'confidence': 0.83,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 6,
                    'title': 'Chicken Curry',
                    'servings': 2,
                    'confidence': 0.80,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 7,
                    'title': 'Chicken Breast',
                    'servings': 2,
                    'confidence': 0.78,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 8,
                    'title': 'Chicken Thighs',
                    'servings': 2,
                    'confidence': 0.75,
                    'image': 'https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?w=200&h=150&fit=crop&crop=center'
                }
            ]
        else:
            # Generic varieties for other dishes
            varieties = [
                {
                    'id': 1,
                    'title': f'Classic {dish_name.title()}',
                    'servings': 2,
                    'confidence': 0.90,
                    'image': 'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 2,
                    'title': f'Spicy {dish_name.title()}',
                    'servings': 2,
                    'confidence': 0.85,
                    'image': 'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 3,
                    'title': f'Vegetarian {dish_name.title()}',
                    'servings': 2,
                    'confidence': 0.80,
                    'image': 'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 4,
                    'title': f'Creamy {dish_name.title()}',
                    'servings': 2,
                    'confidence': 0.75,
                    'image': 'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 5,
                    'title': f'Garlic {dish_name.title()}',
                    'servings': 2,
                    'confidence': 0.70,
                    'image': 'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?w=200&h=150&fit=crop&crop=center'
                },
                {
                    'id': 6,
                    'title': f'Herb {dish_name.title()}',
                    'servings': 2,
                    'confidence': 0.65,
                    'image': 'https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?w=200&h=150&fit=crop&crop=center'
                }
            ]
        
        return jsonify({
            'success': True,
            'varieties': varieties
        })
        
    except Exception as e:
        logger.error(f"Error searching varieties: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to search varieties. Please try again.'
        }), 500

# ============================================================================
# DELIVERY ROUTES
# ============================================================================

@app.route('/delivery', methods=['POST'])
@require_auth
def create_delivery_order():
    """Main delivery endpoint for WeKno food delivery app"""
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        dish_name = data.get('dish_name', '').strip()
        servings = data.get('servings', 2)
        user_location = data.get('user_location', {})
        
        # Validate input
        if not dish_name:
            return jsonify({
                'success': False,
                'error': 'Dish name is required'
            }), 400
        
        if not isinstance(servings, int) or servings < 1 or servings > 10:
            return jsonify({
                'success': False,
                'error': 'Servings must be an integer between 1 and 10'
            }), 400
        
        # Validate user location (use default if not provided)
        if not user_location or not user_location.get('lat') or not user_location.get('lng'):
            user_location = Config.DEFAULT_USER_LOCATION
            logger.info(f"No user location provided, using default: {user_location}")
        
        logger.info(f"Processing delivery order for: '{dish_name}'")
        
        # Step 1: Fetch ingredients from Spoonacular API first
        ingredients = get_ingredients_by_dish_name(dish_name)
        
        # Try fallback for pizza varieties if Spoonacular fails
        if not ingredients:
            logger.info(f"Trying fallback for pizza varieties in delivery: {dish_name}")
            ingredients = get_ingredients_by_dish_name(dish_name)
        
        if not ingredients:
            logger.warning(f"No ingredients found in Spoonacular or fallback for delivery: {dish_name}")
            return jsonify({
                'success': False,
                'error': f'No ingredients found for "{dish_name}". Please try a different dish.'
            }), 404
        
        # Step 2: Scale ingredients based on servings
        scaled_ingredients = scale_api_ingredients(ingredients, 2, servings)
        
        # Step 3: Find and rank shops
        ranked_shops = find_and_rank_shops(
            user_location, 
            scaled_ingredients, 
            MOCK_SHOPS, 
            Config.MAX_DELIVERY_DISTANCE_KM, 
            Config.MIN_INGREDIENT_MATCH_PERCENT
        )
        
        if not ranked_shops:
            return jsonify({
                'success': False,
                'error': f'No shops found within {Config.MAX_DELIVERY_DISTANCE_KM}km with at least {Config.MIN_INGREDIENT_MATCH_PERCENT}% ingredient match.'
            }), 404
        
        # Step 4: Get top shop
        top_shop = ranked_shops[0]
        
        # Step 5: Assign delivery agent
        delivery_agent = assign_delivery_agent(top_shop["location"])
        
        if not delivery_agent:
            return jsonify({
                'success': False,
                'error': 'No delivery agents available at the moment.'
            }), 503
        
        # Step 6: Generate order ID
        order_id = f"WK{random.randint(10000, 99999)}"
        
        # Step 7: Calculate total delivery time
        total_delivery_time = estimate_delivery_time(
            top_shop["distance_km"], 
            len(scaled_ingredients)
        )
        
        # Step 8: Format response
        response_data = {
            'success': True,
            'order_id': order_id,
            'dish': dish_name,
            'ingredients': scaled_ingredients,
            'top_shop': {
                'name': top_shop["name"],
                'match_percent': top_shop["match_percent"],
                'distance_km': top_shop["distance_km"],
                'available_ingredients': top_shop["available_ingredients"],
                'missing_ingredients': top_shop["missing_ingredients"]
            },
            'delivery_agent': delivery_agent,
            'estimated_delivery_time_minutes': total_delivery_time,
            'all_qualified_shops': ranked_shops
        }
        
        logger.info(f"Created delivery order for '{dish_name}': {order_id}")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error creating delivery order: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to create delivery order. Please try again.'
        }), 500

@app.route('/delivery/test', methods=['POST'])
def create_delivery_order_test():
    """Test delivery endpoint (no authentication required)"""
    print("=== DELIVERY TEST ENDPOINT CALLED ===")
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        dish_name = data.get('dish_name', '').strip()
        servings = data.get('servings', 2)
        user_location = data.get('user_location', {})
        
        # Check for authentication token
        auth_header = request.headers.get('Authorization')
        user_id = None
        
        print(f"Auth header present: {auth_header is not None}")
        logger.info(f"Auth header present: {auth_header is not None}")
        if auth_header:
            print(f"Auth header starts with Bearer: {auth_header.startswith('Bearer ')}")
            logger.info(f"Auth header starts with Bearer: {auth_header.startswith('Bearer ')}")
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            logger.info(f"Token extracted: {token[:20]}...")
            try:
                # Decode token to get user_id
                payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')
                logger.info(f"Authenticated user ID: {user_id}")
            except jwt.ExpiredSignatureError:
                logger.warning("Token expired")
            except jwt.InvalidTokenError as e:
                logger.warning(f"Invalid token: {str(e)}")
            except Exception as e:
                logger.error(f"JWT decode error: {str(e)}")
        else:
            logger.info("No valid authorization header found")
        
        # Validate input
        if not dish_name:
            return jsonify({
                'success': False,
                'error': 'Dish name is required'
            }), 400
        
        if not isinstance(servings, int) or servings < 1 or servings > 10:
            return jsonify({
                'success': False,
                'error': 'Servings must be an integer between 1 and 10'
            }), 400
        
        # Validate user location (use default if not provided)
        if not user_location or not user_location.get('lat') or not user_location.get('lng'):
            user_location = Config.DEFAULT_USER_LOCATION
            logger.info(f"No user location provided, using default: {user_location}")
        
        logger.info(f"Processing TEST delivery order for: '{dish_name}' -> '{dish_name}' (User ID: {user_id})")
        
        # Step 1: Fetch ingredients from Spoonacular API first
        ingredients = get_recipe_ingredients_from_spoonacular_improved(dish_name)
        
        # Try fallback for pizza varieties if Spoonacular fails
        if not ingredients:
            logger.info(f"Trying fallback for pizza varieties in test delivery: {dish_name}")
            ingredients = get_ingredients_by_dish_name(dish_name)
        
        if not ingredients:
            logger.warning(f"No ingredients found in Spoonacular or fallback for test delivery: {dish_name}")
            return jsonify({
                'success': False,
                'error': f'No ingredients found for "{dish_name}". Please try a different dish.'
            }), 404
        
        # Step 2: Scale ingredients based on servings
        scaled_ingredients = scale_api_ingredients(ingredients, 2, servings)
        
        # Step 3: Find and rank shops
        ranked_shops = find_and_rank_shops(
            user_location, 
            scaled_ingredients, 
            MOCK_SHOPS, 
            Config.MAX_DELIVERY_DISTANCE_KM, 
            Config.MIN_INGREDIENT_MATCH_PERCENT
        )
        
        if not ranked_shops:
            return jsonify({
                'success': False,
                'error': f'No shops found within {Config.MAX_DELIVERY_DISTANCE_KM}km with at least {Config.MIN_INGREDIENT_MATCH_PERCENT}% ingredient match.'
            }), 404
        
        # Step 4: Get top shop
        top_shop = ranked_shops[0]
        
        # Step 5: Assign delivery agent
        delivery_agent = assign_delivery_agent(top_shop["location"])
        
        if not delivery_agent:
            return jsonify({
                'success': False,
                'error': 'No delivery agents available at the moment.'
            }), 503
        
        # Step 6: Generate order ID
        order_id = f"WK{random.randint(10000, 99999)}"
        
        # Step 7: Calculate total delivery time
        total_delivery_time = estimate_delivery_time(
            top_shop["distance_km"], 
            len(scaled_ingredients)
        )
        
        # Step 8: Save order to user's database if authenticated
        if user_id:
            try:
                db = SessionLocal()
                new_order = Order(
                    user_id=user_id,
                    dish_name=dish_name,
                    ingredients=json.dumps(scaled_ingredients),
                    servings=servings,
                    status='pending',
                    timestamp=datetime.utcnow()
                )
                db.add(new_order)
                db.commit()
                db.refresh(new_order)
                logger.info(f"Order saved to database for user {user_id}: Order ID {new_order.id}")
                db.close()
            except Exception as e:
                logger.error(f"Error saving order to database: {str(e)}")
                db.close()
                # Continue with delivery order even if database save fails
        
        # Step 9: Format response
        response_data = {
            'success': True,
            'order_id': order_id,
            'dish': dish_name,
            'ingredients': scaled_ingredients,
            'top_shop': {
                'name': top_shop["name"],
                'match_percent': top_shop["match_percent"],
                'distance_km': top_shop["distance_km"],
                'available_ingredients': top_shop["available_ingredients"],
                'missing_ingredients': top_shop["missing_ingredients"]
            },
            'delivery_agent': delivery_agent,
            'estimated_delivery_time_minutes': total_delivery_time,
            'all_qualified_shops': ranked_shops
        }
        
        logger.info(f"Created TEST delivery order for '{dish_name}': {order_id}")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error creating TEST delivery order: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to create delivery order. Please try again.'
        }), 500



@app.route('/delivery/shops', methods=['GET'])
def get_available_shops():
    """Get available shops"""
    try:
        shops_data = []
        for shop_name, shop_data in MOCK_SHOPS.items():
            shops_data.append({
                'name': shop_name,
                'location': shop_data['location'],
                'inventory_count': len(shop_data['inventory']),
                'inventory': shop_data['inventory']
            })
        
        return jsonify({
            'success': True,
            'shops': shops_data
        })
        
    except Exception as e:
        logger.error(f"Error getting shops: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get shops'
        }), 500

@app.route('/delivery/agents', methods=['GET'])
def get_delivery_agents():
    """Get delivery agents"""
    try:
        return jsonify({
            'success': True,
            'agents': DELIVERY_AGENTS
        })
        
    except Exception as e:
        logger.error(f"Error getting agents: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get delivery agents'
        }), 500

@app.route('/delivery/ranked-shops', methods=['POST'])
def get_ranked_shops():
    """Get ranked shops based on ingredient match and distance"""
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        dish_name = data.get('dish_name', '').strip()
        user_location = data.get('user_location', {})
        max_distance_km = data.get('max_distance_km', Config.MAX_DELIVERY_DISTANCE_KM)
        min_match_percent = data.get('min_match_percent', Config.MIN_INGREDIENT_MATCH_PERCENT)
        
        # Validate input
        if not dish_name:
            return jsonify({
                'success': False,
                'error': 'Dish name is required'
            }), 400
        
        # Validate user location (use default if not provided)
        if not user_location or not user_location.get('lat') or not user_location.get('lng'):
            user_location = Config.DEFAULT_USER_LOCATION
            logger.info(f"No user location provided, using default: {user_location}")
        
        logger.info(f"Finding ranked shops for: '{dish_name}' within {max_distance_km}km, min {min_match_percent}% match")
        
        # Step 1: Fetch ingredients from Spoonacular API first
        ingredients = get_recipe_ingredients_from_spoonacular_improved(dish_name)
        
        # Try fallback for pizza varieties if Spoonacular fails
        if not ingredients:
            logger.info(f"Trying fallback for pizza varieties in ranked shops: {dish_name}")
            ingredients = get_ingredients_by_dish_name(dish_name)
        
        if not ingredients:
            logger.warning(f"No ingredients found in Spoonacular or fallback for ranked shops: {dish_name}")
            return jsonify({
                'success': False,
                'error': f'No ingredients found for "{dish_name}". Please try a different dish.'
            }), 404
        
        # Step 2: Find and rank shops
        ranked_shops = find_and_rank_shops(user_location, ingredients, MOCK_SHOPS, max_distance_km, min_match_percent)
        
        if not ranked_shops:
            return jsonify({
                'success': False,
                'error': f'No shops found within {max_distance_km}km with at least {min_match_percent}% ingredient match.'
            }), 404
        
        # Step 3: Get top shop
        top_shop = ranked_shops[0]
        
        # Step 4: Assign delivery agent
        delivery_agent = assign_delivery_agent(top_shop["location"])
        
        # Step 5: Format response
        response_data = {
            'success': True,
            'dish': dish_name,
            'ingredients': ingredients,
            'top_shop': {
                'name': top_shop["name"],
                'match_percent': top_shop["match_percent"],
                'distance_km': top_shop["distance_km"],
                'available_ingredients': top_shop["available_ingredients"],
                'missing_ingredients': top_shop["missing_ingredients"]
            },
            'delivery_agent': delivery_agent,
            'all_qualified_shops': ranked_shops
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error getting ranked shops: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get ranked shops. Please try again.'
        }), 500

# ERROR HANDLERS


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# MAIN APPLICATION
# ============================================================================

if __name__ == '__main__':
    print("🚀 Starting We Know API server...")
    print(f"📡 Spoonacular API key: {'✅ Configured' if Config.SPOONACULAR_API_KEY else '❌ Not configured'}")
    print(f"🌐 Server will be available at: http://localhost:8000")
    print(f"🔧 Health check: http://localhost:8000/health")
    
    app.run(debug=False, host='0.0.0.0', port=8000) 