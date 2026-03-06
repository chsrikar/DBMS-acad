"""
========================================
College Canteen Food Ordering System
DBMS Mini Project - API Routers (Orders)
========================================

This module contains API endpoints for order management.

Endpoints:
- POST /orders - Place new order
- GET /orders/{id} - Get order details
- PUT /orders/{id}/status - Update order status
- GET /orders/status/{status} - Get orders by status
- GET /orders/student/{id} - Get orders by student
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import crud, schemas
from app.models import OrderStatus

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Place a new food order.
    
    This is a TRANSACTION that:
    1. Validates student exists
    2. Validates canteen exists
    3. Validates all menu items exist and are available
    4. Creates the order header
    5. Creates all order items with prices at time of order
    6. Calculates the total amount automatically
    7. Creates delivery record if applicable
    
    Order Status Flow:
        PLACED → PREPARING → READY → DELIVERED
                     ↘ CANCELLED ↙
    
    SQL Equivalent (Transaction):
        BEGIN TRANSACTION;
        
        INSERT INTO orders (...) VALUES (...);
        SET @order_id = LAST_INSERT_ID();
        
        INSERT INTO order_items (...) VALUES (...);
        -- For each item
        
        UPDATE orders SET total_amount = (
            SELECT SUM(subtotal) FROM order_items WHERE order_id = @order_id
        ) WHERE order_id = @order_id;
        
        COMMIT;
    """
    # Validate student exists
    if not crud.get_student(db, order.student_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student with ID {order.student_id} not found"
        )
    
    # Validate canteen exists
    if not crud.get_canteen(db, order.canteen_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Canteen with ID {order.canteen_id} not found"
        )
    
    try:
        return crud.create_order(db, order)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific order.
    
    Returns:
    - Order header info
    - All order items with menu item details
    - Payment information
    - Delivery/pickup information
    
    SQL Equivalent (with JOINs):
        SELECT o.*, s.*, oi.*, mi.*, p.*, dp.*
        FROM orders o
        JOIN students s ON o.student_id = s.student_id
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        LEFT JOIN menu_items mi ON oi.item_id = mi.item_id
        LEFT JOIN payments p ON o.order_id = p.order_id
        LEFT JOIN delivery_pickups dp ON o.order_id = dp.order_id
        WHERE o.order_id = ?;
    """
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    return order


@router.put("/{order_id}/status", response_model=schemas.OrderResponse)
def update_order_status(order_id: int, status_update: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    """
    Update order status with validation.
    
    Valid status transitions (state machine):
    - PLACED → PREPARING or CANCELLED
    - PREPARING → READY or CANCELLED
    - READY → DELIVERED or CANCELLED
    - DELIVERED → (no transitions, final state)
    - CANCELLED → (no transitions, final state)
    
    Invalid transitions will return an error.
    
    SQL Equivalent:
        -- First check current status
        SELECT order_status FROM orders WHERE order_id = ?;
        
        -- If valid transition:
        UPDATE orders
        SET order_status = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE order_id = ?;
    """
    try:
        new_status = OrderStatus[status_update.order_status.value]
        order = crud.update_order_status(db, order_id, new_status)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with ID {order_id} not found"
            )
        return order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/status/{order_status}", response_model=List[schemas.OrderResponse])
def get_orders_by_status(
    order_status: schemas.OrderStatusEnum,
    canteen_id: Optional[int] = Query(None, description="Filter by canteen"),
    db: Session = Depends(get_db)
):
    """
    Get all orders with a specific status.
    
    Useful for kitchen staff to see:
    - PLACED orders (new orders to prepare)
    - PREPARING orders (currently being made)
    - READY orders (waiting for pickup/delivery)
    
    SQL Equivalent:
        SELECT o.*, s.name, s.roll_number
        FROM orders o
        JOIN students s ON o.student_id = s.student_id
        WHERE o.order_status = ?
          AND (o.canteen_id = ? OR ? IS NULL)
        ORDER BY o.order_date ASC;
    """
    status = OrderStatus[order_status.value]
    return crud.get_orders_by_status(db, status, canteen_id)


@router.get("/student/{student_id}", response_model=List[schemas.OrderBrief])
def get_student_orders(
    student_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all orders for a specific student with pagination.
    
    Returns brief order info sorted by date (newest first).
    
    SQL Equivalent:
        SELECT order_id, order_date, order_status, order_type, total_amount
        FROM orders
        WHERE student_id = ?
        ORDER BY order_date DESC
        LIMIT ? OFFSET ?;
    """
    # Validate student exists
    if not crud.get_student(db, student_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
    
    orders = crud.get_orders_by_student(db, student_id, skip=skip, limit=limit)
    return [
        schemas.OrderBrief(
            order_id=o.order_id,
            order_date=o.order_date,
            order_status=schemas.OrderStatusEnum(o.order_status.value),
            order_type=schemas.OrderTypeEnum(o.order_type.value),
            total_amount=o.total_amount
        )
        for o in orders
    ]
