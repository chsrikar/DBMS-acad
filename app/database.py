"""
========================================
College Canteen Food Ordering System
DBMS Mini Project - Database Configuration
========================================

This module handles database connection and session management using SQLAlchemy.

DBMS Concepts Demonstrated:
- Database Connection Management
- Session Factory Pattern
- ORM Engine Configuration
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ========================================
# DATABASE URL CONFIGURATION
# ========================================
# The DATABASE_URL specifies the database connection string
# Format: dialect+driver://username:password@host:port/database_name
#
# Examples:
# - MySQL: mysql+pymysql://root:password@localhost:3306/canteen_db
# - PostgreSQL: postgresql://postgres:password@localhost:5432/canteen_db
# - SQLite: sqlite:///./canteen.db
# ========================================

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./canteen.db")

# ========================================
# SQLALCHEMY ENGINE CONFIGURATION
# ========================================
# The engine is the starting point for any SQLAlchemy application.
# It maintains a pool of connections to the database.
#
# Parameters:
# - connect_args: Additional arguments passed to the database driver
# - poolclass: Connection pool strategy (StaticPool for SQLite)
# - echo: Set to True to log all SQL statements (useful for debugging/learning)
# ========================================

if DATABASE_URL.startswith("sqlite"):
    # SQLite specific configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # Required for SQLite with FastAPI
        poolclass=StaticPool,
        echo=True  # Enable SQL logging for academic demonstration
    )
else:
    # MySQL/PostgreSQL configuration
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,  # Number of connections to keep in the pool
        max_overflow=20,  # Additional connections allowed beyond pool_size
        pool_pre_ping=True,  # Verify connections before using
        echo=True  # Enable SQL logging
    )

# ========================================
# SESSION FACTORY
# ========================================
# SessionLocal is a factory for creating new Session objects.
# Each Session manages persistence operations for ORM-mapped objects.
#
# Parameters:
# - autocommit=False: Changes are not automatically committed
# - autoflush=False: Changes are not automatically flushed to DB
# - bind=engine: Associate sessions with our database engine
# ========================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ========================================
# DECLARATIVE BASE
# ========================================
# Base class for all ORM models.
# All model classes will inherit from this Base.
# This is the foundation for SQLAlchemy's declarative mapping system.
# ========================================

Base = declarative_base()


def get_db():
    """
    Dependency function for FastAPI to provide database sessions.
    
    This implements the Unit of Work pattern:
    1. Create a new session for each request
    2. Yield the session for use in the request
    3. Close the session after the request completes
    
    Usage in FastAPI:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables.
    
    This function:
    1. Imports all models to register them with the Base
    2. Creates all tables that don't exist yet
    
    SQL Equivalent:
        CREATE TABLE IF NOT EXISTS students (...);
        CREATE TABLE IF NOT EXISTS canteens (...);
        ... (for all tables)
    """
    # Import all models to register them with Base
    from app.models import (
        Student, Hostel, Department, Canteen,
        MenuItem, Order, OrderItem, DeliveryPickup,
        DeliveryPersonnel, Payment
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


def drop_all_tables():
    """
    Drop all tables from the database.
    WARNING: This will delete all data!
    
    SQL Equivalent:
        DROP TABLE IF EXISTS payments;
        DROP TABLE IF EXISTS delivery_pickups;
        ... (for all tables in correct order respecting FK constraints)
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️ All database tables dropped!")
