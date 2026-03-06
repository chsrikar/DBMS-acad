# 📊 Database Schema Documentation
## College Canteen Food Ordering System - DBMS Mini Project

This document provides a comprehensive overview of the database schema,
designed for academic understanding and DBMS viva preparation.

---

## 🏗️ Entity-Relationship Diagram (ERD)

```
┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
│    HOSTELS      │          │   DEPARTMENTS   │          │    CANTEENS     │
├─────────────────┤          ├─────────────────┤          ├─────────────────┤
│ hostel_id (PK)  │          │ department_id(PK│          │ canteen_id (PK) │
│ hostel_name     │          │ department_name │          │ name            │
│ hostel_type     │          │ department_code │          │ location        │
│ address         │          │ created_at      │          │ opening_time    │
│ created_at      │          └────────┬────────┘          │ closing_time    │
└────────┬────────┘                   │                   │ is_active       │
         │                            │                   └────────┬────────┘
         │ 1:M                        │ 1:M                        │ 1:M
         ▼                            ▼                            ▼
┌─────────────────────────────────────────────┐          ┌─────────────────┐
│                  STUDENTS                    │          │   MENU_ITEMS    │
├─────────────────────────────────────────────┤          ├─────────────────┤
│ student_id (PK)                              │          │ item_id (PK)    │
│ name                                         │          │ canteen_id (FK) │◄───┐
│ email (UNIQUE)                               │          │ item_name       │    │
│ roll_number (UNIQUE)                         │          │ description     │    │
│ phone                                        │          │ price           │    │
│ password_hash                                │          │ category        │    │
│ hostel_id (FK) ──────────────────────────────┼──────────│ is_vegetarian   │    │
│ department_id (FK) ──────────────────────────┘          │ is_available    │    │
│ created_at                                              │ created_at      │    │
│ updated_at                                              │ updated_at      │    │
└────────────────────┬────────────────────────┘          └────────┬────────┘    │
                     │                                             │             │
                     │ 1:M                                         │ 1:M         │
                     ▼                                             │             │
┌─────────────────────────────────────────────┐                   │             │
│                   ORDERS                     │                   │             │
├─────────────────────────────────────────────┤                   │             │
│ order_id (PK)                                │                   │             │
│ student_id (FK) ─────────────────────────────┤                   │             │
│ canteen_id (FK) ─────────────────────────────┼───────────────────┼─────────────┘
│ order_date                                   │                   │
│ order_status (ENUM)                          │                   │
│ order_type (ENUM)                            │                   │
│ total_amount                                 │                   │
│ special_instructions                         │                   │
│ created_at                                   │                   │
│ updated_at                                   │                   │
└───────┬──────────┬──────────┬───────────────┘                   │
        │          │          │                                    │
        │ 1:M      │ 1:1      │ 1:1                                │
        ▼          ▼          ▼                                    │
┌───────────────┐ ┌─────────────────┐ ┌─────────────────┐          │
│ ORDER_ITEMS   │ │    PAYMENTS     │ │DELIVERY_PICKUPS │          │
├───────────────┤ ├─────────────────┤ ├─────────────────┤          │
│order_item_id  │ │ payment_id (PK) │ │ delivery_id(PK) │          │
│  (PK)         │ │ order_id(FK,UNQ)│ │ order_id(FK,UNQ)│          │
│order_id (FK)──┤ │ amount_paid     │ │ delivery_address│          │
│item_id (FK)───┼─┤ payment_method  │ │ personnel_id(FK)│──┐       │
│quantity       │ │ payment_status  │ │ estimated_time  │  │       │
│unit_price     │ │ transaction_id  │ │actual_del_time  │  │       │
│subtotal       │ │ payment_date    │ │ is_delivered    │  │       │
│notes          │ │ created_at      │ │ created_at      │  │       │
└───────────────┘ └─────────────────┘ └─────────────────┘  │       │
        │                                                   │       │
        │ M:1                                               │ M:1   │
        ▼                                                   ▼       │
        └───────────────────────────────────────────────────┼───────┘
                                                            │
                                          ┌─────────────────┴───────┐
                                          │  DELIVERY_PERSONNEL     │
                                          ├─────────────────────────┤
                                          │ personnel_id (PK)       │
                                          │ name                    │
                                          │ phone (UNIQUE)          │
                                          │ is_available            │
                                          │ created_at              │
                                          └─────────────────────────┘
```

---

## 📋 Table Details

