"""
========================================
College Canteen Food Ordering System
DBMS Mini Project - ORM Models
========================================

This module defines all database tables using SQLAlchemy ORM.
Each class represents a table in the database.

DBMS CONCEPTS DEMONSTRATED:
1. Primary Keys (PK) - Unique identifier for each record
2. Foreign Keys (FK) - Establish relationships between tables
3. Relationships - One-to-Many, Many-to-One, One-to-One
4. Constraints - NOT NULL, UNIQUE, CHECK
5. Normalization - Tables designed up to 3NF
6. Referential Integrity - Cascade actions on delete/update

NORMALIZATION ANALYSIS:
- 1NF: All attributes are atomic (no multi-valued attributes)
- 2NF: No partial dependencies (all non-key attributes depend on entire PK)
- 3NF: No transitive dependencies (non-key attributes don't depend on other non-key attributes)
"""

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean,
    ForeignKey, Enum, Text, CheckConstraint, UniqueConstraint,
    func
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


# ========================================
# ENUMERATIONS (Domain Constraints)
# ========================================
# Enums ensure data integrity by restricting values to a predefined set
# This implements CHECK constraints at the application level

class OrderStatus(enum.Enum):
    """
    Valid order status transitions:
    PLACED → PREPARING → READY → DELIVERED
    
    Note: Status can only move forward, never backward
    This represents a state machine in the database
    """
    PLACED = "PLACED"           # Order just created
    PREPARING = "PREPARING"     # Kitchen is preparing
    READY = "READY"             # Ready for pickup/delivery
    DELIVERED = "DELIVERED"     # Order completed
    CANCELLED = "CANCELLED"     # Order cancelled


class OrderType(enum.Enum):
    """Type of order fulfillment"""
    PICKUP = "PICKUP"       # Student picks up from canteen
    DELIVERY = "DELIVERY"   # Delivered to student location


class PaymentMethod(enum.Enum):
    """Supported payment methods"""
    CASH = "CASH"   # Cash payment
    UPI = "UPI"     # UPI payment (GooglePay, PhonePe, etc.)


class PaymentStatus(enum.Enum):
    """Payment processing status"""
    PENDING = "PENDING"       # Payment not yet made
    COMPLETED = "COMPLETED"   # Payment successful
    FAILED = "FAILED"         # Payment failed
    REFUNDED = "REFUNDED"     # Payment refunded


# ========================================
# MASTER TABLES (Reference/Lookup Tables)
# ========================================
# These tables store reference data with minimal dependencies
# They help achieve 3NF by eliminating transitive dependencies


