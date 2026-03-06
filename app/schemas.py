"""
========================================
College Canteen Food Ordering System
DBMS Mini Project - Pydantic Schemas
========================================

Pydantic schemas define the structure of data for:
1. API Request validation (what data the API accepts)
2. API Response serialization (what data the API returns)
3. Data transformation between API and ORM layers

These schemas are separate from ORM models because:
- ORM models define database structure
- Pydantic schemas define API data structure
- This separation follows clean architecture principles
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ========================================
# ENUM SCHEMAS (for API validation)
# ========================================

class OrderStatusEnum(str, Enum):
    PLACED = "PLACED"
    PREPARING = "PREPARING"
    READY = "READY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class OrderTypeEnum(str, Enum):
    PICKUP = "PICKUP"
    DELIVERY = "DELIVERY"


class PaymentMethodEnum(str, Enum):
    CASH = "CASH"
    UPI = "UPI"


class PaymentStatusEnum(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


# ========================================
# HOSTEL SCHEMAS
# ========================================

class HostelBase(BaseModel):
    """Base schema with common hostel fields"""
    hostel_name: str = Field(..., min_length=1, max_length=100)
    hostel_type: str = Field(..., pattern="^(BOYS|GIRLS|CO-ED)$")
    address: Optional[str] = None


class HostelCreate(HostelBase):
    """Schema for creating a new hostel"""
    pass


class HostelResponse(HostelBase):
    """Schema for hostel API response"""
    hostel_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ========================================
# DEPARTMENT SCHEMAS
# ========================================

class DepartmentBase(BaseModel):
    """Base schema with common department fields"""
    department_name: str = Field(..., min_length=1, max_length=100)
    department_code: str = Field(..., min_length=1, max_length=10)


class DepartmentCreate(DepartmentBase):
    """Schema for creating a new department"""
    pass


class DepartmentResponse(DepartmentBase):
    """Schema for department API response"""
    department_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ========================================
# STUDENT SCHEMAS
# ========================================

class StudentBase(BaseModel):
    """Base schema with common student fields"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    roll_number: str = Field(..., min_length=1, max_length=20)
    phone: Optional[str] = Field(None, max_length=15)
    hostel_id: Optional[int] = None
    department_id: Optional[int] = None


class StudentCreate(StudentBase):
    """Schema for student registration"""
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    
    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, v):
        if not v.endswith("@visat.ac.in"):
            raise ValueError("Email must allow only VISAT domain (e.g., @visat.ac.in)")
        return v


class StudentLogin(BaseModel):
    """Schema for student login"""
    email: EmailStr
    password: str


class StudentUpdate(BaseModel):
    """Schema for updating student profile"""
    name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=15)
    hostel_id: Optional[int] = None
    department_id: Optional[int] = None


class StudentResponse(StudentBase):
    """Schema for student API response"""
    student_id: int
    created_at: datetime
    updated_at: datetime
    hostel: Optional[HostelResponse] = None
    department: Optional[DepartmentResponse] = None
    
    model_config = ConfigDict(from_attributes=True)


class StudentBrief(BaseModel):
    """Brief student info for nested responses"""
    student_id: int
    name: str
    roll_number: str
    email: Optional[str] = None
    phone: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# ========================================
# CANTEEN SCHEMAS
# ========================================

class CanteenBase(BaseModel):
    """Base schema with common canteen fields"""
    name: str = Field(..., min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=200)
    opening_time: Optional[str] = Field(None, max_length=10)
    closing_time: Optional[str] = Field(None, max_length=10)
    is_active: bool = True


class CanteenCreate(CanteenBase):
    """Schema for creating a new canteen"""
    pass


class CanteenUpdate(BaseModel):
    """Schema for updating canteen"""
    name: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=200)
    opening_time: Optional[str] = Field(None, max_length=10)
    closing_time: Optional[str] = Field(None, max_length=10)
    is_active: Optional[bool] = None


class CanteenResponse(CanteenBase):
    """Schema for canteen API response"""
    canteen_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ========================================
# MENU ITEM SCHEMAS
# ========================================

class MenuItemBase(BaseModel):
    """Base schema with common menu item fields"""
    item_name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    category: Optional[str] = Field(None, max_length=50)
    is_vegetarian: bool = True
    is_available: bool = True
    image_url: Optional[str] = None


class MenuItemCreate(MenuItemBase):
    """Schema for creating a new menu item"""
    canteen_id: int


class MenuItemUpdate(BaseModel):
    """Schema for updating menu item"""
    item_name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, max_length=50)
    is_vegetarian: Optional[bool] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None


class MenuItemResponse(MenuItemBase):
    """Schema for menu item API response"""
    item_id: int
    canteen_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class MenuItemBrief(BaseModel):
    """Brief menu item info for nested responses"""
    item_id: int
    item_name: str
    price: float
    
    model_config = ConfigDict(from_attributes=True)


# ========================================
# ORDER ITEM SCHEMAS
# ========================================

