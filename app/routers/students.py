"""
========================================
College Canteen Food Ordering System
DBMS Mini Project - API Routers (Students)
========================================

This module contains API endpoints for student management.

Endpoints:
- POST /students/register - Register new student
- POST /students/login - Student login
- GET /students - Get all students
- GET /students/{id} - Get student by ID
- PUT /students/{id} - Update student
- GET /students/{id}/orders - Get student order history
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/register", response_model=schemas.StudentResponse, status_code=status.HTTP_201_CREATED)
def register_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """
    Register a new student.
    
    This endpoint:
    1. Validates input data (Pydantic)
    2. Checks for duplicate email/roll number
    3. Hashes the password
    4. Creates the student record
    
    Corresponding SQL Operations:
    - SELECT to check duplicates
    - INSERT to create record
    """
    # Check if email already exists
    if crud.get_student_by_email(db, student.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{student.email}' is already registered"
        )
    
    # Check if roll number already exists
    if crud.get_student_by_roll_number(db, student.roll_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Roll number '{student.roll_number}' is already registered"
        )
    
    # Validate hostel exists if provided
    if student.hostel_id and not crud.get_hostel(db, student.hostel_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Hostel with ID {student.hostel_id} not found"
        )
    
    # Validate department exists if provided
    if student.department_id and not crud.get_department(db, student.department_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department with ID {student.department_id} not found"
        )
    
    return crud.create_student(db, student)


@router.post("/login", response_model=schemas.StudentResponse)
def login_student(credentials: schemas.StudentLogin, db: Session = Depends(get_db)):
    """
    Authenticate a student.
    
    This endpoint:
    1. Looks up the student by email
    2. Verifies the password hash
    3. Returns student info on success
    
    Note: In production, this would return a JWT token instead.
    """
    student = crud.verify_student_password(db, credentials.email, credentials.password)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    return student


@router.get("/", response_model=List[schemas.StudentResponse])
def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all students with pagination.
    
    Query Parameters:
    - skip: Number of records to skip (for pagination)
    - limit: Maximum records to return
    
    SQL Equivalent:
        SELECT s.*, h.*, d.* FROM students s
        LEFT JOIN hostels h ON s.hostel_id = h.hostel_id
        LEFT JOIN departments d ON s.department_id = d.department_id
        ORDER BY s.name LIMIT ? OFFSET ?;
    """
    return crud.get_students(db, skip=skip, limit=limit)


@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """
    Get a specific student by ID.
    
    Returns student with related hostel and department information.
    """
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
    return student


@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, student_update: schemas.StudentUpdate, db: Session = Depends(get_db)):
    """
    Update student information.
    
    Only provided fields are updated (partial update).
    """
    student = crud.update_student(db, student_id, student_update)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
    return student


@router.get("/{student_id}/orders", response_model=schemas.StudentOrderHistory)
def get_student_orders(student_id: int, db: Session = Depends(get_db)):
    """
    Get complete order history for a student.
    
    Returns:
    - Student basic info
    - Total orders count
    - Total amount spent
    - List of all orders
    
    SQL Equivalent:
        SELECT COUNT(*) as total_orders, SUM(total_amount) as total_spent
        FROM orders WHERE student_id = ?;
        
        SELECT * FROM orders WHERE student_id = ? ORDER BY order_date DESC;
    """
    history = crud.get_student_order_history(db, student_id)
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found"
        )
    return history