class Hostel(Base):
    """
    HOSTEL TABLE - Master Data
    ========================================
    Purpose: Store hostel information (reference data)
    
    Normalization Justification:
    - Separated from Students to avoid data redundancy
    - If hostel details change, update in one place only
    - Achieves 3NF by eliminating transitive dependency
    
    Relationships:
    - One Hostel → Many Students (1:M)
    
    SQL Equivalent:
        CREATE TABLE hostels (
            hostel_id INT PRIMARY KEY AUTO_INCREMENT,
            hostel_name VARCHAR(100) NOT NULL UNIQUE,
            hostel_type VARCHAR(20) NOT NULL CHECK (hostel_type IN ('BOYS', 'GIRLS', 'CO-ED')),
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    __tablename__ = "hostels"
    
    # Primary Key
    hostel_id = Column(Integer, primary_key=True, autoincrement=True,
                       comment="Primary Key - Unique hostel identifier")
    
    # Attributes
    hostel_name = Column(String(100), nullable=False, unique=True,
                         comment="Hostel name - must be unique")
    hostel_type = Column(String(20), nullable=False,
                         comment="Type: BOYS, GIRLS, or CO-ED")
    address = Column(Text,
                     comment="Physical address of the hostel")
    
    # Audit field
    created_at = Column(DateTime, default=datetime.utcnow,
                        comment="Record creation timestamp")
    
    # Relationship: One Hostel has Many Students
    students = relationship("Student", back_populates="hostel")
    
    def __repr__(self):
        return f"<Hostel(id={self.hostel_id}, name='{self.hostel_name}')>"


class Department(Base):
    """
    DEPARTMENT TABLE - Master Data
    ========================================
    Purpose: Store academic department information
    
    Normalization Justification:
    - Separated from Students to avoid storing department details repeatedly
    - Changes to department info need only one update
    - Achieves 3NF
    
    Relationships:
    - One Department → Many Students (1:M)
    
    SQL Equivalent:
        CREATE TABLE departments (
            department_id INT PRIMARY KEY AUTO_INCREMENT,
            department_name VARCHAR(100) NOT NULL UNIQUE,
            department_code VARCHAR(10) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    __tablename__ = "departments"
    
    # Primary Key
    department_id = Column(Integer, primary_key=True, autoincrement=True,
                           comment="Primary Key - Unique department identifier")
    
    # Attributes
    department_name = Column(String(100), nullable=False, unique=True,
                             comment="Full department name")
    department_code = Column(String(10), nullable=False, unique=True,
                             comment="Short code (e.g., CSE, ECE, ME)")
    
    # Audit field
    created_at = Column(DateTime, default=datetime.utcnow,
                        comment="Record creation timestamp")
    
    # Relationship: One Department has Many Students
    students = relationship("Student", back_populates="department")
    
    def __repr__(self):
        return f"<Department(id={self.department_id}, code='{self.department_code}')>"


class DeliveryPersonnel(Base):
    """
    DELIVERY PERSONNEL TABLE
    ========================================
    Purpose: Store delivery staff information
    
    Relationships:
    - One Personnel → Many Deliveries (1:M)
    
    SQL Equivalent:
        CREATE TABLE delivery_personnel (
            personnel_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(15) NOT NULL UNIQUE,
            is_available BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    __tablename__ = "delivery_personnel"
    
    # Primary Key
    personnel_id = Column(Integer, primary_key=True, autoincrement=True,
                          comment="Primary Key - Unique personnel identifier")
    
    # Attributes
    name = Column(String(100), nullable=False,
                  comment="Full name of delivery person")
    roll_number = Column(String(20), nullable=False, unique=True,
                         comment="College roll number")
    email = Column(String(100), nullable=False, unique=True,
                   comment="College email address")
    phone = Column(String(15), nullable=False, unique=True,
                   comment="Contact phone number - unique")
    password_hash = Column(String(255), nullable=False,
                           comment="Hashed password")
    is_available = Column(Boolean, default=True,
                          comment="Availability status for new deliveries")
    
    # Audit field
    created_at = Column(DateTime, default=datetime.utcnow,
                        comment="Record creation timestamp")
    
    # Relationship: One Personnel handles Many Deliveries
    deliveries = relationship("DeliveryPickup", back_populates="personnel")
    
    def __repr__(self):
        return f"<DeliveryPersonnel(id={self.personnel_id}, name='{self.name}')>"


# ========================================
# STUDENT TABLE (Core Entity)
# ========================================

class Student(Base):
    """
    STUDENT TABLE
    ========================================
    Purpose: Store registered student information
    
    Normalization Analysis:
    - 1NF: All attributes are atomic (single values only)
    - 2NF: All attributes depend on the primary key (student_id)
    - 3NF: hostel_id and department_id are FKs to separate tables
           This eliminates transitive dependencies
    
    Relationships:
    - Many Students → One Hostel (M:1)
    - Many Students → One Department (M:1)
    - One Student → Many Orders (1:M)
    
    Constraints:
    - PRIMARY KEY: student_id
    - UNIQUE: email, roll_number
    - FOREIGN KEY: hostel_id → hostels.hostel_id
    - FOREIGN KEY: department_id → departments.department_id
    - NOT NULL: name, email, roll_number, password_hash
    
    SQL Equivalent:
        CREATE TABLE students (
            student_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            roll_number VARCHAR(20) NOT NULL UNIQUE,
            phone VARCHAR(15),
            password_hash VARCHAR(255) NOT NULL,
            hostel_id INT,
            department_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (hostel_id) REFERENCES hostels(hostel_id),
            FOREIGN KEY (department_id) REFERENCES departments(department_id)
        );
    """
    __tablename__ = "students"
    
    # Primary Key
    student_id = Column(Integer, primary_key=True, autoincrement=True,
                        comment="Primary Key - Auto-incrementing unique identifier")
    
    # Core Attributes
    name = Column(String(100), nullable=False,
                  comment="Student's full name")
    email = Column(String(100), nullable=False, unique=True,
                   comment="Email address - used for login - UNIQUE constraint")
    roll_number = Column(String(20), nullable=False, unique=True,
                         comment="College roll number - UNIQUE constraint")
    phone = Column(String(15),
                   comment="Contact phone number (optional)")
    password_hash = Column(String(255), nullable=False,
                           comment="Hashed password for security")
    
    # Foreign Keys (References to Master Tables)
    hostel_id = Column(Integer, ForeignKey("hostels.hostel_id"),
                       comment="FK → hostels.hostel_id - Student's hostel")
    department_id = Column(Integer, ForeignKey("departments.department_id"),
                           comment="FK → departments.department_id - Student's department")
    
    # Audit Fields
    created_at = Column(DateTime, default=datetime.utcnow,
                        comment="Timestamp when record was created")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                        comment="Timestamp of last update")
    
    # ========================================
    # ORM RELATIONSHIPS
    # ========================================
    # These define how SQLAlchemy loads related objects
    # back_populates creates bidirectional relationship
    
    hostel = relationship("Hostel", back_populates="students")
    department = relationship("Department", back_populates="students")
    orders = relationship("Order", back_populates="student", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Student(id={self.student_id}, roll='{self.roll_number}', name='{self.name}')>"


# ========================================
# CANTEEN & MENU TABLES
# ========================================

class Canteen(Base):
    """
    CANTEEN TABLE
    ========================================
    Purpose: Store canteen/cafeteria information
    
    Relationships:
    - One Canteen → Many Menu Items (1:M)
    - One Canteen → Many Orders (1:M)
    
    SQL Equivalent:
        CREATE TABLE canteens (
            canteen_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            location VARCHAR(200),
            opening_time TIME,
            closing_time TIME,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    __tablename__ = "canteens"
    
    # Primary Key
    canteen_id = Column(Integer, primary_key=True, autoincrement=True,
                        comment="Primary Key - Unique canteen identifier")
    
    # Attributes
    name = Column(String(100), nullable=False,
                  comment="Canteen name")
    location = Column(String(200),
                      comment="Physical location in campus")
    opening_time = Column(String(10),
                          comment="Opening time (e.g., '08:00')")
    closing_time = Column(String(10),
                          comment="Closing time (e.g., '22:00')")
    is_active = Column(Boolean, default=True,
                       comment="Whether canteen is currently operational")
    
    # Audit field
    created_at = Column(DateTime, default=datetime.utcnow,
                        comment="Record creation timestamp")
    
    # Relationships
    menu_items = relationship("MenuItem", back_populates="canteen", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="canteen")
    
    def __repr__(self):
        return f"<Canteen(id={self.canteen_id}, name='{self.name}')>"


class MenuItem(Base):
    """
    MENU ITEM TABLE
    ========================================
    Purpose: Store food items available in canteens
    
    Normalization Analysis:
    - Separated from Canteen to handle many items per canteen
    - Price stored here (not in order_items) as the "current" price
    - Order_items stores the price at time of order (historical price)
    
    Relationships:
    - Many Menu Items → One Canteen (M:1)
    - One Menu Item → Many Order Items (1:M)
    
    Constraints:
    - FOREIGN KEY: canteen_id → canteens.canteen_id
    - CHECK: price > 0 (price must be positive)
    
    SQL Equivalent:
        CREATE TABLE menu_items (
            item_id INT PRIMARY KEY AUTO_INCREMENT,
            canteen_id INT NOT NULL,
            item_name VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL CHECK (price > 0),
            category VARCHAR(50),
            is_vegetarian BOOLEAN DEFAULT TRUE,
            is_available BOOLEAN DEFAULT TRUE,
            image_url VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (canteen_id) REFERENCES canteens(canteen_id)
        );
    """
    __tablename__ = "menu_items"
    
    # Primary Key
    item_id = Column(Integer, primary_key=True, autoincrement=True,
                     comment="Primary Key - Unique item identifier")
    
    # Foreign Key
    canteen_id = Column(Integer, ForeignKey("canteens.canteen_id"), nullable=False,
                        comment="FK → canteens.canteen_id - Which canteen offers this item")
    
    # Attributes
    item_name = Column(String(100), nullable=False,
                       comment="Name of the food item")
    description = Column(Text,
                         comment="Detailed description of the item")
    price = Column(Float, nullable=False,
                   comment="Current price in INR - must be positive")
    category = Column(String(50),
                      comment="Category: Breakfast, Lunch, Snacks, Beverages, etc.")
    is_vegetarian = Column(Boolean, default=True,
                           comment="Whether item is vegetarian")
    is_available = Column(Boolean, default=True,
                          comment="Current availability status")
    image_url = Column(String(500),
                       comment="URL to item image")
    
    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow,
                        comment="Record creation timestamp")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                        comment="Last update timestamp")
    
    # Check constraint for positive price
    __table_args__ = (
        CheckConstraint('price > 0', name='check_positive_price'),
    )
    
    # Relationships
    canteen = relationship("Canteen", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")
    
    def __repr__(self):
        return f"<MenuItem(id={self.item_id}, name='{self.item_name}', price={self.price})>"


# ========================================
# ORDER MANAGEMENT TABLES
# ========================================

class Order(Base):
    """
    ORDER TABLE (Header)
    ========================================
    Purpose: Store order header information
    
    Normalization Analysis:
    - This is the "header" table for orders
    - Contains order-level information (who, when, status, total)
    - Line items are in separate Order_Items table (1NF compliance)
    
    Relationships:
    - Many Orders → One Student (M:1)
    - Many Orders → One Canteen (M:1)
    - One Order → Many Order Items (1:M)
    - One Order → One Payment (1:1)
    - One Order → One Delivery/Pickup (1:1)
    
    Status Workflow:
    PLACED → PREPARING → READY → DELIVERED
                    ↘ CANCELLED ↙
    
    SQL Equivalent:
        CREATE TABLE orders (
            order_id INT PRIMARY KEY AUTO_INCREMENT,
            student_id INT NOT NULL,
            canteen_id INT NOT NULL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            order_status ENUM('PLACED','PREPARING','READY','DELIVERED','CANCELLED') DEFAULT 'PLACED',
            order_type ENUM('PICKUP', 'DELIVERY') NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
            special_instructions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (canteen_id) REFERENCES canteens(canteen_id)
        );
    """
    __tablename__ = "orders"
    
    # Primary Key
    order_id = Column(Integer, primary_key=True, autoincrement=True,
                      comment="Primary Key - Unique order identifier")
    
    # Foreign Keys
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False,
                        comment="FK → students.student_id - Who placed the order")
    canteen_id = Column(Integer, ForeignKey("canteens.canteen_id"), nullable=False,
                        comment="FK → canteens.canteen_id - Which canteen")
    
    # Order Details
    order_date = Column(DateTime, default=datetime.utcnow,
                        comment="When the order was placed")
    order_status = Column(Enum(OrderStatus), default=OrderStatus.PLACED,
                          comment="Current status: PLACED, PREPARING, READY, DELIVERED, CANCELLED")
    order_type = Column(Enum(OrderType), nullable=False,
                        comment="PICKUP or DELIVERY")
    total_amount = Column(Float, default=0.0,
                          comment="Total bill amount (auto-calculated)")
    special_instructions = Column(Text,
                                  comment="Any special requests from student")
    
    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow,
                        comment="Record creation timestamp")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,
                        comment="Last update timestamp")
    
    # Relationships
    student = relationship("Student", back_populates="orders")
    canteen = relationship("Canteen", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False, cascade="all, delete-orphan")
    delivery = relationship("DeliveryPickup", back_populates="order", uselist=False, cascade="all, delete-orphan")
    
    def calculate_total(self):
        """
        Calculate the total order amount from order items.
        
        SQL Equivalent:
            SELECT SUM(subtotal) FROM order_items WHERE order_id = ?;
        """
        return sum(item.subtotal for item in self.order_items)
    
    def __repr__(self):
        return f"<Order(id={self.order_id}, student_id={self.student_id}, status={self.order_status.value})>"


