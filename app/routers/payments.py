"""
========================================
College Canteen Food Ordering System
DBMS Mini Project - API Routers (Payments & Reports)
========================================

This module contains API endpoints for:
1. Payment management
2. Delivery management
3. Report generation

Endpoints:
- POST /payments - Record a payment
- PUT /payments/{id} - Update payment status
- GET /payments/order/{order_id} - Get payment for order
- PUT /delivery/{order_id}/confirm - Confirm delivery
- GET /reports/revenue - Daily revenue report
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.database import get_db
from app import crud, schemas

router = APIRouter(tags=["Payments & Reports"])


# ========================================
# PAYMENT ENDPOINTS
# ========================================

@router.post("/payments", response_model=schemas.PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    """
    Record a new payment for an order.
    
    Payment Methods:
    - CASH: Cash payment at counter
    - UPI: Digital payment (provide transaction_id)
    
    Initial status is PENDING until confirmed.
    
    SQL Equivalent:
        -- Check if order exists and doesn't have payment
        SELECT * FROM orders o
        LEFT JOIN payments p ON o.order_id = p.order_id
        WHERE o.order_id = ? AND p.payment_id IS NULL;
        
        -- Create payment
        INSERT INTO payments (order_id, amount_paid, payment_method, payment_status, transaction_id)
        VALUES (?, ?, ?, 'PENDING', ?);
    """
    # Validate order exists
    order = crud.get_order(db, payment.order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {payment.order_id} not found"
        )
    
    # Check if payment already exists
    existing_payment = crud.get_payment_by_order(db, payment.order_id)
    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment already exists for order {payment.order_id}"
        )
    
    # Validate amount matches order total
    if abs(payment.amount_paid - order.total_amount) > 0.01:  # Allow small float difference
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment amount ({payment.amount_paid}) doesn't match order total ({order.total_amount})"
        )
    
    return crud.create_payment(db, payment)


@router.put("/payments/{payment_id}", response_model=schemas.PaymentResponse)
def update_payment_status(payment_id: int, payment_update: schemas.PaymentUpdate, db: Session = Depends(get_db)):
    """
    Update payment status.
    
    Status Flow:
    - PENDING → COMPLETED (payment successful)
    - PENDING → FAILED (payment failed)
    - COMPLETED → REFUNDED (refund issued)
    
    SQL Equivalent:
        UPDATE payments
        SET payment_status = ?,
            transaction_id = COALESCE(?, transaction_id),
            payment_date = CASE WHEN ? = 'COMPLETED' THEN CURRENT_TIMESTAMP ELSE payment_date END
        WHERE payment_id = ?;
    """
    payment = crud.update_payment_status(db, payment_id, payment_update)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payment with ID {payment_id} not found"
        )
    return payment


@router.get("/payments/order/{order_id}", response_model=schemas.PaymentResponse)
def get_payment_by_order(order_id: int, db: Session = Depends(get_db)):
    """
    Get payment information for a specific order.
    
    SQL Equivalent:
        SELECT * FROM payments WHERE order_id = ?;
    """
    payment = crud.get_payment_by_order(db, order_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No payment found for order {order_id}"
        )
    return payment


# ========================================
# DELIVERY ENDPOINTS
# ========================================

@router.put("/delivery/{order_id}/confirm", response_model=schemas.DeliveryPickupResponse)
def confirm_delivery(order_id: int, db: Session = Depends(get_db)):
    """
    Confirm that an order has been delivered/picked up.
    
    This:
    1. Sets is_delivered = True
    2. Records actual_delivery_time
    
    SQL Equivalent:
        UPDATE delivery_pickups
        SET is_delivered = TRUE,
            actual_delivery_time = CURRENT_TIMESTAMP
        WHERE order_id = ?;
    """
    delivery = crud.update_delivery_status(db, order_id, is_delivered=True)
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Delivery record for order {order_id} not found"
        )
    return delivery


# ========================================
# REPORT ENDPOINTS
# ========================================

@router.get("/reports/revenue", response_model=schemas.DailyRevenueReport)
def get_daily_revenue_report(
    report_date: Optional[date] = Query(None, description="Date for report (default: today)"),
    db: Session = Depends(get_db)
):
    """
    Generate daily revenue report.
    
    Returns:
    - Total number of orders placed
    - Number of completed (paid) orders
    - Total revenue collected
    - Revenue breakdown by payment method (Cash/UPI)
    
    SQL Equivalent:
        SELECT 
            DATE(o.order_date) as date,
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
        GROUP BY DATE(o.order_date);
    """
    if report_date is None:
        report_date = date.today()
    
    return crud.get_daily_revenue(db, report_date)
