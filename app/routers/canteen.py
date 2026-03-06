"""
========================================
College Canteen Food Ordering System
DBMS Mini Project - API Routers (Canteen & Master Data)
========================================

This module contains API endpoints for:
1. Canteen management
2. Hostel master data
3. Department master data
4. Delivery personnel management

These are typically admin-only endpoints for managing reference data.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud, schemas

router = APIRouter(tags=["Canteen & Master Data"])


# ========================================
# CANTEEN ENDPOINTS
# ========================================

@router.post("/canteens", response_model=schemas.CanteenResponse, status_code=status.HTTP_201_CREATED)
def create_canteen(canteen: schemas.CanteenCreate, db: Session = Depends(get_db)):
    """
    Create a new canteen.
    
    SQL Equivalent:
        INSERT INTO canteens (name, location, opening_time, closing_time, is_active, created_at)
        VALUES (?, ?, ?, ?, TRUE, CURRENT_TIMESTAMP);
    """
    return crud.create_canteen(db, canteen)


@router.get("/canteens", response_model=List[schemas.CanteenResponse])
def get_canteens(active_only: bool = False, db: Session = Depends(get_db)):
    """
    Get all canteens.
    
    SQL Equivalent:
        SELECT * FROM canteens 
        WHERE is_active = TRUE OR ? = FALSE
        ORDER BY name;
    """
    return crud.get_canteens(db, active_only=active_only)


@router.get("/canteens/{canteen_id}", response_model=schemas.CanteenResponse)
def get_canteen(canteen_id: int, db: Session = Depends(get_db)):
    """
    Get a specific canteen by ID.
    """
    canteen = crud.get_canteen(db, canteen_id)
    if not canteen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Canteen with ID {canteen_id} not found"
        )
    return canteen


@router.put("/canteens/{canteen_id}", response_model=schemas.CanteenResponse)
def update_canteen(canteen_id: int, canteen_update: schemas.CanteenUpdate, db: Session = Depends(get_db)):
    """
    Update canteen information.
    """
    canteen = crud.update_canteen(db, canteen_id, canteen_update)
    if not canteen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Canteen with ID {canteen_id} not found"
        )
    return canteen


# ========================================
# HOSTEL ENDPOINTS
# ========================================

@router.post("/hostels", response_model=schemas.HostelResponse, status_code=status.HTTP_201_CREATED)
def create_hostel(hostel: schemas.HostelCreate, db: Session = Depends(get_db)):
    """
    Create a new hostel (master data).
    
    SQL Equivalent:
        INSERT INTO hostels (hostel_name, hostel_type, address, created_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP);
    """
    return crud.create_hostel(db, hostel)


@router.get("/hostels", response_model=List[schemas.HostelResponse])
def get_hostels(db: Session = Depends(get_db)):
    """
    Get all hostels.
    
    SQL Equivalent:
        SELECT * FROM hostels ORDER BY hostel_name;
    """
    return crud.get_hostels(db)


# ========================================
# DEPARTMENT ENDPOINTS
# ========================================

@router.post("/departments", response_model=schemas.DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    """
    Create a new department (master data).
    
    SQL Equivalent:
        INSERT INTO departments (department_name, department_code, created_at)
        VALUES (?, ?, CURRENT_TIMESTAMP);
    """
    return crud.create_department(db, department)


@router.get("/departments", response_model=List[schemas.DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    """
    Get all departments.
    
    SQL Equivalent:
        SELECT * FROM departments ORDER BY department_code;
    """
    return crud.get_departments(db)


# ========================================
# DELIVERY PERSONNEL ENDPOINTS
# ========================================

@router.post("/delivery-personnel", response_model=schemas.DeliveryPersonnelResponse, status_code=status.HTTP_201_CREATED)
def create_delivery_personnel(personnel: schemas.DeliveryPersonnelCreate, db: Session = Depends(get_db)):
    """
    Add a new delivery person.
    
    SQL Equivalent:
        INSERT INTO delivery_personnel (name, phone, is_available, created_at)
        VALUES (?, ?, TRUE, CURRENT_TIMESTAMP);
    """
    return crud.create_delivery_personnel(db, personnel)


@router.get("/delivery-personnel/available", response_model=List[schemas.DeliveryPersonnelResponse])
def get_available_personnel(db: Session = Depends(get_db)):
    """
    Get all available delivery personnel.
    
    SQL Equivalent:
        SELECT * FROM delivery_personnel
        WHERE is_available = TRUE
        ORDER BY name;
    """
    return crud.get_available_delivery_personnel(db)
