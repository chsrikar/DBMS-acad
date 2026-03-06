"""
========================================
College Canteen Food Ordering System
DBMS Mini Project - API Routers (Menu)
========================================

This module contains API endpoints for menu management.

Endpoints:
- POST /menu - Create menu item
- GET /menu - Get all menu items with filters
- GET /menu/{id} - Get menu item by ID
- PUT /menu/{id} - Update menu item
- DELETE /menu/{id} - Delete menu item
- PUT /menu/{id}/toggle - Toggle availability
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/menu", tags=["Menu"])


@router.post("/", response_model=schemas.MenuItemResponse, status_code=status.HTTP_201_CREATED)
def create_menu_item(item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    """
    Create a new menu item.
    
    Validates:
    - Canteen exists
    - Price is positive (Pydantic validation)
    
    SQL Equivalent:
        INSERT INTO menu_items (canteen_id, item_name, description, price, ...)
        VALUES (?, ?, ?, ?, ...);
    """
    # Validate canteen exists
    if not crud.get_canteen(db, item.canteen_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Canteen with ID {item.canteen_id} not found"
        )
    
    return crud.create_menu_item(db, item)


@router.get("/", response_model=List[schemas.MenuItemResponse])
def get_menu_items(
    canteen_id: Optional[int] = Query(None, description="Filter by canteen"),
    category: Optional[str] = Query(None, description="Filter by category"),
    available_only: bool = Query(False, description="Show only available items"),
    vegetarian_only: bool = Query(False, description="Show only vegetarian items"),
    db: Session = Depends(get_db)
):
    """
    Get menu items with optional filters.
    
    Query Parameters:
    - canteen_id: Filter by specific canteen
    - category: Filter by food category
    - available_only: Only show items currently available
    - vegetarian_only: Only show vegetarian items
    
    SQL Equivalent:
        SELECT * FROM menu_items
        WHERE (canteen_id = ? OR ? IS NULL)
          AND (category = ? OR ? IS NULL)
          AND (is_available = TRUE OR ? = FALSE)
          AND (is_vegetarian = TRUE OR ? = FALSE)
        ORDER BY category, item_name;
    """
    return crud.get_menu_items(
        db,
        canteen_id=canteen_id,
        category=category,
        available_only=available_only,
        vegetarian_only=vegetarian_only
    )


@router.get("/{item_id}", response_model=schemas.MenuItemResponse)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get a specific menu item by ID.
    """
    item = crud.get_menu_item(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu item with ID {item_id} not found"
        )
    return item


@router.put("/{item_id}", response_model=schemas.MenuItemResponse)
def update_menu_item(item_id: int, item_update: schemas.MenuItemUpdate, db: Session = Depends(get_db)):
    """
    Update a menu item (partial update).
    
    Only provided fields are updated.
    
    SQL Equivalent:
        UPDATE menu_items
        SET item_name = COALESCE(?, item_name),
            price = COALESCE(?, price),
            ...
            updated_at = CURRENT_TIMESTAMP
        WHERE item_id = ?;
    """
    item = crud.update_menu_item(db, item_id, item_update)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu item with ID {item_id} not found"
        )
    return item


@router.delete("/{item_id}", response_model=schemas.Message)
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete a menu item.
    
    Note: This will fail if there are existing orders referencing this item
    (referential integrity constraint).
    
    SQL Equivalent:
        DELETE FROM menu_items WHERE item_id = ?;
    """
    if not crud.delete_menu_item(db, item_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu item with ID {item_id} not found"
        )
    return schemas.Message(message=f"Menu item {item_id} deleted successfully")


@router.put("/{item_id}/toggle", response_model=schemas.MenuItemResponse)
def toggle_availability(item_id: int, db: Session = Depends(get_db)):
    """
    Toggle menu item availability.
    
    Convenient endpoint to enable/disable items.
    
    SQL Equivalent:
        UPDATE menu_items
        SET is_available = NOT is_available,
            updated_at = CURRENT_TIMESTAMP
        WHERE item_id = ?;
    """
    item = crud.toggle_menu_item_availability(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu item with ID {item_id} not found"
        )
    return item


@router.get("/popular/items", response_model=List[dict])
def get_popular_items(limit: int = Query(10, le=50), db: Session = Depends(get_db)):
    """
    Get most popular menu items by order count.
    
    SQL Equivalent:
        SELECT mi.item_id, mi.item_name, mi.price,
               COUNT(oi.order_item_id) as order_count,
               SUM(oi.quantity) as total_quantity
        FROM menu_items mi
        LEFT JOIN order_items oi ON mi.item_id = oi.item_id
        GROUP BY mi.item_id
        ORDER BY order_count DESC
        LIMIT ?;
    """
    return crud.get_popular_items(db, limit=limit)
