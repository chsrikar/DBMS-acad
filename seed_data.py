"""
========================================
College Canteen Food Ordering System
DBMS Mini Project - Seed Data Script
========================================

This script populates the database with sample data for testing.
Run this after starting the server to have test data available.

Usage:
    python seed_data.py

The script will:
1. Create sample hostels and departments
2. Create a canteen with menu items
3. Create sample students
4. Create delivery personnel
5. Place sample orders
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, init_db
from app.models import (
    Hostel, Department, Canteen, MenuItem, Student,
    DeliveryPersonnel, Order, OrderItem, Payment, DeliveryPickup,
    OrderStatus, OrderType, PaymentMethod, PaymentStatus
)
from passlib.context import CryptContext
from datetime import datetime

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_database():
    """
    Populate the database with sample data.
    
    This demonstrates INSERT operations:
    
    SQL Equivalents:
        INSERT INTO hostels (...) VALUES (...);
        INSERT INTO departments (...) VALUES (...);
        INSERT INTO canteens (...) VALUES (...);
        INSERT INTO menu_items (...) VALUES (...);
        INSERT INTO students (...) VALUES (...);
        INSERT INTO orders (...) VALUES (...);
        INSERT INTO order_items (...) VALUES (...);
        INSERT INTO payments (...) VALUES (...);
    """
    
    # Initialize database (create tables)
    init_db()
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Hostel).first():
            print("⚠️ Database already has data. Skipping seed.")
            return
        
        print("🌱 Seeding database with sample data...")
        
        # ========================================
        # 1. CREATE HOSTELS (Master Data)
        # ========================================
        # SQL: INSERT INTO hostels (hostel_name, hostel_type, address) VALUES (...)
        
        hostels = [
            Hostel(hostel_name="Boys Hostel", hostel_type="BOYS", address="North Campus"),
            Hostel(hostel_name="Girls Hostel", hostel_type="GIRLS", address="South Campus"),
        ]
        db.add_all(hostels)
        db.flush()
        print("✅ Created 2 hostels")
        
        # ========================================
        # 2. CREATE DEPARTMENTS (Master Data)
        # ========================================
        # SQL: INSERT INTO departments (department_name, department_code) VALUES (...)
        
        departments = [
            Department(department_name="Computer Science & Engineering", department_code="CSE"),
            Department(department_name="Electronics & Communication", department_code="ECE"),
            Department(department_name="Mechanical Engineering", department_code="ME"),
            Department(department_name="Civil Engineering", department_code="CE"),
            Department(department_name="Electrical Engineering", department_code="EE"),
        ]
        db.add_all(departments)
        db.flush()
        print("✅ Created 5 departments")
        
        # ========================================
        # 3. CREATE CANTEEN
        # ========================================
        # SQL: INSERT INTO canteens (name, location, ...) VALUES (...)
        
        canteen = Canteen(
            name="Main Canteen",
            location="Central Campus, Ground Floor",
            opening_time="08:00",
            closing_time="22:00",
            is_active=True
        )
        db.add(canteen)
        db.flush()
        print("✅ Created 1 canteen")
        
        # ========================================
        # 4. CREATE MENU ITEMS
        # ========================================
        # SQL: INSERT INTO menu_items (canteen_id, item_name, price, ...) VALUES (...)
        
        menu_items = [
            # Beverages
            MenuItem(canteen_id=canteen.canteen_id, item_name="Lime", description="Refreshing lime juice", 
                     price=12.00, category="Beverages", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Fresh Lime", description="Fresh squeezed lime juice", 
                     price=20.00, category="Beverages", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Tea", description="Hot tea", 
                     price=10.00, category="Beverages", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Coffee", description="Hot coffee", 
                     price=15.00, category="Beverages", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Black Tea", description="Hot black tea", 
                     price=8.00, category="Beverages", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Black Coffee", description="Hot black coffee", 
                     price=10.00, category="Beverages", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Badam Milk", description="Almond flavored milk", 
                     price=20.00, category="Beverages", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Rose Milk", description="Rose flavored milk", 
                     price=20.00, category="Beverages", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Boost Milk", description="Boost flavored milk", 
                     price=20.00, category="Beverages", is_vegetarian=True, is_available=True),
            
            # Snacks
            MenuItem(canteen_id=canteen.canteen_id, item_name="Uzhunnuvada", description="Traditional Kerala vada", 
                     price=12.00, category="Snacks", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Parippuvada", description="Lentil vada", 
                     price=12.00, category="Snacks", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Ullivada", description="Onion vada", 
                     price=12.00, category="Snacks", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Samoosa", description="Crispy fried pastry with filling", 
                     price=14.00, category="Snacks", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Pazhampori", description="Banana fritters", 
                     price=13.00, category="Snacks", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Sweetna", description="Sweet snack", 
                     price=18.00, category="Snacks", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Cream Bun", description="Soft bun with cream filling", 
                     price=15.00, category="Snacks", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Egg Puffs", description="Puff pastry with egg filling", 
                     price=23.00, category="Snacks", is_vegetarian=False, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Chicken Puffs", description="Puff pastry with chicken filling", 
                     price=23.00, category="Snacks", is_vegetarian=False, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Veg Puffs", description="Puff pastry with vegetable filling", 
                     price=18.00, category="Snacks", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Banana Puffs", description="Puff pastry with banana filling", 
                     price=1.00, category="Snacks", is_vegetarian=True, is_available=False),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Chicken Roll", description="Roll with chicken filling", 
                     price=30.00, category="Snacks", is_vegetarian=False, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Sandwich", description="Fresh sandwich", 
                     price=42.00, category="Snacks", is_vegetarian=True, is_available=True),
            MenuItem(canteen_id=canteen.canteen_id, item_name="Burger", description="Delicious burger", 
                     price=42.00, category="Snacks", is_vegetarian=True, is_available=True),
        ]
        db.add_all(menu_items)
        db.flush()
        print(f"✅ Created {len(menu_items)} menu items")
        
        # ========================================
        # 5. CREATE DELIVERY PERSONNEL
        # ========================================
        # SQL: INSERT INTO delivery_personnel (name, phone, is_available) VALUES (...)
        
        delivery_staff = [
            # No demo delivery personnel
        ]
        # db.add_all(delivery_staff)
        # db.flush()
        print("✅ Skipped creating delivery personnel (User Request)")
        
        # ========================================
        # 6. CREATE STUDENTS (SKIPPED)
        # ========================================
        # Users will register manually via the frontend.
        print("ℹ️ Skipping student creation (users will register manually)")
        
        # ========================================
        # 7. CREATE SAMPLE ORDERS (SKIPPED)
        # ========================================
        print("ℹ️ Skipping sample orders (system starts empty)")
        
        db.commit()
        
        print("\n" + "="*50)
        print("🎉 Database seeded successfully!")
        print("="*50)
        print("\nℹ️ No test credentials created. Please register a new user.")
        print("\n🔗 API Documentation: http://localhost:8000/docs")
        print("="*50)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
