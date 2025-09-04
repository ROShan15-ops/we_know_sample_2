import bcrypt
import jwt
import logging
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from models import get_db, User
from config import Config

logger = logging.getLogger(__name__)

def create_access_token(data: dict):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify JWT token"""
    try:
        logger.info(f"Verifying token with secret key: {Config.JWT_SECRET_KEY[:20]}...")
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        logger.info(f"Token verification successful, user_id: {payload.get('user_id')}")
        return payload
    except jwt.InvalidTokenError as e:
        logger.error(f"Token verification failed: {e}")
        return None

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Authorization header missing'}), 401
        
        try:
            token = auth_header.split(' ')[1]  # Bearer <token>
            payload = verify_token(token)
            
            if not payload:
                return jsonify({'error': 'Invalid token'}), 401
            
            # Add user info to request
            request.user = payload
            return f(*args, **kwargs)
            
        except IndexError:
            return jsonify({'error': 'Invalid authorization header format'}), 401
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return jsonify({'error': 'Authentication failed'}), 401
    
    return decorated_function

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_user(db, name: str, email: str, password: str):
    """Create a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return None, "User with this email already exists"
    
    # Hash password
    hashed_password = hash_password(password)
    
    # Create user
    user = User(
        name=name,
        email=email,
        password_hash=hashed_password
    )
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user, None
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {e}")
        return None, "Failed to create user"

def authenticate_user(db, email: str, password: str):
    """Authenticate user with email and password"""
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return None, "Invalid email or password"
    
    if not verify_password(password, user.password_hash):
        return None, "Invalid email or password"
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    return user, None 