class OrderItem(Base):
    """
    ORDER ITEM TABLE (Line Items / Junction Table)
    ========================================
    Purpose: Store individual items within an order
    
    Normalization Analysis:
    - This table achieves 1NF by storing one item per row
    - Stores price at time of order (unit_price) for historical accuracy
    - Subtotal = quantity × unit_price (derived but stored for performance)
    
    Relationships:
    - Many Order Items → One Order (M:1)
    - Many Order Items → One Menu Item (M:1)
    
    Why store unit_price separately?
    - Menu prices can change over time
    - We need to preserve the price at which the order was placed
    - This is a common pattern for transactional data
    
    SQL Equivalent:
        CREATE TABLE order_items (
            order_item_id INT PRIMARY KEY AUTO_INCREMENT,
            order_id INT NOT NULL,
            item_id INT NOT NULL,
            quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
            unit_price DECIMAL(10,2) NOT NULL,
            subtotal DECIMAL(10,2) NOT NULL,
            notes TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
        );
    """
    __tablename__ = "order_items"
    
    # Primary Key
    order_item_id = Column(Integer, primary_key=True, autoincrement=True,
                           comment="Primary Key - Unique order item identifier")
    
    # Foreign Keys
    order_id = Column(Integer, ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False,
                      comment="FK → orders.order_id - Which order this belongs to")
    item_id = Column(Integer, ForeignKey("menu_items.item_id"), nullable=False,
                     comment="FK → menu_items.item_id - Which menu item")
    
    # Line Item Details
    quantity = Column(Integer, nullable=False, default=1,
                      comment="Number of items ordered - must be positive")
    unit_price = Column(Float, nullable=False,
                        comment="Price per unit at time of order")
    subtotal = Column(Float, nullable=False,
                      comment="quantity × unit_price (stored for quick access)")
    notes = Column(Text,
                   comment="Special notes for this item (e.g., 'less spicy')")
    
    # Check constraints
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_positive_quantity'),
    )
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(id={self.order_item_id}, item_id={self.item_id}, qty={self.quantity})>"


