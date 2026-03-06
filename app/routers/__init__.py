"""
Routers package initialization
"""

from app.routers.students import router as students_router
from app.routers.menu import router as menu_router
from app.routers.orders import router as orders_router
from app.routers.payments import router as payments_router
from app.routers.canteen import router as canteen_router

__all__ = [
    "students_router",
    "menu_router", 
    "orders_router",
    "payments_router",
    "canteen_router"
]