### 1. HOSTELS (Master Data)
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| hostel_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| hostel_name | VARCHAR(100) | NOT NULL, UNIQUE | Hostel name |
| hostel_type | VARCHAR(20) | NOT NULL | BOYS, GIRLS, or CO-ED |
| address | TEXT | - | Physical address |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation time |

**Purpose**: Store hostel master data, referenced by students.
**Normalization**: Eliminates redundancy - hostel info stored once.

---

### 2. DEPARTMENTS (Master Data)
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| department_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| department_name | VARCHAR(100) | NOT NULL, UNIQUE | Full department name |
| department_code | VARCHAR(10) | NOT NULL, UNIQUE | Short code (CSE, ECE) |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation time |

**Purpose**: Store department master data.
**Normalization**: Achieves 3NF by separating department info.

---

### 3. STUDENTS
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| student_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Student's full name |
| email | VARCHAR(100) | NOT NULL, UNIQUE | Login email |
| roll_number | VARCHAR(20) | NOT NULL, UNIQUE | College roll number |
| phone | VARCHAR(15) | - | Contact number |
| password_hash | VARCHAR(255) | NOT NULL | Encrypted password |
| hostel_id | INTEGER | FOREIGN KEY → hostels | Student's hostel |
| department_id | INTEGER | FOREIGN KEY → departments | Student's department |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Registration time |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update time |

**Relationships**:
- M:1 with HOSTELS (many students in one hostel)
- M:1 with DEPARTMENTS (many students in one department)
- 1:M with ORDERS (one student can have many orders)

---

### 4. CANTEENS
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| canteen_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Canteen name |
| location | VARCHAR(200) | - | Campus location |
| opening_time | VARCHAR(10) | - | Opening time (HH:MM) |
| closing_time | VARCHAR(10) | - | Closing time (HH:MM) |
| is_active | BOOLEAN | DEFAULT TRUE | Operational status |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation time |

**Relationships**:
- 1:M with MENU_ITEMS (one canteen has many items)
- 1:M with ORDERS (one canteen receives many orders)

---

### 5. MENU_ITEMS
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| item_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| canteen_id | INTEGER | FOREIGN KEY → canteens, NOT NULL | Parent canteen |
| item_name | VARCHAR(100) | NOT NULL | Food item name |
| description | TEXT | - | Item description |
| price | DECIMAL(10,2) | NOT NULL, CHECK > 0 | Current price |
| category | VARCHAR(50) | - | Breakfast, Lunch, etc. |
| is_vegetarian | BOOLEAN | DEFAULT TRUE | Veg/Non-veg flag |
| is_available | BOOLEAN | DEFAULT TRUE | Current availability |
| image_url | VARCHAR(500) | - | Item image |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update |

**Relationships**:
- M:1 with CANTEENS (many items in one canteen)
- 1:M with ORDER_ITEMS (one item in many orders)

---

### 6. ORDERS (Transaction Header)
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| order_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| student_id | INTEGER | FOREIGN KEY → students, NOT NULL | Ordering student |
| canteen_id | INTEGER | FOREIGN KEY → canteens, NOT NULL | Target canteen |
| order_date | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Order placement time |
| order_status | ENUM | DEFAULT 'PLACED' | Status workflow |
| order_type | ENUM | NOT NULL | PICKUP or DELIVERY |
| total_amount | DECIMAL(10,2) | DEFAULT 0 | Calculated total |
| special_instructions | TEXT | - | Special requests |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update |

**Order Status Values**: PLACED → PREPARING → READY → DELIVERED (or CANCELLED)

**Relationships**:
- M:1 with STUDENTS (many orders from one student)
- M:1 with CANTEENS (many orders to one canteen)
- 1:M with ORDER_ITEMS (one order has many items)
- 1:1 with PAYMENTS (one order has one payment)
- 1:1 with DELIVERY_PICKUPS (one order has one delivery record)

---

### 7. ORDER_ITEMS (Transaction Detail)
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| order_item_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| order_id | INTEGER | FOREIGN KEY → orders, CASCADE DELETE | Parent order |
| item_id | INTEGER | FOREIGN KEY → menu_items | Ordered item |
| quantity | INTEGER | NOT NULL, CHECK > 0 | Quantity ordered |
| unit_price | DECIMAL(10,2) | NOT NULL | Price at order time |
| subtotal | DECIMAL(10,2) | NOT NULL | quantity × unit_price |
| notes | TEXT | - | Item-specific notes |

**Why store unit_price separately?**
Menu prices can change. We store the price at order time to maintain historical accuracy.

**Relationships**:
- M:1 with ORDERS (many items in one order)
- M:1 with MENU_ITEMS (one menu item in many orders)

---