# ========================================
# DELIVERY & PAYMENT TABLES
# ========================================

class DeliveryPickup(Base):
    """
    DELIVERY/PICKUP TABLE
    ========================================
    Purpose: Store delivery or pickup details for an order
    
    Relationships:
    - One Delivery → One Order (1:1)
    - Many Deliveries → One Personnel (M:1)
    
    Design Notes:
    - Created as a separate table to handle optional delivery info
    - Not all orders have delivery details (pickup orders don't need delivery personnel)
    - This maintains 3NF by keeping optional data separate
    
    SQL Equivalent:
        CREATE TABLE delivery_pickups (
            delivery_id INT PRIMARY KEY AUTO_INCREMENT,
            order_id INT NOT NULL UNIQUE,
            delivery_address TEXT,
            personnel_id INT,
            estimated_time VARCHAR(50),
            actual_delivery_time TIMESTAMP,
            is_delivered BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (personnel_id) REFERENCES delivery_personnel(personnel_id)
        );
    """
    __tablename__ = "delivery_pickups"
    
    # Primary Key
    delivery_id = Column(Integer, primary_key=True, autoincrement=True,
                         comment="Primary Key - Unique delivery record identifier")
    
    # Foreign Keys
    order_id = Column(Integer, ForeignKey("orders.order_id", ondelete="CASCADE"),
                      nullable=False, unique=True,
                      comment="FK → orders.order_id - UNIQUE for 1:1 relationship")
    personnel_id = Column(Integer, ForeignKey("delivery_personnel.personnel_id"),
                          comment="FK → delivery_personnel.personnel_id - Assigned delivery person")
    
    # Delivery Details
    delivery_address = Column(Text,
                              comment="Delivery location (hostel room, etc.)")
    estimated_time = Column(String(50),
                            comment="Estimated delivery/pickup time")
    actual_delivery_time = Column(DateTime,
                                  comment="When actually delivered")
    is_delivered = Column(Boolean, default=False,
                          comment="Delivery confirmation status")
    
    # Audit field
    created_at = Column(DateTime, default=datetime.utcnow,
                        comment="Record creation timestamp")
    
    # Relationships
    order = relationship("Order", back_populates="delivery")
    personnel = relationship("DeliveryPersonnel", back_populates="deliveries")
    
    def __repr__(self):
        return f"<DeliveryPickup(id={self.delivery_id}, order_id={self.order_id}, delivered={self.is_delivered})>"


