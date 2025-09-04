import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask Configuration
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY', '9fa1698f628d41f0af451651e77bbb71')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./weknow.db')
    
    # API Configuration
    SPOONACULAR_BASE_URL = 'https://api.spoonacular.com/recipes'
    
    # Delivery System Configuration
    MAX_DELIVERY_DISTANCE_KM = 5
    MIN_INGREDIENT_MATCH_PERCENT = 60
    DEFAULT_USER_LOCATION = {"lat": 37.7749, "lng": -122.4194}  # San Francisco
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'weknow-super-secret-jwt-key-2024-secure-and-unique')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = 24 