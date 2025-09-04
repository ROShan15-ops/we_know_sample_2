#!/usr/bin/env python3

from flask import Flask, request, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test_ingredients():
    try:
        data = request.get_json()
        dish_name = data.get('dish_name', '').strip()
        
        logger.info(f"Testing dish: {dish_name}")
        
        # Import and test the function
        from ingredient_service import get_ingredients_by_dish_name
        
        logger.info(f"Calling get_ingredients_by_dish_name for: {dish_name}")
        ingredients = get_ingredients_by_dish_name(dish_name)
        
        logger.info(f"Result: {ingredients}")
        logger.info(f"Type: {type(ingredients)}")
        logger.info(f"Length: {len(ingredients) if ingredients else 0}")
        logger.info(f"Bool: {bool(ingredients)}")
        
        return jsonify({
            'success': True,
            'ingredients': ingredients,
            'type': str(type(ingredients)),
            'length': len(ingredients) if ingredients else 0,
            'bool': bool(ingredients)
        })
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=8001) 