class Payment(Base):
    """
    PAYMENT TABLE
    ========================================
    Purpose: Store payment/billing information for orders
    
    Relationships:
    - One Payment → One Order (1:1)
    
    Design Notes:
    - Separated from Order table for better normalization
    - Allows tracking payment attempts and status changes
    - Supports multiple payment methods
    - Stores UPI payment screenshots for verification
    
    SQL Equivalent:
        CREATE TABLE payments (
            payment_id INT PRIMARY KEY AUTO_INCREMENT,
            order_id INT NOT NULL UNIQUE,
            amount_paid DECIMAL(10,2) NOT NULL,
            payment_method ENUM('CASH', 'UPI') NOT NULL,
            payment_status ENUM('PENDING', 'COMPLETED', 'FAILED', 'REFUNDED') DEFAULT 'PENDING',
            transaction_id VARCHAR(100),
            payment_screenshot TEXT,
            payment_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
        );
    """
    __tablename__ = "payments"
    
    # Primary Key
    payment_id = Column(Integer, primary_key=True, autoincrement=True,
                        comment="Primary Key - Unique payment identifier")
    
    # Foreign Key
    order_id = Column(Integer, ForeignKey("orders.order_id", ondelete="CASCADE"),
                      nullable=False, unique=True,
                      comment="FK → orders.order_id - UNIQUE for 1:1 relationship")
    
    # Payment Details
    amount_paid = Column(Float, nullable=False,
                         comment="Amount paid/to be paid")
    payment_method = Column(Enum(PaymentMethod), nullable=False,
                            comment="CASH or UPI")
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING,
                            comment="PENDING, COMPLETED, FAILED, or REFUNDED")
    transaction_id = Column(String(100),
                            comment="UPI transaction ID (for UPI payments)")
    payment_screenshot = Column(Text,
                                comment="Base64 encoded screenshot of UPI payment")
    payment_date = Column(DateTime,
                          comment="When payment was completed")
    
    # Audit field
    created_at = Column(DateTime, default=datetime.utcnow,
                        comment="Record creation timestamp")
    
    # Relationship
    order = relationship("Order", back_populates="payment")
    
    def __repr__(self):
        return f"<Payment(id={self.payment_id}, order_id={self.order_id}, status={self.payment_status.value})>"


