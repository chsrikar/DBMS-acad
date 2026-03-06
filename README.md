# 🍽️ College Canteen Food Ordering System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.25-red.svg)
![License](https://img.shields.io/badge/License-Academic-yellow.svg)

**A comprehensive Database Management System (DBMS) mini project demonstrating real-world implementation of relational database concepts through a modern food ordering platform.**

[Features](#-features) • [Tech Stack](#-technology-stack) • [Installation](#-installation) • [Architecture](#-architecture) • [Troubleshooting](#-troubleshooting)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Architecture](#-architecture)
  - [System Architecture](#system-architecture)
  - [Database Architecture](#database-architecture)
  - [Project Structure](#project-structure)
- [DBMS Concepts Demonstrated](#-dbms-concepts-demonstrated)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
  - [Windows Installation](#windows-installation)
  - [Linux/Mac Installation](#linuxmac-installation)
  - [Database Configuration](#database-configuration)
- [Running the Application](#-running-the-application)
- [Seeding Sample Data](#-seeding-sample-data)
- [Usage Guide](#-usage-guide)
  - [Student Features](#student-features)
  - [Admin Features](#admin-features)
  - [API Documentation](#api-documentation)
- [Troubleshooting](#-troubleshooting)
- [Testing](#-testing)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The **College Canteen Food Ordering System** is a full-stack web application designed as a DBMS mini project to demonstrate practical implementation of relational database concepts. The system enables students to browse menus, place orders, make payments, and track their order history, while canteen administrators can manage inventory, update order status, and generate revenue reports.

### Purpose

This project serves multiple purposes:
- **Academic**: Demonstrates core DBMS concepts (normalization, relationships, transactions, constraints)
- **Practical**: Provides a real-world solution to campus food ordering challenges
- **Learning**: Showcases modern web development practices with Python, FastAPI, and SQLAlchemy

### Key Highlights

✅ **Complete CRUD Operations** on all entities  
✅ **Complex Relationships** (1:1, 1:M, M:M)  
✅ **Transaction Management** for order processing  
✅ **RESTful API** with comprehensive documentation  
✅ **Modern Frontend** with responsive design  
✅ **Multiple Database Support** (SQLite, MySQL, PostgreSQL)  
✅ **Data Validation** using Pydantic schemas  
✅ **Security** with password hashing (bcrypt)  

---

## ✨ Features

### 🎓 Student Portal

| Feature | Description | DBMS Concept |
|---------|-------------|--------------|
| **User Registration** | Create account with email, roll number, hostel, and department | INSERT operation with UNIQUE constraints |
| **Authentication** | Secure login with password hashing | SELECT with WHERE clause, password verification |
| **Browse Menu** | View available food items by canteen and category | SELECT with JOIN operations |
| **Shopping Cart** | Add/remove items, view cart summary | In-memory state management |
| **Place Orders** | Submit orders with multiple items | TRANSACTION with multiple INSERTs |
| **Order Tracking** | Real-time status updates (Placed → Preparing → Ready → Delivered) | UPDATE operations with state machine |
| **Order History** | View past orders with complete details | SELECT with complex JOINs (4+ tables) |
| **Payment Processing** | Record payments via Cash/UPI | INSERT with foreign key relationship |
| **Profile Management** | Update personal information | UPDATE operation |

### 👨‍💼 Admin/Canteen Management

| Feature | Description | DBMS Concept |
|---------|-------------|--------------|
| **Inventory Management** | Add, update, delete menu items | CRUD operations |
| **Availability Toggle** | Mark items as available/unavailable | UPDATE with boolean flag |
| **Order Management** | View and update order status | SELECT with filtering, UPDATE status |
| **Revenue Reports** | Generate daily/monthly revenue summaries | Aggregate functions (SUM, COUNT) |
| **Student Analytics** | View active students and order patterns | GROUP BY queries |

### 🔧 System Features

- **API Documentation**: Auto-generated Swagger UI and ReDoc
- **Error Handling**: Comprehensive validation and error messages
- **Pagination**: Efficient data retrieval with skip/limit
- **CORS Support**: Frontend-backend communication
- **Database Migrations**: Schema version control (Alembic ready)
- **Seed Data**: Pre-populated test data for quick testing

---

## 🛠️ Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11+ | Core programming language |
| **FastAPI** | 0.109.0 | Modern, high-performance web framework |
| **SQLAlchemy** | 2.0.25 | SQL toolkit and ORM |
| **Pydantic** | 2.5.3 | Data validation using Python type hints |
| **Uvicorn** | 0.27.0 | Lightning-fast ASGI server |
| **Passlib** | 1.7.4 | Password hashing (bcrypt) |
| **Python-Jose** | 3.3.0 | JWT token handling (ready for authentication) |
| **Alembic** | 1.13.1 | Database migration tool |

### Database Support

| Database | Driver | Use Case |
|----------|--------|----------|
| **SQLite** | Built-in | Development, testing, quick demos |
| **MySQL** | pymysql 1.1.0 | Production deployment |
| **PostgreSQL** | psycopg2-binary 2.9.9 | Production deployment (advanced features) |

### Frontend

| Technology | Purpose |
|------------|---------|
| **HTML5** | Structure and semantics |
| **CSS3** | Modern styling with animations |
| **JavaScript (ES6+)** | Client-side logic and API interaction |
| **Fetch API** | HTTP requests to backend |

### Development Tools

- **VS Code**: Recommended IDE
- **Postman**: API testing
- **DB Browser for SQLite**: Database inspection
- **Git**: Version control

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │
│  │  Student UI   │  │   Admin UI    │  │  Mobile App   │       │
│  │  (Browser)    │  │  (Browser)    │  │  (Future)     │       │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘       │
│          │                   │                   │               │
│          └───────────────────┴───────────────────┘               │
│                              │                                   │
│                         HTTP/REST                                │
│                              │                                   │
└──────────────────────────────┼───────────────────────────────────┘
                               │
┌──────────────────────────────┼───────────────────────────────────┐
│                    APPLICATION LAYER                              │
│                              │                                   │
│                    ┌─────────▼──────────┐                        │
│                    │   FastAPI Server   │                        │
│                    │   (Uvicorn ASGI)   │                        │
│                    └─────────┬──────────┘                        │
│                              │                                   │
│          ┌───────────────────┼───────────────────┐               │
│          │                   │                   │               │
│    ┌─────▼─────┐      ┌─────▼─────┐      ┌─────▼─────┐         │
│    │  Students │      │   Orders  │      │  Canteen  │         │
│    │  Router   │      │   Router  │      │  Router   │         │
│    └─────┬─────┘      └─────┬─────┘      └─────┬─────┘         │
│          │                   │                   │               │
│          └───────────────────┼───────────────────┘               │
│                              │                                   │
│                    ┌─────────▼──────────┐                        │
│                    │   CRUD Operations  │                        │
│                    │   (Business Logic) │                        │
│                    └─────────┬──────────┘                        │
│                              │                                   │
│                    ┌─────────▼──────────┐                        │
│                    │   SQLAlchemy ORM   │                        │
│                    │   (Data Models)    │                        │
│                    └─────────┬──────────┘                        │
│                              │                                   │
└──────────────────────────────┼───────────────────────────────────┘
                               │
┌──────────────────────────────┼───────────────────────────────────┐
│                       DATABASE LAYER                              │
│                              │                                   │
│                    ┌─────────▼──────────┐                        │
│                    │  Relational DBMS   │                        │
│                    │  SQLite/MySQL/     │                        │
│                    │  PostgreSQL        │                        │
│                    └────────────────────┘                        │
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Students │  │  Orders  │  │  Canteen │  │ Payments │        │
│  │  Table   │  │  Table   │  │  Table   │  │  Table   │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└───────────────────────────────────────────────────────────────────┘
```

### Database Architecture

#### Entity-Relationship Diagram (ERD)

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   HOSTELS   │         │ DEPARTMENTS │         │  CANTEENS   │
├─────────────┤         ├─────────────┤         ├─────────────┤
│ hostel_id◆  │         │department_id│         │ canteen_id◆ │
│ name        │         │ name        │         │ name        │
│ type        │         │ code        │         │ location    │
│ address     │         └──────┬──────┘         │ hours       │
└──────┬──────┘                │                └──────┬──────┘
       │                       │                       │
       │ 1                     │ 1                   1 │
       │                       │                       │
       │ M                     │ M                   M │
       │         ┌─────────────┴─────────────┐         │
       └────────▶│        STUDENTS           │         │
                 ├───────────────────────────┤         │
                 │ student_id ◆              │         │
                 │ name                      │         │
                 │ email (UNIQUE)            │         │
                 │ roll_number (UNIQUE)      │         │
                 │ password_hash             │         │
                 │ hostel_id ◇               │         │
                 │ department_id ◇           │         │
                 └────────────┬──────────────┘         │
                              │                        │
                            1 │                        │
                              │                        │
                            M │                        │
                 ┌────────────┴──────────────┐         │
                 │        ORDERS             │◀────────┘
                 ├───────────────────────────┤
                 │ order_id ◆                │
                 │ student_id ◇              │
                 │ canteen_id ◇              │
                 │ order_date                │
                 │ order_status              │
                 │ order_type                │
                 │ total_amount              │
                 └─────┬──────┬───────┬──────┘
                       │      │       │
                     1 │    1 │       │ M
                       │      │       │
                     1 │    1 │       │ 1
         ┌─────────────┘      │       └───────────────┐
         │                    │                       │
┌────────▼────────┐  ┌────────▼────────┐   ┌─────────▼────────┐
│    PAYMENTS     │  │DELIVERY_PICKUPS │   │   ORDER_ITEMS    │
├─────────────────┤  ├─────────────────┤   ├──────────────────┤
│ payment_id ◆    │  │ delivery_id ◆   │   │ order_item_id ◆  │
│ order_id ◇      │  │ order_id ◇      │   │ order_id ◇       │
│ amount          │  │ personnel_id ◇  │   │ item_id ◇        │
│ method          │  │ delivery_time   │   │ quantity         │
│ status          │  │ location        │   │ unit_price       │
│ timestamp       │  │ instructions    │   │ subtotal         │
└─────────────────┘  └─────────────────┘   └──────────┬───────┘
                                                       │
                                                       │ M
                                                       │
                                                       │ 1
                                            ┌──────────▼───────┐
                                            │   MENU_ITEMS     │
                                            ├──────────────────┤
                                            │ item_id ◆        │
                                            │ canteen_id ◇     │
                                            │ name             │
                                            │ description      │
                                            │ price            │
                                            │ category         │
                                            │ is_vegetarian    │
                                            │ is_available     │
                                            └──────────────────┘

Legend:
  ◆ = Primary Key
  ◇ = Foreign Key
  1:M = One-to-Many Relationship
  1:1 = One-to-One Relationship
```

#### Database Tables

| Table | Records | Purpose | Relationships |
|-------|---------|---------|---------------|
| **hostels** | Master data | Store hostel information | 1:M with students |
| **departments** | Master data | Store department information | 1:M with students |
| **canteens** | Master data | Store canteen information | 1:M with menu_items, orders |
| **students** | Transaction | Store student accounts | M:1 with hostels/departments, 1:M with orders |
| **menu_items** | Master data | Store food items | M:1 with canteens, 1:M with order_items |
| **orders** | Transaction | Store order headers | M:1 with students/canteens, 1:M with order_items |
| **order_items** | Transaction | Store order line items | M:1 with orders/menu_items |
| **payments** | Transaction | Store payment records | 1:1 with orders |
| **delivery_pickups** | Transaction | Store delivery information | 1:1 with orders |
| **delivery_personnel** | Master data | Store delivery staff | 1:M with delivery_pickups |

### Project Structure

```
dbms-project/
│
├── app/                          # Backend application
│   ├── __init__.py               # Package initialization
│   ├── main.py                   # FastAPI application entry point
│   ├── database.py               # Database connection & session management
│   ├── models.py                 # SQLAlchemy ORM models (database tables)
│   ├── schemas.py                # Pydantic schemas (data validation)
│   ├── crud.py                   # CRUD operations (business logic)
│   │
│   └── routers/                  # API route handlers
│       ├── __init__.py           # Router exports
│       ├── students.py           # Student endpoints (/api/students/*)
│       ├── menu.py               # Menu endpoints (/api/menu/*)
│       ├── orders.py             # Order endpoints (/api/orders/*)
│       ├── payments.py           # Payment endpoints (/api/payments/*)
│       └── canteen.py            # Canteen endpoints (/api/canteen/*)
│
├── frontend/                     # Frontend application
│   ├── index.html                # Landing page
│   ├── menu.html                 # Browse menu
│   ├── cart.html                 # Shopping cart
│   ├── orders.html               # Order history & tracking
│   ├── profile.html              # User profile
│   ├── admin.html                # Admin dashboard
│   │
│   ├── css/                      # Stylesheets
│   │   ├── styles.css            # Main styles
│   │   ├── components.css        # Reusable components
│   │   └── admin.css             # Admin-specific styles
│   │
│   └── js/                       # JavaScript modules
│       ├── api.js                # API communication layer
│       ├── auth.js               # Authentication logic
│       ├── app.js                # Main application logic
│       ├── menu.js               # Menu browsing
│       ├── cart.js               # Cart management
│       ├── cart-page.js          # Cart page logic
│       ├── orders-page.js        # Orders page logic
│       ├── profile-page.js       # Profile page logic
│       ├── admin.js              # Admin dashboard
│       └── shared.js             # Shared utilities
│
├── docs/                         # Documentation
│   ├── DATABASE_SCHEMA.md        # Database design documentation
│   ├── PROJECT_GUIDE.md          # Comprehensive project guide
│   └── QUICK_START.md            # Quick setup instructions
│
├── requirements.txt              # Python dependencies
├── seed_data.py                  # Database seeding script
├── sql_queries.py                # Raw SQL query examples
├── canteen.db                    # SQLite database (created on first run)
├── .env                          # Environment variables (create this)
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

#### Directory Purpose

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| **`app/`** | Contains all backend Python code | `main.py`, `models.py`, `schemas.py` |
| **`app/routers/`** | API endpoint definitions organized by feature | `students.py`, `orders.py` |
| **`frontend/`** | Static HTML/CSS/JS files for the UI | `index.html`, `menu.html` |
| **`docs/`** | Project documentation and guides | `DATABASE_SCHEMA.md` |
| **Root** | Configuration and utility scripts | `requirements.txt`, `seed_data.py` |

---

## 📚 DBMS Concepts Demonstrated

This project comprehensively demonstrates the following database management concepts:

### 1. Database Design Principles

| Concept | Implementation | Example |
|---------|----------------|---------|
| **Normalization (3NF)** | Tables designed to eliminate redundancy | Hostels and Departments are separate tables referenced by Students |
| **Entity Integrity** | Every table has a primary key | `student_id`, `order_id`, `item_id` |
| **Referential Integrity** | Foreign keys with cascade rules | `orders.student_id` references `students.student_id` |
| **Domain Integrity** | Constraints on valid values | Check constraints on price > 0, enum for order status |

### 2. Relationships

| Type | Example | Implementation |
|------|---------|----------------|
| **One-to-Many (1:M)** | One Student → Many Orders | `students.student_id` ← `orders.student_id` (FK) |
| **Many-to-One (M:1)** | Many Orders → One Canteen | `orders.canteen_id` (FK) → `canteens.canteen_id` |
| **One-to-One (1:1)** | One Order → One Payment | `payments.order_id` (FK, UNIQUE) → `orders.order_id` |
| **Many-to-Many (M:M)** | Orders ↔ Menu Items | Through `order_items` junction table |

### 3. Constraints

```sql
-- Primary Key Constraint
student_id INT PRIMARY KEY AUTO_INCREMENT

-- Foreign Key Constraint with Cascade
FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE

-- Unique Constraint
email VARCHAR(255) UNIQUE NOT NULL

-- Check Constraint
CHECK (price >= 0)
CHECK (quantity > 0)

-- Not Null Constraint
student_name VARCHAR(255) NOT NULL

-- Default Constraint
is_available BOOLEAN DEFAULT TRUE
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### 4. SQL Operations

| Operation | Endpoint | SQL Concept |
|-----------|----------|-------------|
| **INSERT** | `POST /students/register` | Create new student record |
| **SELECT** | `GET /students/{id}` | Retrieve specific record |
| **UPDATE** | `PUT /orders/{id}/status` | Modify existing record |
| **DELETE** | `DELETE /menu/{id}` | Remove record (with cascade) |
| **JOIN** | `GET /students/{id}/orders` | Multi-table queries |
| **AGGREGATE** | `GET /canteen/reports` | SUM, COUNT, AVG functions |
| **GROUP BY** | Revenue by date | Grouping and aggregation |
| **ORDER BY** | Menu items by price | Sorting results |
| **LIMIT/OFFSET** | Pagination | Result set pagination |

### 5. Transactions

Order placement is implemented as an **ACID transaction**:

```python
# Transaction ensures atomicity
db.begin()
try:
    # 1. Create order header
    order = Order(...)
    db.add(order)
    db.flush()
    
    # 2. Create order items
    for item in items:
        order_item = OrderItem(...)
        db.add(order_item)
    
    # 3. Calculate total
    order.total_amount = sum(item.subtotal for item in order.items)
    
    # 4. Commit transaction
    db.commit()
except:
    db.rollback()  # Rollback on any error
    raise
```

**ACID Properties Demonstrated:**
- **Atomicity**: All operations succeed or all fail
- **Consistency**: Database remains in valid state
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed changes persist

### 6. Advanced Features

- **Triggers** (via SQLAlchemy events): Auto-update timestamps
- **Views** (via ORM relationships): Pre-defined JOIN queries
- **Indexes** (implicit): Primary keys automatically indexed
- **Stored Procedures** (ready): Can be added for complex operations
- **Password Security**: Bcrypt hashing with salt

---

## 📦 Prerequisites

Before installation, ensure you have the following installed:

### Required Software

| Software | Minimum Version | Download Link | Purpose |
|----------|----------------|---------------|---------|
| **Python** | 3.11+ | [python.org](https://www.python.org/downloads/) | Core runtime |
| **pip** | Latest | Comes with Python | Package manager |
| **Git** | Latest | [git-scm.com](https://git-scm.com/) | Version control (optional) |

### Verification

Open terminal/command prompt and verify installations:

```bash
# Check Python version (should be 3.11 or higher)
python --version
# or
python3 --version

# Check pip version
pip --version
# or
pip3 --version

# Check Git (optional)
git --version
```

### System Requirements

- **OS**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+)
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB for project + dependencies
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

---

## 🚀 Installation

### Windows Installation

#### Step 1: Download/Clone Project

**Option A: Download ZIP**
1. Download the project ZIP file
2. Extract to desired location (e.g., `D:\dbms-project`)

**Option B: Clone with Git**
```powershell
cd D:\
git clone <repository-url> dbms-project
cd dbms-project
```

#### Step 2: Open Terminal

1. Open PowerShell or Command Prompt
2. Navigate to project directory:
```powershell
cd D:\dbms-project
```

#### Step 3: Create Virtual Environment

A virtual environment isolates project dependencies from system Python.

```powershell
# Create virtual environment
python -m venv venv

# If above fails, try:
python3 -m venv venv
```

**Troubleshooting**: If you get "python not recognized":
- Add Python to PATH in System Environment Variables
- Use full path: `C:\Python311\python.exe -m venv venv`

#### Step 4: Activate Virtual Environment

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**If execution policy error occurs:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**Git Bash:**
```bash
source venv/Scripts/activate
```

**Success indicator**: Your prompt should show `(venv)` prefix:
```powershell
(venv) PS D:\dbms-project>
```

#### Step 5: Install Dependencies

```powershell
# Upgrade pip first (recommended)
python -m pip install --upgrade pip

# Install all project dependencies
pip install -r requirements.txt
```

**This installs:**
- FastAPI (web framework)
- SQLAlchemy (ORM)
- Uvicorn (server)
- Pydantic (validation)
- Passlib (password hashing)
- Database drivers (pymysql, psycopg2)
- Other utilities

**Installation time**: 2-5 minutes depending on internet speed

#### Step 6: Initialize Database

```powershell
# Start the server (this auto-creates database tables)
uvicorn app.main:app --reload
```

**What happens:**
1. SQLAlchemy creates `canteen.db` (SQLite database)
2. All tables are created based on models
3. Server starts on http://localhost:8000

**Stop the server**: Press `Ctrl+C`

#### Step 7: Seed Sample Data (Optional but Recommended)

```powershell
# Populate database with test data
python seed_data.py
```

**Sample data includes:**
- 2 Hostels (Boys, Girls)
- 5 Departments (CSE, ECE, ME, CE, EE)
- 2 Canteens with 10+ menu items
- 5 Sample students
- 3 Sample orders

---

### Linux/Mac Installation

#### Step 1: Clone/Download Project

```bash
cd ~
git clone <repository-url> dbms-project
cd dbms-project
```

#### Step 2: Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

#### Step 4: Initialize & Seed Database

```bash
# Start server to create tables
uvicorn app.main:app --reload &

# Wait 2 seconds, then stop
sleep 2
pkill -f uvicorn

# Seed data
python seed_data.py
```

---

### Database Configuration

By default, the project uses **SQLite** (no setup required). For production, use MySQL or PostgreSQL.

#### SQLite (Default)

No configuration needed. Database file is created at:
```
d:\dbms-project\canteen.db
```

#### MySQL Setup

1. Install MySQL Server
2. Create database:
```sql
CREATE DATABASE canteen_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'canteen_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON canteen_db.* TO 'canteen_user'@'localhost';
FLUSH PRIVILEGES;
```

3. Create `.env` file in project root:
```env
DATABASE_URL=mysql+pymysql://canteen_user:your_password@localhost:3306/canteen_db
```

4. Run server (tables auto-created):
```bash
uvicorn app.main:app --reload
```

#### PostgreSQL Setup

1. Install PostgreSQL Server
2. Create database:
```sql
CREATE DATABASE canteen_db;
CREATE USER canteen_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE canteen_db TO canteen_user;
```

3. Create `.env` file:
```env
DATABASE_URL=postgresql://canteen_user:your_password@localhost:5432/canteen_db
```

4. Run server:
```bash
uvicorn app.main:app --reload
```

---

## 🏃 Running the Application

### Start Backend Server

```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Start FastAPI server with auto-reload
uvicorn app.main:app --reload

# Server will start at http://127.0.0.1:8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Options:**
```bash
# Custom host/port
uvicorn app.main:app --host 0.0.0.0 --port 8080

# Disable auto-reload (production)
uvicorn app.main:app

# Enable verbose logging
uvicorn app.main:app --log-level debug
```

### Access Application

Once the server is running, open your browser:

| URL | Purpose |
|-----|---------|
| **http://localhost:8000** | API root |
| **http://localhost:8000/docs** | **Swagger UI** - Interactive API documentation |
| **http://localhost:8000/redoc** | **ReDoc** - Alternative API documentation |

### Open Frontend

Open the HTML files directly in your browser:

```powershell
# Windows - open default browser
start frontend/index.html

# Or manually navigate to:
# file:///D:/dbms-project/frontend/index.html
```

**For better experience, use Live Server:**
1. Install [VS Code Live Server extension](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
2. Right-click `frontend/index.html`
3. Select "Open with Live Server"
4. Frontend opens at `http://127.0.0.1:5500/frontend/index.html`

### Testing Setup

Verify everything is working:

1. **API Test**: Visit http://localhost:8000/docs
2. **Get Students**: Try `GET /api/students/` endpoint
3. **Frontend Test**: Open `frontend/index.html` in browser
4. **Login Test**: Use sample credentials:
   - Email: `john.doe@college.edu`
   - Password: `password123`

---

## 🌱 Seeding Sample Data

The seed script populates the database with realistic test data.

### Run Seed Script

```powershell
# Ensure server is running in another terminal
# Then run:
python seed_data.py
```

### Sample Data Created

| Entity | Count | Details |
|--------|-------|---------|
| **Hostels** | 2 | Boys Hostel, Girls Hostel |
| **Departments** | 5 | CSE, ECE, ME, CE, EE |
| **Canteens** | 2 | Main Canteen, Night Canteen |
| **Menu Items** | 12+ | Breakfast, Lunch, Dinner, Snacks |
| **Students** | 5 | With different departments/hostels |
| **Delivery Personnel** | 2 | Sample delivery staff |
| **Orders** | 3 | Orders in various states |
| **Payments** | 3 | Linked to orders |

### Sample User Credentials

| Name | Email | Password | Roll Number |
|------|-------|----------|-------------|
| John Doe | john.doe@college.edu | password123 | CS2021001 |
| Jane Smith | jane.smith@college.edu | password123 | EC2021002 |
| Bob Johnson | bob.johnson@college.edu | password123 | ME2021003 |
| Alice Williams | alice.williams@college.edu | password123 | CE2021004 |
| Charlie Brown | charlie.brown@college.edu | password123 | EE2021005 |

### Resetting Database

To start fresh:

```powershell
# Stop the server (Ctrl+C)

# Delete database file
Remove-Item canteen.db

# Restart server (recreates empty database)
uvicorn app.main:app --reload

# Re-seed data
python seed_data.py
```

---

## 📖 Usage Guide

### Student Features

#### 1. Registration

**Via API (Swagger UI):**
1. Go to http://localhost:8000/docs
2. Find `POST /api/students/register`
3. Click "Try it out"
4. Enter student details:
```json
{
  "name": "Test Student",
  "email": "test@college.edu",
  "roll_number": "CS2022001",
  "phone": "9876543210",
  "password": "securepass123",
  "hostel_id": 1,
  "department_id": 1
}
```
5. Click "Execute"

**Via Frontend:**
1. Open frontend/index.html
2. Click "Register" in navigation
3. Fill registration form
4. Submit

#### 2. Login

**Via API:**
```json
POST /api/students/login
{
  "email": "john.doe@college.edu",
  "password": "password123"
}
```

**Via Frontend:**
1. Click "Login" button
2. Enter credentials
3. Click "Sign In"

#### 3. Browse Menu

**Via API:**
```
GET /api/menu/
GET /api/menu/canteen/1
GET /api/menu/category/BREAKFAST
```

**Via Frontend:**
1. Navigate to "Menu" page
2. Filter by canteen or category
3. View item details

#### 4. Place Order

**Via API:**
```json
POST /api/orders/
{
  "student_id": 1,
  "canteen_id": 1,
  "order_type": "PICKUP",
  "items": [
    {"item_id": 1, "quantity": 2},
    {"item_id": 3, "quantity": 1}
  ]
}
```

**Via Frontend:**
1. Add items to cart
2. Review cart
3. Click "Place Order"
4. Confirm order details

#### 5. Track Orders

**Via API:**
```
GET /api/students/1/orders
GET /api/orders/1
```

**Via Frontend:**
1. Navigate to "My Orders" page
2. View all orders with status
3. Click order for details

#### 6. Make Payment

**Via API:**
```json
POST /api/payments/
{
  "order_id": 1,
  "payment_method": "UPI",
  "transaction_id": "TXN123456"
}
```

### Admin Features

#### 1. Manage Menu Items

**Add Item:**
```json
POST /api/menu/
{
  "canteen_id": 1,
  "item_name": "Masala Dosa",
  "description": "South Indian crispy dosa",
  "price": 60.00,
  "category": "BREAKFAST",
  "is_vegetarian": true,
  "is_available": true
}
```

**Update Item:**
```json
PUT /api/menu/1
{
  "price": 65.00,
  "is_available": true
}
```

**Delete Item:**
```
DELETE /api/menu/1
```

#### 2. Update Order Status

```json
PUT /api/orders/1/status
{
  "order_status": "PREPARING"
}
```

**Valid Transitions:**
- PLACED → PREPARING
- PREPARING → READY
- READY → DELIVERED
- Any → CANCELLED

#### 3. View Reports

**Daily Revenue:**
```
GET /api/canteen/1/revenue?date=2026-03-06
```

**Response:**
```json
{
  "date": "2026-03-06",
  "canteen_name": "Main Canteen",
  "total_orders": 25,
  "total_revenue": 1250.00,
  "completed_orders": 23,
  "cancelled_orders": 2
}
```

### API Documentation

#### Authentication

Currently, authentication is **simplified for academic purposes**. In production:
- Use JWT tokens
- Implement role-based access control (RBAC)
- Add authentication middleware

#### Base URL

```
http://localhost:8000/api
```

#### Response Format

**Success Response:**
```json
{
  "student_id": 1,
  "name": "John Doe",
  "email": "john.doe@college.edu",
  "roll_number": "CS2021001"
}
```

**Error Response:**
```json
{
  "detail": "Student with ID 999 not found"
}
```

#### Status Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST |
| 400 | Bad Request | Validation error, duplicate entry |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Data validation failed |
| 500 | Server Error | Internal server error |

#### Pagination

Most list endpoints support pagination:

```
GET /api/students/?skip=0&limit=10
GET /api/orders/?skip=20&limit=10
```

#### Complete API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **Students** |
| POST | `/api/students/register` | Register new student |
| POST | `/api/students/login` | Student login |
| GET | `/api/students/` | Get all students |
| GET | `/api/students/{id}` | Get student by ID |
| PUT | `/api/students/{id}` | Update student |
| GET | `/api/students/{id}/orders` | Get student's order history |
| **Menu** |
| GET | `/api/menu/` | Get all menu items |
| POST | `/api/menu/` | Add new menu item |
| GET | `/api/menu/{id}` | Get menu item by ID |
| PUT | `/api/menu/{id}` | Update menu item |
| DELETE | `/api/menu/{id}` | Delete menu item |
| GET | `/api/menu/canteen/{id}` | Get menu by canteen |
| GET | `/api/menu/category/{category}` | Get menu by category |
| **Orders** |
| POST | `/api/orders/` | Place new order |
| GET | `/api/orders/{id}` | Get order details |
| PUT | `/api/orders/{id}/status` | Update order status |
| GET | `/api/orders/status/{status}` | Get orders by status |
| GET | `/api/orders/student/{id}` | Get orders by student |
| **Payments** |
| POST | `/api/payments/` | Record payment |
| GET | `/api/payments/{id}` | Get payment details |
| PUT | `/api/payments/{id}/status` | Update payment status |
| GET | `/api/payments/order/{order_id}` | Get payment for order |
| **Canteen** |
| GET | `/api/canteen/` | Get all canteens |
| POST | `/api/canteen/` | Add new canteen |
| GET | `/api/canteen/{id}` | Get canteen by ID |
| GET | `/api/canteen/{id}/revenue` | Get revenue report |

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. "python is not recognized"

**Problem**: Python not in PATH

**Solutions:**
```powershell
# Option A: Add Python to PATH (Windows)
# 1. Search "Environment Variables" in Start Menu
# 2. Click "Environment Variables"
# 3. Under "System variables", find "Path"
# 4. Click "Edit" → "New"
# 5. Add: C:\Python311\
# 6. Add: C:\Python311\Scripts\
# 7. Click "OK" and restart terminal

# Option B: Use full path
C:\Python311\python.exe -m venv venv

# Option C: Use Python launcher
py -m venv venv
```

#### 2. PowerShell Execution Policy Error

**Problem**: 
```
.\venv\Scripts\Activate.ps1 : File cannot be loaded because running scripts is disabled
```

**Solution:**
```powershell
# Set execution policy for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate again
.\venv\Scripts\Activate.ps1
```

#### 3. Port Already in Use

**Problem**:
```
ERROR: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)
```

**Solutions:**
```powershell
# Option A: Use different port
uvicorn app.main:app --port 8001

# Option B: Kill process using port 8000
# Find process ID
netstat -ano | findstr :8000

# Kill process (replace <PID> with actual number)
taskkill /PID <PID> /F

# Option C: Restart computer
```

#### 4. Module Not Found

**Problem**:
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solutions:**
```powershell
# Ensure venv is activated (should see (venv) in prompt)
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt

# If still fails, check pip location
pip --version
# Should show path inside venv folder

# Force reinstall
pip install --force-reinstall -r requirements.txt
```

#### 5. Database Locked (SQLite)

**Problem**:
```
sqlite3.OperationalError: database is locked
```

**Solutions:**
```powershell
# Stop all running server instances (Ctrl+C)

# Delete database and recreate
Remove-Item canteen.db
uvicorn app.main:app --reload
python seed_data.py

# Or wait and retry (SQLite releases lock after timeout)
```

#### 6. CORS Errors in Frontend

**Problem**: 
```
Access to fetch at 'http://localhost:8000/api/...' from origin 'file://' has been blocked by CORS
```

**Solutions:**
```powershell
# Option A: Use Live Server extension in VS Code
# Option B: Use Python HTTP server
cd frontend
python -m http.server 8080
# Open http://localhost:8080/index.html

# Option C: Disable browser security (NOT RECOMMENDED)
# Chrome: --disable-web-security --user-data-dir="C:/temp"
```

#### 7. Foreign Key Constraint Error

**Problem**:
```
IntegrityError: FOREIGN KEY constraint failed
```

**Solutions:**
- Ensure referenced IDs exist (e.g., hostel_id exists in hostels table)
- Check seeded data was loaded: `python seed_data.py`
- Verify relationships in Swagger UI `/docs`

#### 8. Password Hashing Error

**Problem**:
```
ValueError: Invalid salt
```

**Solutions:**
```powershell
# Reinstall passlib with bcrypt
pip uninstall passlib
pip install passlib[bcrypt]

# Or install bcrypt separately
pip install bcrypt
```

#### 9. Uvicorn Doesn't Auto-Reload

**Problem**: Code changes not reflected

**Solutions:**
- Ensure using `--reload` flag
- Check console for syntax errors
- Manually restart server (Ctrl+C, then start again)
- Use debug logging: `uvicorn app.main:app --reload --log-level debug`

#### 10. Can't Connect to MySQL/PostgreSQL

**Problem**:
```
OperationalError: (2003, "Can't connect to MySQL server")
```

**Solutions:**
```powershell
# Check database service is running
# MySQL:
net start MySQL80

# PostgreSQL:
net start postgresql-x64-14

# Verify credentials in .env file
# Check DATABASE_URL format

# Test connection separately
python -c "import pymysql; pymysql.connect(host='localhost', user='root', password='yourpass')"
```

### Getting Help

If you encounter issues not listed here:

1. **Check Server Logs**: Look for error messages in terminal
2. **Verify Database**: Use DB Browser to inspect `canteen.db`
3. **Test API**: Use Swagger UI at `/docs` to test endpoints
4. **Check Dependencies**: Ensure all packages in `requirements.txt` are installed
5. **Review Documentation**: See `docs/` folder for detailed guides

---

## 🧪 Testing

### Manual Testing with Swagger UI

1. Start server: `uvicorn app.main:app --reload`
2. Open http://localhost:8000/docs
3. Test each endpoint:

**Example Test Flow:**
1. Register student → `POST /api/students/register`
2. Login student → `POST /api/students/login`
3. Get menu → `GET /api/menu/`
4. Place order → `POST /api/orders/`
5. Get order → `GET /api/orders/{id}`
6. Make payment → `POST /api/payments/`
7. Update status → `PUT /api/orders/{id}/status`

### Database Inspection

**SQLite (DB Browser):**
1. Download [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Open `canteen.db`
3. Browse tables, run queries

**SQL Queries:**
```sql
-- View all students
SELECT * FROM students;

-- View orders with student info
SELECT o.*, s.name, s.email
FROM orders o
JOIN students s ON o.student_id = s.student_id;

-- Revenue by date
SELECT DATE(order_date) as date, SUM(total_amount) as revenue
FROM orders
WHERE order_status = 'DELIVERED'
GROUP BY DATE(order_date);
```

### Automated Testing (Future)

```bash
# Install pytest
pip install pytest pytest-cov

# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

---

## 🚀 Future Enhancements

### Planned Features

- [ ] **JWT Authentication**: Secure token-based auth
- [ ] **Real-time Updates**: WebSocket for live order tracking
- [ ] **Payment Gateway**: Integrate Razorpay/Stripe
- [ ] **Email Notifications**: Order confirmations via email
- [ ] **SMS Alerts**: Twilio integration for order updates
- [ ] **Rating System**: Rate food items and delivery
- [ ] **Search & Filters**: Advanced menu search
- [ ] **Favorites**: Save favorite food items
- [ ] **Reorder**: Quick reorder from history
- [ ] **Offers & Coupons**: Discount management
- [ ] **Analytics Dashboard**: Charts for admin
- [ ] **Mobile Apps**: React Native/Flutter apps
- [ ] **Multi-language**: i18n support
- [ ] **Dark Mode**: Theme switcher

### Technical Improvements

- [ ] Migration scripts with Alembic
- [ ] Comprehensive test suite (pytest)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Docker containerization
- [ ] Redis caching for performance
- [ ] Celery for background tasks
- [ ] API rate limiting
- [ ] Advanced logging (ELK stack)
- [ ] Monitoring (Prometheus + Grafana)
- [ ] OpenAPI spec generation

---

## 🤝 Contributing

This is an academic project, but contributions are welcome!
version 1.0 created by chinthapenta srikar in collabration with Vimal J Mathew

### How to Contribute

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/NewFeature`
3. **Commit changes**: `git commit -m 'Add NewFeature'`
4. **Push to branch**: `git push origin feature/NewFeature`
5. **Open Pull Request**

### Contribution Guidelines

- Follow existing code style
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting
- Write meaningful commit messages

### Areas for Contribution

- Bug fixes
- New features
- Documentation improvements
- Test coverage
- Performance optimization
- UI/UX enhancements

---

## 📄 License

This project is created for **academic purposes** as a DBMS mini project demonstration.

### Usage Rights

✅ **Permitted:**
- Use for learning and education
- Modify and extend for your own projects
- Reference in academic work (with citation)
- Share with classmates

❌ **Not Permitted:**
- Commercial use without permission
- Claiming as original work (plagiarism)
- Redistribution without attribution

### Citation

If you use this project in your academic work, please cite:

```
College Canteen Food Ordering System
DBMS Mini Project
2026
Available at: [repository-url]
```

---

## 📞 Support & Contact

### Documentation

- **Database Schema**: See [docs/DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md)
- **Project Guide**: See [docs/PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md)
- **Quick Start**: See [docs/QUICK_START.md](docs/QUICK_START.md)

### Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Python Docs**: https://docs.python.org/3/

### Acknowledgments

- FastAPI framework by Sebastián Ramírez
- SQLAlchemy by Michael Bayer
- All open-source contributors

---

<div align="center">

### ⭐ Star this project if you found it helpful!

**Made with ❤️ for DBMS learning**

</div>

---

## 📋 Quick Reference

### Essential Commands

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload

# Seed database
python seed_data.py

# Deactivate venv
deactivate
```

### Important URLs

- **API Server**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Frontend**: file:///path/to/frontend/index.html

### Sample Credentials

- **Email**: `john.doe@college.edu`
- **Password**: `password123`

### Project Info

- **Python**: 3.11+
- **Framework**: FastAPI 0.109.0
- **ORM**: SQLAlchemy 2.0.25
- **Database**: SQLite (dev), MySQL/PostgreSQL (prod)
- **Port**: 8000 (default)

---

**Last Updated**: March 6, 2026  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