class OrderItemCreate(BaseModel):
    """Schema for creating an order item"""
    item_id: int
    quantity: int = Field(..., gt=0, description="Quantity must be positive")
    notes: Optional[str] = None


class OrderItemResponse(BaseModel):
    """Schema for order item API response"""
    order_item_id: int
    item_id: int
    quantity: int
    unit_price: float
    subtotal: float
    notes: Optional[str] = None
    menu_item: MenuItemBrief
    
    model_config = ConfigDict(from_attributes=True)


# ========================================
# DELIVERY PERSONNEL SCHEMAS
# ========================================

class DeliveryPersonnelBase(BaseModel):
    """Base schema for delivery personnel"""
    name: str = Field(..., min_length=1, max_length=100)
    roll_number: str = Field(..., min_length=1, max_length=20)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    is_available: bool = True


class DeliveryPersonnelCreate(DeliveryPersonnelBase):
    """Schema for creating delivery personnel"""
    password: str = Field(..., min_length=6)

class DeliveryLogin(BaseModel):
    """Schema for delivery personnel login"""
    email: EmailStr
    password: str

class DeliveryPersonnelResponse(DeliveryPersonnelBase):
    """Schema for returning delivery personnel data"""
    personnel_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)





# ========================================
# DELIVERY/PICKUP SCHEMAS
# ========================================

class DeliveryPickupCreate(BaseModel):
    """Schema for creating delivery/pickup info"""
    delivery_address: Optional[str] = None
    personnel_id: Optional[int] = None
    estimated_time: Optional[str] = None


class DeliveryPickupResponse(BaseModel):
    """Schema for delivery/pickup API response"""
    delivery_id: int
    order_id: int
    delivery_address: Optional[str] = None
    personnel_id: Optional[int] = None
    estimated_time: Optional[str] = None
    actual_delivery_time: Optional[datetime] = None
    is_delivered: bool
    personnel: Optional[DeliveryPersonnelResponse] = None
    
    model_config = ConfigDict(from_attributes=True)


# ========================================
# PAYMENT SCHEMAS
# ========================================

class PaymentCreate(BaseModel):
    """Schema for creating a payment"""
    order_id: int
    amount_paid: float = Field(..., gt=0)
    payment_method: PaymentMethodEnum
    transaction_id: Optional[str] = None
    payment_screenshot: Optional[str] = Field(None, description="Base64 encoded payment screenshot")


class PaymentUpdate(BaseModel):
    """Schema for updating payment status"""
    payment_status: Optional[PaymentStatusEnum] = None
    transaction_id: Optional[str] = None
    payment_screenshot: Optional[str] = Field(None, description="Base64 encoded payment screenshot")


class PaymentResponse(BaseModel):
    """Schema for payment API response"""
    payment_id: int
    order_id: int
    amount_paid: float
    payment_method: PaymentMethodEnum
    payment_status: PaymentStatusEnum
    transaction_id: Optional[str] = None
    payment_screenshot: Optional[str] = None
    payment_date: Optional[datetime] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ========================================
# ORDER SCHEMAS
# ========================================

class OrderCreate(BaseModel):
    """Schema for creating a new order"""
    student_id: int
    canteen_id: int
    order_type: OrderTypeEnum
    items: List[OrderItemCreate] = Field(..., min_length=1)
    special_instructions: Optional[str] = None
    delivery_info: Optional[DeliveryPickupCreate] = None


class OrderStatusUpdate(BaseModel):
    """Schema for updating order status"""
    order_status: OrderStatusEnum


class OrderResponse(BaseModel):
    """Schema for order API response"""
    order_id: int
    student_id: int
    canteen_id: int
    order_date: datetime
    order_status: OrderStatusEnum
    order_type: OrderTypeEnum
    total_amount: float
    special_instructions: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    student: StudentBrief
    order_items: List[OrderItemResponse] = []
    payment: Optional[PaymentResponse] = None
    delivery: Optional[DeliveryPickupResponse] = None
    
    model_config = ConfigDict(from_attributes=True)


class OrderBrief(BaseModel):
    """Brief order info for lists"""
    order_id: int
    order_date: datetime
    order_status: OrderStatusEnum
    order_type: OrderTypeEnum
    total_amount: float
    payment: Optional[PaymentResponse] = None
    
    model_config = ConfigDict(from_attributes=True)


# ========================================
# REPORT SCHEMAS
# ========================================

class DailyRevenueReport(BaseModel):
    """Schema for daily revenue report"""
    date: str
    total_orders: int
    completed_orders: int
    total_revenue: float
    cash_revenue: float
    upi_revenue: float


class StudentOrderHistory(BaseModel):
    """Schema for student order history"""
    student: StudentBrief
    total_orders: int
    total_spent: float
    orders: List[OrderBrief]


# ========================================
# GENERIC RESPONSE SCHEMAS
# ========================================

class Message(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    total: int
    page: int
    per_page: int
    pages: int
    data: List