# ========================================
# TABLE SUMMARY FOR VIVA
# ========================================
"""
ENTITY-RELATIONSHIP SUMMARY:

1. STUDENTS (student_id PK)
   - References: hostels (FK), departments (FK)
   - Referenced by: orders

2. HOSTELS (hostel_id PK)
   - Referenced by: students

3. DEPARTMENTS (department_id PK)
   - Referenced by: students

4. CANTEENS (canteen_id PK)
   - Referenced by: menu_items, orders

5. MENU_ITEMS (item_id PK)
   - References: canteens (FK)
   - Referenced by: order_items

6. ORDERS (order_id PK)
   - References: students (FK), canteens (FK)
   - Referenced by: order_items, payments, delivery_pickups

7. ORDER_ITEMS (order_item_id PK)
   - References: orders (FK), menu_items (FK)

8. DELIVERY_PICKUPS (delivery_id PK)
   - References: orders (FK), delivery_personnel (FK)

9. DELIVERY_PERSONNEL (personnel_id PK)
   - Referenced by: delivery_pickups

10. PAYMENTS (payment_id PK)
    - References: orders (FK)


RELATIONSHIP TYPES:
- One-to-Many (1:M): Hostel→Students, Department→Students, Student→Orders, 
                     Canteen→MenuItems, Order→OrderItems
- Many-to-One (M:1): Inverse of above
- One-to-One (1:1): Order→Payment, Order→DeliveryPickup
"""
