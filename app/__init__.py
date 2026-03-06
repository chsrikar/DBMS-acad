"""
========================================
College Canteen Food Ordering System
DBMS Mini Project - Package Initialization
========================================
"""

# Import all models to make them available at package level
from app.models import (
    Student, Hostel, Department, Canteen,
    MenuItem, Order, OrderItem, DeliveryPickup,
    DeliveryPersonnel, Payment,
    OrderStatus, OrderType, PaymentMethod, PaymentStatus
)

from app.database import Base, engine, SessionLocal, get_db, init_db

__all__ = [
    # Models
    "Student", "Hostel", "Department", "Canteen",
    "MenuItem", "Order", "OrderItem", "DeliveryPickup",
    "DeliveryPersonnel", "Payment",
    # Enums
    "OrderStatus", "OrderType", "PaymentMethod", "PaymentStatus",
    # Database
    "Base", "engine", "SessionLocal", "get_db", "init_db"
]