### 8. PAYMENTS
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| payment_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| order_id | INTEGER | FOREIGN KEY → orders, UNIQUE, CASCADE DELETE | Related order |
| amount_paid | DECIMAL(10,2) | NOT NULL | Payment amount |
| payment_method | ENUM | NOT NULL | CASH or UPI |
| payment_status | ENUM | DEFAULT 'PENDING' | Payment state |
| transaction_id | VARCHAR(100) | - | UPI transaction ID |
| payment_date | TIMESTAMP | - | When completed |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation time |

**Payment Status Values**: PENDING → COMPLETED/FAILED, COMPLETED → REFUNDED

**Relationship**: 1:1 with ORDERS (UNIQUE constraint on order_id)

---

### 9. DELIVERY_PICKUPS
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| delivery_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| order_id | INTEGER | FOREIGN KEY → orders, UNIQUE, CASCADE DELETE | Related order |
| delivery_address | TEXT | - | Delivery location |
| personnel_id | INTEGER | FOREIGN KEY → delivery_personnel | Assigned person |
| estimated_time | VARCHAR(50) | - | ETA |
| actual_delivery_time | TIMESTAMP | - | When delivered |
| is_delivered | BOOLEAN | DEFAULT FALSE | Confirmation flag |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation time |

**Relationships**:
- 1:1 with ORDERS (UNIQUE constraint on order_id)
- M:1 with DELIVERY_PERSONNEL (many deliveries by one person)

---

### 10. DELIVERY_PERSONNEL
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| personnel_id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Staff name |
| phone | VARCHAR(15) | NOT NULL, UNIQUE | Contact number |
| is_available | BOOLEAN | DEFAULT TRUE | Available for delivery |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation time |

**Relationship**: 1:M with DELIVERY_PICKUPS (one person handles many deliveries)

---

## 🔑 Key Relationships Summary

### One-to-Many (1:M)
| Parent | Child | Foreign Key |
|--------|-------|-------------|
| Hostel | Student | students.hostel_id |
| Department | Student | students.department_id |
| Student | Order | orders.student_id |
| Canteen | MenuItem | menu_items.canteen_id |
| Canteen | Order | orders.canteen_id |
| Order | OrderItem | order_items.order_id |
| MenuItem | OrderItem | order_items.item_id |
| DeliveryPersonnel | DeliveryPickup | delivery_pickups.personnel_id |

### One-to-One (1:1)
| Table A | Table B | Constraint |
|---------|---------|------------|
| Order | Payment | payments.order_id UNIQUE |
| Order | DeliveryPickup | delivery_pickups.order_id UNIQUE |

---

## 📐 Normalization Analysis

### First Normal Form (1NF) ✅
- All attributes contain atomic values
- No repeating groups (items stored in separate ORDER_ITEMS table)
- Each row uniquely identifiable by primary key

### Second Normal Form (2NF) ✅
- In 1NF
- All non-key attributes depend on entire primary key
- No partial dependencies

### Third Normal Form (3NF) ✅
- In 2NF
- No transitive dependencies
- Examples:
  - Hostel details separated from Students
  - Department details separated from Students
  - Menu items separated from Orders (via ORDER_ITEMS)

---

## 🔒 Constraints Summary

| Constraint Type | Example |
|-----------------|---------|
| PRIMARY KEY | student_id, order_id, etc. |
| FOREIGN KEY | orders.student_id → students.student_id |
| UNIQUE | students.email, students.roll_number |
| NOT NULL | name, email, price |
| CHECK | price > 0, quantity > 0 |
| DEFAULT | is_available DEFAULT TRUE |
| CASCADE DELETE | order_items deleted when order deleted |

---

## 💡 VIVA Questions & Answers

**Q1: Why separate Hostels and Departments into different tables?**
A: To achieve 3NF and eliminate redundancy. If hostel info was stored in Students, we'd repeat the same hostel address for every student in that hostel.

**Q2: Why store unit_price in ORDER_ITEMS when it's already in MENU_ITEMS?**
A: Menu prices can change over time. We need to preserve the historical price at which the order was placed.

**Q3: What happens when an Order is deleted?**
A: Due to CASCADE DELETE, all related ORDER_ITEMS, PAYMENTS, and DELIVERY_PICKUPS are automatically deleted.

**Q4: How is the order total calculated?**
A: SUM of all subtotals from ORDER_ITEMS where order_id matches.

**Q5: What enforces the 1:1 relationship between Order and Payment?**
A: The UNIQUE constraint on payments.order_id ensures each order can have only one payment record.

---

*This document was created for academic purposes - DBMS Mini Project*
