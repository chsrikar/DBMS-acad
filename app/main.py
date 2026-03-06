"""
========================================
College Canteen Food Ordering System
DBMS Mini Project - FastAPI Main Application
========================================

This is the entry point of the application.
It configures the FastAPI app and includes all routers.

To run the application:
    uvicorn app.main:app --reload

Then visit:
    http://localhost:8000/docs - Swagger UI (API documentation)
    http://localhost:8000/redoc - ReDoc (Alternative API documentation)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers import (
    students_router,
    menu_router,
    orders_router,
    payments_router,
    canteen_router
)

# ========================================
# APPLICATION CONFIGURATION
# ========================================

app = FastAPI(
    title="🍽️ College Canteen Food Ordering System",
    description="""
## DBMS Mini Project

A comprehensive food ordering system demonstrating relational database concepts:

### 📚 DBMS Concepts Covered
- **Primary Keys & Foreign Keys**: Unique identifiers and relationships
- **Normalization (3NF)**: Proper table design to minimize redundancy
- **One-to-Many Relationships**: Student → Orders, Canteen → MenuItems
- **One-to-One Relationships**: Order → Payment, Order → Delivery
- **Constraints**: NOT NULL, UNIQUE, CHECK
- **Transactions**: Order creation as atomic operation
- **Aggregate Functions**: SUM, COUNT for reports

### 🔗 API Modules
- **Students**: Registration, login, profile management
- **Menu**: Food items CRUD with availability toggle
- **Orders**: Order placement with automatic total calculation
- **Payments**: Payment recording and status tracking
- **Reports**: Daily revenue generation

### 🛠️ Technology Stack
- **Backend**: Python FastAPI
- **ORM**: SQLAlchemy 2.0
- **Database**: SQLite (dev) / MySQL / PostgreSQL
- **Validation**: Pydantic

---
*Developed for academic demonstration of DBMS concepts*
    """,
    version="1.0.0",
    contact={
        "name": "DBMS Mini Project",
    },
    license_info={
        "name": "Academic Use",
    }
)

# ========================================
# CORS MIDDLEWARE
# ========================================
# Allow cross-origin requests (needed for frontend integration)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================
# INCLUDE ROUTERS
# ========================================
# Each router handles a specific module of the application

app.include_router(students_router, prefix="/api")
app.include_router(menu_router, prefix="/api")
app.include_router(orders_router, prefix="/api")
app.include_router(payments_router, prefix="/api")
app.include_router(canteen_router, prefix="/api")


# ========================================
# ROOT ENDPOINT
# ========================================

@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint - API health check and information.
    """
    return {
        "message": "🍽️ College Canteen Food Ordering System API",
        "version": "1.0.0",
        "status": "running",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        },
        "api_endpoints": {
            "students": "/api/students",
            "menu": "/api/menu",
            "orders": "/api/orders",
            "payments": "/api/payments",
            "canteens": "/api/canteens",
            "reports": "/api/reports"
        }
    }


@app.get("/health", tags=["Root"])
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}


# ========================================
# STARTUP EVENT
# ========================================

@app.on_event("startup")
async def startup():
    """
    Initialize database on application startup.
    Creates all tables if they don't exist.
    """
    print("🚀 Starting College Canteen Food Ordering System...")
    init_db()
    print("✅ Application ready!")


# ========================================
# MAIN ENTRY POINT
# ========================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
