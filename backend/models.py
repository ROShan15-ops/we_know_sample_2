from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import Config

# Database setup
engine = create_engine(
    Config.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    
    # Relationships
    recent_searches = relationship("RecentSearch", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    saved_addresses = relationship("SavedAddress", back_populates="user", cascade="all, delete-orphan")
    user_preferences = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    allergies = relationship("UserAllergy", back_populates="user", cascade="all, delete-orphan")


class RecentSearch(Base):
    __tablename__ = "recent_searches"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dish_name = Column(String, nullable=False)
    search_timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="recent_searches")


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dish_name = Column(String, nullable=False)
    ingredients = Column(JSON, nullable=False)  # Store ingredients as JSON
    servings = Column(Integer, default=2)
    order_timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")  # pending, completed, cancelled
    
    # Relationship
    user = relationship("User", back_populates="orders")


class SavedAddress(Base):
    __tablename__ = "saved_addresses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    address_type = Column(String, nullable=False)  # home, work, other
    address_line1 = Column(String, nullable=False)
    address_line2 = Column(String)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="saved_addresses")


class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    dietary_restrictions = Column(JSON, default=list)  # Store as JSON array
    favorite_cuisines = Column(JSON, default=list)  # Store as JSON array
    serving_size_preference = Column(Integer, default=2)
    notifications_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="user_preferences")


class UserAllergy(Base):
    __tablename__ = "user_allergies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    allergy_name = Column(String, nullable=False)
    allergy_type = Column(String, nullable=False)  # common, custom
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="allergies")

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 