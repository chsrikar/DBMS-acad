"""
========================================
College Canteen Food Ordering System
DBMS Mini Project - CRUD Operations
========================================

CRUD = Create, Read, Update, Delete

This module implements database operations using SQLAlchemy ORM.
Each function includes the equivalent SQL query in comments
for academic reference.

DBMS Concepts Demonstrated:
1. INSERT operations (Create)
2. SELECT operations with WHERE, JOIN (Read)
3. UPDATE operations with conditions
4. DELETE operations with CASCADE
5. Aggregate functions (SUM, COUNT, GROUP BY)
6. Subqueries and JOIN operations
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_, desc
from datetime import datetime, date
from typing import List, Optional
from passlib.context import CryptContext

from app.models import (
    Student, Hostel, Department, Canteen,
    MenuItem, Order, OrderItem, DeliveryPickup,
    DeliveryPersonnel, Payment,
    OrderStatus, OrderType, PaymentMethod, PaymentStatus
)
from app import schemas

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ========================================
# HOSTEL CRUD OPERATIONS
# ========================================

def create_hostel(db: Session, hostel: schemas.HostelCreate) -> Hostel:
    """
    Create a new hostel record.
    
    SQL Equivalent:
        INSERT INTO hostels (hostel_name, hostel_type, address, created_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP);
    """
    db_hostel = Hostel(**hostel.model_dump())
    db.add(db_hostel)
    db.commit()
    db.refresh(db_hostel)
    return db_hostel


def get_hostels(db: Session) -> List[Hostel]:
    """
    Get all hostels.
    
    SQL Equivalent:
        SELECT * FROM hostels ORDER BY hostel_name;
    """
    return db.query(Hostel).order_by(Hostel.hostel_name).all()


def get_hostel(db: Session, hostel_id: int) -> Optional[Hostel]:
    """
    Get hostel by ID.
    
    SQL Equivalent:
        SELECT * FROM hostels WHERE hostel_id = ?;
    """
    return db.query(Hostel).filter(Hostel.hostel_id == hostel_id).first()


# ========================================
# DEPARTMENT CRUD OPERATIONS
# ========================================

def create_department(db: Session, department: schemas.DepartmentCreate) -> Department:
    """
    Create a new department record.
    
    SQL Equivalent:
        INSERT INTO departments (department_name, department_code, created_at)
        VALUES (?, ?, CURRENT_TIMESTAMP);
    """
    db_department = Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


def get_departments(db: Session) -> List[Department]:
    """
    Get all departments.
    
    SQL Equivalent:
        SELECT * FROM departments ORDER BY department_code;
    """
    return db.query(Department).order_by(Department.department_code).all()


def get_department(db: Session, department_id: int) -> Optional[Department]:
    """
    Get department by ID.
    
    SQL Equivalent:
        SELECT * FROM departments WHERE department_id = ?;
    """
    return db.query(Department).filter(Department.department_id == department_id).first()


# ========================================
# STUDENT CRUD OPERATIONS
# ========================================

def create_student(db: Session, student: schemas.StudentCreate) -> Student:
    """
    Create a new student record with hashed password.
    
    SQL Equivalent:
        INSERT INTO students (name, email, roll_number, phone, password_hash, 
                             hostel_id, department_id, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    """
    hashed_password = pwd_context.hash(student.password)
    db_student = Student(
        name=student.name,
        email=student.email,
        roll_number=student.roll_number,
        phone=student.phone,
        password_hash=hashed_password,
        hostel_id=student.hostel_id,
        department_id=student.department_id
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_student(db: Session, student_id: int) -> Optional[Student]:
    """
    Get student by ID with related hostel and department.
    
    SQL Equivalent (with JOIN):
        SELECT s.*, h.*, d.*
        FROM students s
        LEFT JOIN hostels h ON s.hostel_id = h.hostel_id
        LEFT JOIN departments d ON s.department_id = d.department_id
        WHERE s.student_id = ?;
    """
    return db.query(Student)\
        .options(joinedload(Student.hostel), joinedload(Student.department))\
        .filter(Student.student_id == student_id)\
        .first()


def get_student_by_email(db: Session, email: str) -> Optional[Student]:
    """
    Get student by email (for login).
    
    SQL Equivalent:
        SELECT * FROM students WHERE email = ?;
    """
    return db.query(Student).filter(Student.email == email).first()


def get_student_by_roll_number(db: Session, roll_number: str) -> Optional[Student]:
    """
    Get student by roll number.
    
    SQL Equivalent:
        SELECT * FROM students WHERE roll_number = ?;
    """
    return db.query(Student).filter(Student.roll_number == roll_number).first()


def get_students(db: Session, skip: int = 0, limit: int = 100) -> List[Student]:
    """
    Get all students with pagination.
    
    SQL Equivalent:
        SELECT s.*, h.hostel_name, d.department_name
        FROM students s
        LEFT JOIN hostels h ON s.hostel_id = h.hostel_id
        LEFT JOIN departments d ON s.department_id = d.department_id
        ORDER BY s.name
        LIMIT ? OFFSET ?;
    """
    return db.query(Student)\
        .options(joinedload(Student.hostel), joinedload(Student.department))\
        .order_by(Student.name)\
        .offset(skip).limit(limit)\
        .all()


def update_student(db: Session, student_id: int, student_update: schemas.StudentUpdate) -> Optional[Student]:
    """
    Update student details.
    
    SQL Equivalent:
        UPDATE students
        SET name = COALESCE(?, name),
            phone = COALESCE(?, phone),
            hostel_id = COALESCE(?, hostel_id),
            department_id = COALESCE(?, department_id),
            updated_at = CURRENT_TIMESTAMP
        WHERE student_id = ?;
    """
    db_student = get_student(db, student_id)
    if db_student:
        update_data = student_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student


def verify_student_password(db: Session, email: str, password: str) -> Optional[Student]:
    """
    Verify student credentials for login.
    
    This performs:
    1. SELECT query to find student by email
    2. Password hash verification (bcrypt)
    """
    student = get_student_by_email(db, email)
    if student and pwd_context.verify(password, student.password_hash):
        return student
    return None


# ========================================
# CANTEEN CRUD OPERATIONS
# ========================================

def create_canteen(db: Session, canteen: schemas.CanteenCreate) -> Canteen:
    """
    Create a new canteen.
    
    SQL Equivalent:
        INSERT INTO canteens (name, location, opening_time, closing_time, is_active, created_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP);
    """
    db_canteen = Canteen(**canteen.model_dump())
    db.add(db_canteen)
    db.commit()
    db.refresh(db_canteen)
    return db_canteen


def get_canteens(db: Session, active_only: bool = False) -> List[Canteen]:
    """
    Get all canteens, optionally filter by active status.
    
    SQL Equivalent:
        SELECT * FROM canteens 
        WHERE (is_active = TRUE OR ? = FALSE)
        ORDER BY name;
    """
    query = db.query(Canteen)
    if active_only:
        query = query.filter(Canteen.is_active == True)
    return query.order_by(Canteen.name).all()


def get_canteen(db: Session, canteen_id: int) -> Optional[Canteen]:
    """
    Get canteen by ID.
    
    SQL Equivalent:
        SELECT * FROM canteens WHERE canteen_id = ?;
    """
    return db.query(Canteen).filter(Canteen.canteen_id == canteen_id).first()


def update_canteen(db: Session, canteen_id: int, canteen_update: schemas.CanteenUpdate) -> Optional[Canteen]:
    """
    Update canteen details.
    
    SQL Equivalent:
        UPDATE canteens
        SET name = COALESCE(?, name), ...
        WHERE canteen_id = ?;
    """
    db_canteen = get_canteen(db, canteen_id)
    if db_canteen:
        update_data = canteen_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_canteen, key, value)
        db.commit()
        db.refresh(db_canteen)
    return db_canteen


# ========================================
# MENU ITEM CRUD OPERATIONS
# ========================================

def create_menu_item(db: Session, item: schemas.MenuItemCreate) -> MenuItem:
    """
    Create a new menu item.
    
    SQL Equivalent:
        INSERT INTO menu_items (canteen_id, item_name, description, price, 
                               category, is_vegetarian, is_available, image_url,
                               created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    """
    db_item = MenuItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_menu_items(
    db: Session, 
    canteen_id: Optional[int] = None,
    category: Optional[str] = None,
    available_only: bool = False,
    vegetarian_only: bool = False
) -> List[MenuItem]:
    """
    Get menu items with optional filters.
    
    SQL Equivalent:
        SELECT * FROM menu_items
        WHERE (canteen_id = ? OR ? IS NULL)
          AND (category = ? OR ? IS NULL)
          AND (is_available = TRUE OR ? = FALSE)
          AND (is_vegetarian = TRUE OR ? = FALSE)
        ORDER BY category, item_name;
    """
    query = db.query(MenuItem)
    
    if canteen_id:
        query = query.filter(MenuItem.canteen_id == canteen_id)
    if category:
        query = query.filter(MenuItem.category == category)
    if available_only:
        query = query.filter(MenuItem.is_available == True)
    if vegetarian_only:
        query = query.filter(MenuItem.is_vegetarian == True)
    
    return query.order_by(MenuItem.category, MenuItem.item_name).all()


def get_menu_item(db: Session, item_id: int) -> Optional[MenuItem]:
    """
    Get menu item by ID.
    
    SQL Equivalent:
        SELECT * FROM menu_items WHERE item_id = ?;
    """
    return db.query(MenuItem).filter(MenuItem.item_id == item_id).first()


def update_menu_item(db: Session, item_id: int, item_update: schemas.MenuItemUpdate) -> Optional[MenuItem]:
    """
    Update menu item details.
    
    SQL Equivalent:
        UPDATE menu_items
        SET item_name = COALESCE(?, item_name),
            description = COALESCE(?, description),
            price = COALESCE(?, price),
            ...
            updated_at = CURRENT_TIMESTAMP
        WHERE item_id = ?;
    """
    db_item = get_menu_item(db, item_id)
    if db_item:
        update_data = item_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_menu_item(db: Session, item_id: int) -> bool:
    """
    Delete a menu item.
    
    SQL Equivalent:
        DELETE FROM menu_items WHERE item_id = ?;
    
    Note: This will fail if there are existing order_items referencing this item
    due to FK constraints (referential integrity).
    """
    db_item = get_menu_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False


def toggle_menu_item_availability(db: Session, item_id: int) -> Optional[MenuItem]:
    """
    Toggle menu item availability status.
    
    SQL Equivalent:
        UPDATE menu_items
        SET is_available = NOT is_available,
            updated_at = CURRENT_TIMESTAMP
        WHERE item_id = ?;
    """
    db_item = get_menu_item(db, item_id)
    if db_item:
        db_item.is_available = not db_item.is_available
        db.commit()
        db.refresh(db_item)
    return db_item


# ========================================
# ORDER CRUD OPERATIONS
# ========================================

def create_order(db: Session, order: schemas.OrderCreate) -> Order:
    """
    Create a new order with items.
    
    This is a TRANSACTION that:
    1. Creates the order header
    2. Creates all order items
    3. Calculates and updates total amount
    4. Creates delivery/pickup record if applicable
    
    SQL Equivalent (simplified):
        BEGIN TRANSACTION;
        
        INSERT INTO orders (student_id, canteen_id, order_type, order_status, 
                           special_instructions, total_amount, order_date)
        VALUES (?, ?, ?, 'PLACED', ?, 0, CURRENT_TIMESTAMP);
        
        -- Get the new order_id
        SET @order_id = LAST_INSERT_ID();
        
        -- For each item:
        INSERT INTO order_items (order_id, item_id, quantity, unit_price, subtotal, notes)
        SELECT @order_id, ?, ?, price, price * ?, ?
        FROM menu_items WHERE item_id = ?;
        
        -- Update total
        UPDATE orders 
        SET total_amount = (SELECT SUM(subtotal) FROM order_items WHERE order_id = @order_id)
        WHERE order_id = @order_id;
        
        -- Create delivery record if needed
        INSERT INTO delivery_pickups (order_id, delivery_address, personnel_id, estimated_time)
        VALUES (@order_id, ?, ?, ?);
        
        COMMIT;
    """
    # Create order header
    db_order = Order(
        student_id=order.student_id,
        canteen_id=order.canteen_id,
        order_type=OrderType[order.order_type.value],
        order_status=OrderStatus.PLACED,
        special_instructions=order.special_instructions
    )
    db.add(db_order)
    db.flush()  # Flush to get the order_id
    
    # Create order items
    total_amount = 0.0
    for item in order.items:
        menu_item = get_menu_item(db, item.item_id)
        if not menu_item:
            db.rollback()
            raise ValueError(f"Menu item {item.item_id} not found")
        if not menu_item.is_available:
            db.rollback()
            raise ValueError(f"Menu item '{menu_item.item_name}' is not available")
        
        subtotal = menu_item.price * item.quantity
        total_amount += subtotal
        
        db_order_item = OrderItem(
            order_id=db_order.order_id,
            item_id=item.item_id,
            quantity=item.quantity,
            unit_price=menu_item.price,
            subtotal=subtotal,
            notes=item.notes
        )
        db.add(db_order_item)
    
    # Update total amount
    db_order.total_amount = total_amount
    
    # Create delivery record if delivery info provided
    if order.delivery_info:
        db_delivery = DeliveryPickup(
            order_id=db_order.order_id,
            delivery_address=order.delivery_info.delivery_address,
            personnel_id=order.delivery_info.personnel_id,
            estimated_time=order.delivery_info.estimated_time
        )
        db.add(db_delivery)
    
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int) -> Optional[Order]:
    """
    Get order by ID with all related data.
    
    SQL Equivalent (using JOINs):
        SELECT o.*, s.name as student_name, s.roll_number,
               oi.*, mi.item_name, mi.price,
               p.*, dp.*
        FROM orders o
        JOIN students s ON o.student_id = s.student_id
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        LEFT JOIN menu_items mi ON oi.item_id = mi.item_id
        LEFT JOIN payments p ON o.order_id = p.order_id
        LEFT JOIN delivery_pickups dp ON o.order_id = dp.order_id
        WHERE o.order_id = ?;
    """
    return db.query(Order)\
        .options(
            joinedload(Order.student),
            joinedload(Order.order_items).joinedload(OrderItem.menu_item),
            joinedload(Order.payment),
            joinedload(Order.delivery).joinedload(DeliveryPickup.personnel)
        )\
        .filter(Order.order_id == order_id)\
        .first()


def get_orders_by_student(db: Session, student_id: int, skip: int = 0, limit: int = 50) -> List[Order]:
    """
    Get all orders for a specific student.
    
    SQL Equivalent:
        SELECT o.*, 
               GROUP_CONCAT(mi.item_name) as items,
               p.payment_status
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        LEFT JOIN menu_items mi ON oi.item_id = mi.item_id
        LEFT JOIN payments p ON o.order_id = p.order_id
        WHERE o.student_id = ?
        GROUP BY o.order_id
        ORDER BY o.order_date DESC
        LIMIT ? OFFSET ?;
    """
    return db.query(Order)\
        .options(
            joinedload(Order.order_items).joinedload(OrderItem.menu_item),
            joinedload(Order.payment)
        )\
        .filter(Order.student_id == student_id)\
        .order_by(desc(Order.order_date))\
        .offset(skip).limit(limit)\
        .all()


def get_orders_by_status(db: Session, status: OrderStatus, canteen_id: Optional[int] = None) -> List[Order]:
    """
    Get orders by status, optionally filtered by canteen.
    
    SQL Equivalent:
        SELECT o.*, s.name, s.roll_number
        FROM orders o
        JOIN students s ON o.student_id = s.student_id
        WHERE o.order_status = ?
          AND (o.canteen_id = ? OR ? IS NULL)
        ORDER BY o.order_date ASC;
    """
    query = db.query(Order)\
        .options(joinedload(Order.student))\
        .filter(Order.order_status == status)
    
    if canteen_id:
        query = query.filter(Order.canteen_id == canteen_id)
    
    return query.order_by(Order.order_date).all()


# Valid status transitions (state machine)
VALID_STATUS_TRANSITIONS = {
    OrderStatus.PLACED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
    OrderStatus.PREPARING: [OrderStatus.READY, OrderStatus.CANCELLED],
    OrderStatus.READY: [OrderStatus.DELIVERED, OrderStatus.CANCELLED],
    OrderStatus.DELIVERED: [],  # Final state
    OrderStatus.CANCELLED: []   # Final state
}


def update_order_status(db: Session, order_id: int, new_status: OrderStatus) -> Optional[Order]:
    """
    Update order status with validation.
    
    Implements state machine logic to prevent invalid transitions.
    
    SQL Equivalent (with validation):
        -- Check current status
        SELECT order_status FROM orders WHERE order_id = ?;
        
        -- If valid transition:
        UPDATE orders
        SET order_status = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE order_id = ?;
    """
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    
    current_status = db_order.order_status
    
    # Validate status transition
    if new_status not in VALID_STATUS_TRANSITIONS.get(current_status, []):
        raise ValueError(
            f"Invalid status transition: {current_status.value} → {new_status.value}. "
            f"Valid transitions: {[s.value for s in VALID_STATUS_TRANSITIONS[current_status]]}"
        )
    
    db_order.order_status = new_status
    db.commit()
    db.refresh(db_order)
    return db_order


# ========================================
# DELIVERY PERSONNEL CRUD OPERATIONS
# ========================================

def create_delivery_personnel(db: Session, personnel: schemas.DeliveryPersonnelCreate) -> DeliveryPersonnel:
    """
    Create a new delivery personnel with hashed password.
    """
    hashed_password = pwd_context.hash(personnel.password)
    db_personnel = DeliveryPersonnel(
        name=personnel.name,
        roll_number=personnel.roll_number,
        email=personnel.email,
        phone=personnel.phone,
        password_hash=hashed_password,
        is_available=personnel.is_available
    )
    db.add(db_personnel)
    db.commit()
    db.refresh(db_personnel)
    return db_personnel

def get_delivery_personnel_by_email(db: Session, email: str) -> Optional[DeliveryPersonnel]:
    return db.query(DeliveryPersonnel).filter(DeliveryPersonnel.email == email).first()

def verify_delivery_password(db: Session, email: str, password: str) -> Optional[DeliveryPersonnel]:
    personnel = get_delivery_personnel_by_email(db, email)
    if personnel and pwd_context.verify(password, personnel.password_hash):
        return personnel
    return None


def get_available_delivery_personnel(db: Session) -> List[DeliveryPersonnel]:
    """
    Get all available delivery personnel.
    
    SQL Equivalent:
        SELECT * FROM delivery_personnel
        WHERE is_available = TRUE
        ORDER BY name;
    """
    return db.query(DeliveryPersonnel)\
        .filter(DeliveryPersonnel.is_available == True)\
        .order_by(DeliveryPersonnel.name)\
        .all()


def update_delivery_status(db: Session, order_id: int, is_delivered: bool) -> Optional[DeliveryPickup]:
    """
    Update delivery confirmation status.
    
    SQL Equivalent:
        UPDATE delivery_pickups
        SET is_delivered = ?,
            actual_delivery_time = CASE WHEN ? = TRUE THEN CURRENT_TIMESTAMP ELSE NULL END
        WHERE order_id = ?;
    """
    db_delivery = db.query(DeliveryPickup).filter(DeliveryPickup.order_id == order_id).first()
    if db_delivery:
        db_delivery.is_delivered = is_delivered
        if is_delivered:
            db_delivery.actual_delivery_time = datetime.utcnow()
        db.commit()
        db.refresh(db_delivery)
    return db_delivery


# ========================================
# PAYMENT CRUD OPERATIONS
# ========================================

def create_payment(db: Session, payment: schemas.PaymentCreate) -> Payment:
    """
    Create a new payment record.
    
    SQL Equivalent:
        INSERT INTO payments (order_id, amount_paid, payment_method, 
                             payment_status, transaction_id, payment_screenshot, created_at)
        VALUES (?, ?, ?, 'PENDING', ?, ?, CURRENT_TIMESTAMP);
    """
    db_payment = Payment(
        order_id=payment.order_id,
        amount_paid=payment.amount_paid,
        payment_method=PaymentMethod[payment.payment_method.value],
        payment_status=PaymentStatus.PENDING,
        transaction_id=payment.transaction_id,
        payment_screenshot=payment.payment_screenshot
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def update_payment_status(db: Session, payment_id: int, payment_update: schemas.PaymentUpdate) -> Optional[Payment]:
    """
    Update payment status and screenshot.
    
    SQL Equivalent:
        UPDATE payments
        SET payment_status = COALESCE(?, payment_status),
            transaction_id = COALESCE(?, transaction_id),
            payment_screenshot = COALESCE(?, payment_screenshot),
            payment_date = CASE WHEN ? = 'COMPLETED' THEN CURRENT_TIMESTAMP ELSE payment_date END
        WHERE payment_id = ?;
    """
    db_payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if db_payment:
        if payment_update.payment_status:
            db_payment.payment_status = PaymentStatus[payment_update.payment_status.value]
            if payment_update.payment_status == schemas.PaymentStatusEnum.COMPLETED:
                db_payment.payment_date = datetime.utcnow()
        if payment_update.transaction_id:
            db_payment.transaction_id = payment_update.transaction_id
        if payment_update.payment_screenshot:
            db_payment.payment_screenshot = payment_update.payment_screenshot
        db.commit()
        db.refresh(db_payment)
    return db_payment


def get_payment_by_order(db: Session, order_id: int) -> Optional[Payment]:
    """
    Get payment for an order.
    
    SQL Equivalent:
        SELECT * FROM payments WHERE order_id = ?;
    """
    return db.query(Payment).filter(Payment.order_id == order_id).first()


# ========================================
# REPORT QUERIES
# ========================================

def get_daily_revenue(db: Session, report_date: date) -> schemas.DailyRevenueReport:
    """
    Get daily revenue report.
    
    SQL Equivalent:
        SELECT 
            DATE(p.payment_date) as date,
            COUNT(DISTINCT o.order_id) as total_orders,
            COUNT(DISTINCT CASE WHEN p.payment_status = 'COMPLETED' THEN o.order_id END) as completed_orders,
            COALESCE(SUM(CASE WHEN p.payment_status = 'COMPLETED' THEN p.amount_paid END), 0) as total_revenue,
            COALESCE(SUM(CASE WHEN p.payment_status = 'COMPLETED' AND p.payment_method = 'CASH' 
                         THEN p.amount_paid END), 0) as cash_revenue,
            COALESCE(SUM(CASE WHEN p.payment_status = 'COMPLETED' AND p.payment_method = 'UPI' 
                         THEN p.amount_paid END), 0) as upi_revenue
        FROM orders o
        LEFT JOIN payments p ON o.order_id = p.order_id
        WHERE DATE(o.order_date) = ?
        GROUP BY DATE(p.payment_date);
    """
    # Get orders for the date
    orders_query = db.query(Order).filter(
        func.date(Order.order_date) == report_date
    )
    total_orders = orders_query.count()
    
    # Get completed payments for the date
    payments_query = db.query(Payment).join(Order).filter(
        func.date(Order.order_date) == report_date,
        Payment.payment_status == PaymentStatus.COMPLETED
    )
    
    completed_orders = payments_query.count()
    
    total_revenue = db.query(func.coalesce(func.sum(Payment.amount_paid), 0)).join(Order).filter(
        func.date(Order.order_date) == report_date,
        Payment.payment_status == PaymentStatus.COMPLETED
    ).scalar()
    
    cash_revenue = db.query(func.coalesce(func.sum(Payment.amount_paid), 0)).join(Order).filter(
        func.date(Order.order_date) == report_date,
        Payment.payment_status == PaymentStatus.COMPLETED,
        Payment.payment_method == PaymentMethod.CASH
    ).scalar()
    
    upi_revenue = db.query(func.coalesce(func.sum(Payment.amount_paid), 0)).join(Order).filter(
        func.date(Order.order_date) == report_date,
        Payment.payment_status == PaymentStatus.COMPLETED,
        Payment.payment_method == PaymentMethod.UPI
    ).scalar()
    
    return schemas.DailyRevenueReport(
        date=str(report_date),
        total_orders=total_orders,
        completed_orders=completed_orders,
        total_revenue=float(total_revenue),
        cash_revenue=float(cash_revenue),
        upi_revenue=float(upi_revenue)
    )


def get_student_order_history(db: Session, student_id: int) -> Optional[schemas.StudentOrderHistory]:
    """
    Get complete order history for a student.
    
    SQL Equivalent:
        SELECT 
            s.student_id, s.name, s.roll_number,
            COUNT(o.order_id) as total_orders,
            COALESCE(SUM(o.total_amount), 0) as total_spent
        FROM students s
        LEFT JOIN orders o ON s.student_id = o.student_id
        WHERE s.student_id = ?
        GROUP BY s.student_id;
        
        -- Then get all orders:
        SELECT o.order_id, o.order_date, o.order_status, o.order_type, o.total_amount
        FROM orders o
        WHERE o.student_id = ?
        ORDER BY o.order_date DESC;
    """
    student = get_student(db, student_id)
    if not student:
        return None
    
    # Get total stats
    stats = db.query(
        func.count(Order.order_id).label('total_orders'),
        func.coalesce(func.sum(Order.total_amount), 0).label('total_spent')
    ).filter(Order.student_id == student_id).first()
    
    # Get orders
    orders = get_orders_by_student(db, student_id)
    
    return schemas.StudentOrderHistory(
        student=schemas.StudentBrief(
            student_id=student.student_id,
            name=student.name,
            roll_number=student.roll_number
        ),
        total_orders=stats.total_orders,
        total_spent=float(stats.total_spent),
        orders=[schemas.OrderBrief(
            order_id=o.order_id,
            order_date=o.order_date,
            order_status=schemas.OrderStatusEnum(o.order_status.value),
            order_type=schemas.OrderTypeEnum(o.order_type.value),
            total_amount=o.total_amount,
            payment=schemas.PaymentResponse(
                payment_id=o.payment.payment_id,
                order_id=o.payment.order_id,
                amount_paid=o.payment.amount_paid,
                payment_method=schemas.PaymentMethodEnum(o.payment.payment_method.value),
                payment_status=schemas.PaymentStatusEnum(o.payment.payment_status.value),
                transaction_id=o.payment.transaction_id,
                payment_screenshot=o.payment.payment_screenshot,
                payment_date=o.payment.payment_date,
                created_at=o.payment.created_at
            ) if o.payment else None
        ) for o in orders]
    )


def get_popular_items(db: Session, limit: int = 10) -> List[dict]:
    """
    Get most popular menu items by order count.
    
    SQL Equivalent:
        SELECT 
            mi.item_id, mi.item_name, mi.price,
            COUNT(oi.order_item_id) as order_count,
            SUM(oi.quantity) as total_quantity
        FROM menu_items mi
        LEFT JOIN order_items oi ON mi.item_id = oi.item_id
        GROUP BY mi.item_id
        ORDER BY order_count DESC
        LIMIT ?;
    """
    results = db.query(
        MenuItem.item_id,
        MenuItem.item_name,
        MenuItem.price,
        func.count(OrderItem.order_item_id).label('order_count'),
        func.coalesce(func.sum(OrderItem.quantity), 0).label('total_quantity')
    ).outerjoin(OrderItem).group_by(MenuItem.item_id)\
     .order_by(desc('order_count'))\
     .limit(limit).all()
    
    return [
        {
            'item_id': r.item_id,
            'item_name': r.item_name,
            'price': r.price,
            'order_count': r.order_count,
            'total_quantity': r.total_quantity
        }
        for r in results
    ]
