# 🍽️ FOODLAB - College Food Ordering System

## Complete Project Guide

---

## 📖 Table of Contents

1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Technology Stack](#-technology-stack)
4. [Project Structure](#-project-structure)
5. [Database Design](#-database-design)
6. [DBMS Concepts Used](#-dbms-concepts-used)
7. [Installation & Setup](#-installation--setup)
8. [Running the Application](#-running-the-application)
9. [Using the Application](#-using-the-application)
10. [API Endpoints](#-api-endpoints)
11. [For Viva Preparation](#-for-viva-preparation)

---

## 🎯 Project Overview

**FOODLAB** is a full-stack web-based food ordering system designed for a college canteen. It allows students to browse the menu, add items to cart, place orders, and track their delivery. The canteen staff can manage incoming orders, update order status, and view reports.

### Purpose
This project is developed as a **DBMS Mini Project** to demonstrate:
- Relational database design principles
- Normalization up to Third Normal Form (3NF)
- CRUD operations using ORM
- API development with proper data validation
- Frontend-backend integration

### Who Uses This System?

| User Type | What They Can Do |
|-----------|------------------|
| **Students** | Browse menu, add to cart, place orders, track orders, view profile |
| **Canteen Staff** | View orders, update status, manage menu availability, view reports |

---

## ✨ Features

### Student Side (Main App)
- 🏠 **Home Page** - Welcome screen with animated design
- 📋 **Menu Browser** - View all food items with filters
- 🛒 **Shopping Cart** - Add/remove items, adjust quantities
- 📦 **Order Placement** - Choose pickup time or delivery
- 👤 **Profile** - View registered details and order history
- 🔐 **Authentication** - Register and login

### Admin Side (Canteen Dashboard)
- 📊 **Order Management** - View all incoming orders
- ⏱️ **Status Updates** - Mark orders as Preparing → Ready → Delivered
- 🍕 **Menu Management** - Toggle item availability
- 📈 **Daily Reports** - View revenue and order statistics

### Special Features
- ⏰ **Pickup Time Slots** - Morning Break, Lunch Break, Afternoon Break
- 🚚 **Delivery Options** - To classroom or hostel (Boys/Girls)
- 💵 **Delivery Charge** - ₹5 for delivery orders
- 🔄 **Real-time Updates** - Auto-refresh every 30 seconds

---

## 🛠️ Technology Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Programming language |
| **FastAPI** | Modern web framework for building APIs |
| **SQLAlchemy 2.0** | ORM (Object-Relational Mapper) for database operations |
| **Pydantic** | Data validation and serialization |
| **SQLite** | Database (can switch to MySQL/PostgreSQL) |
| **Uvicorn** | ASGI server to run the application |
| **Bcrypt** | Password hashing for security |

### Frontend
| Technology | Purpose |
|------------|---------|
| **HTML5** | Page structure |
| **CSS3** | Styling with modern design (glassmorphism, animations) |
| **JavaScript (ES6+)** | Client-side logic and API calls |
| **Google Fonts (Inter)** | Typography |

### Why These Technologies?

1. **FastAPI** - Fastest Python framework with automatic API documentation
2. **SQLAlchemy** - Industry-standard ORM that maps Python classes to database tables
3. **SQLite** - Zero-configuration database, perfect for development
4. **Vanilla JS** - No framework overhead, easy to understand

---

## 📁 Project Structure

```
FOODLAB (dbms-project)/
│
├── 📂 app/                      # Backend Application
│   ├── __init__.py              # Package initializer
│   ├── main.py                  # FastAPI application entry point
│   ├── database.py              # Database connection & session
│   ├── models.py                # SQLAlchemy ORM models (tables)
│   ├── schemas.py               # Pydantic schemas (validation)
│   ├── crud.py                  # CRUD operations
│   └── 📂 routers/              # API route handlers
│       ├── students.py          # Student endpoints
│       ├── menu.py              # Menu endpoints
│       ├── orders.py            # Order endpoints
│       ├── payments.py          # Payment endpoints
│       └── canteen.py           # Canteen/Admin endpoints
│
├── 📂 frontend/                 # Frontend Application
│   ├── index.html               # Main student page
│   ├── admin.html               # Admin dashboard
│   ├── 📂 css/
│   │   ├── styles.css           # Main styles
│   │   ├── components.css       # Component styles
│   │   └── admin.css            # Admin-specific styles
│   └── 📂 js/
│       ├── api.js               # API communication
│       ├── auth.js              # Authentication handling
│       ├── cart.js              # Shopping cart logic
│       ├── app.js               # Main application logic
│       └── admin.js             # Admin dashboard logic
│
├── 📂 docs/                     # Documentation
│   ├── DATABASE_SCHEMA.md       # Database design document
│   ├── QUICK_START.md           # Quick setup guide
│   └── PROJECT_GUIDE.md         # This file
│
├── canteen.db                   # SQLite database file
├── seed_data.py                 # Script to populate sample data
├── sql_queries.py               # SQL query reference
├── requirements.txt             # Python dependencies
├── .env                         # Environment configuration
└── README.md                    # Project readme
```

---

## 🗄️ Database Design

### Entity-Relationship Overview

```
┌──────────────┐         ┌──────────────┐
│   HOSTELS    │         │  DEPARTMENTS │
└──────┬───────┘         └──────┬───────┘
       │ 1                      │ 1
       │                        │
       │ N                      │ N
┌──────┴───────────────────────┴───────┐
│              STUDENTS                 │
└──────────────────┬───────────────────┘
                   │ 1
                   │
                   │ N
┌──────────────────┴───────────────────┐
│               ORDERS                  │
└────────┬─────────────────┬───────────┘
         │ 1               │ 1
         │                 │
         │ N               │ 1
┌────────┴───────┐   ┌─────┴──────┐
│  ORDER_ITEMS   │   │  PAYMENTS  │
└────────┬───────┘   └────────────┘
         │ N
         │
         │ 1
┌────────┴───────┐
│   MENU_ITEMS   │
└────────┬───────┘
         │ N
         │
         │ 1
┌────────┴───────┐
│    CANTEENS    │
└────────────────┘
```

### Database Tables (10 Tables Total)

| Table | Description | Key Fields |
|-------|-------------|------------|
| `hostels` | Student hostels | hostel_id, hostel_name |
| `departments` | Academic departments | department_id, department_name |
| `students` | Registered students | student_id, name, email, roll_number |
| `canteens` | College canteens | canteen_id, canteen_name, location |
| `menu_items` | Food items available | item_id, item_name, price, category |
| `orders` | Customer orders | order_id, student_id, total_amount, status |
| `order_items` | Items in each order | order_item_id, order_id, item_id, quantity |
| `payments` | Payment records | payment_id, order_id, amount, method |
| `delivery_pickup` | Delivery information | id, order_id, delivery_address |
| `delivery_personnel` | Delivery staff | personnel_id, name, phone |

---

## 📚 DBMS Concepts Used

### 1. Primary Keys
Every table has a unique identifier (Primary Key) to ensure each row is unique.
```sql
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ...
);
```

### 2. Foreign Keys
Tables are linked using Foreign Keys to maintain referential integrity.
```sql
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    ...
);
```

### 3. Normalization (up to 3NF)

**First Normal Form (1NF)**
- All columns contain atomic (single) values
- No repeating groups

**Second Normal Form (2NF)**
- Meets 1NF
- All non-key attributes depend on the entire primary key

**Third Normal Form (3NF)**
- Meets 2NF
- No transitive dependencies
- Example: `hostel_name` is stored in `hostels` table, not in `students`

### 4. Relationships

| Type | Example |
|------|---------|
| **One-to-Many** | One Student → Many Orders |
| **Many-to-One** | Many Menu Items → One Canteen |
| **One-to-One** | One Order → One Payment |

### 5. Constraints

| Constraint | Purpose | Example |
|------------|---------|---------|
| `NOT NULL` | Field must have a value | `name VARCHAR NOT NULL` |
| `UNIQUE` | Value must be unique | `email VARCHAR UNIQUE` |
| `CHECK` | Value must satisfy condition | `price DECIMAL CHECK(price > 0)` |
| `DEFAULT` | Provides default value | `status VARCHAR DEFAULT 'PLACED'` |

### 6. Transactions
Order creation uses transactions to ensure all related inserts succeed or fail together.
```python
try:
    db.add(order)
    db.add(payment)
    db.commit()  # Save all changes
except:
    db.rollback()  # Undo all changes if error
```

### 7. Aggregate Functions
Used in reports to calculate statistics.
```sql
SELECT COUNT(*) as total_orders,
       SUM(total_amount) as total_revenue
FROM orders
WHERE DATE(order_date) = '2026-01-10';
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Web browser (Chrome/Firefox recommended)

### Step-by-Step Setup

#### Step 1: Open Terminal/Command Prompt
Navigate to the project folder:
```bash
cd d:\dbms-project
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Setup Environment File
The `.env` file is already configured. Default settings:
```
DATABASE_URL=sqlite:///./canteen.db
SECRET_KEY=your-secret-key-here
```

#### Step 5: Seed Sample Data (Optional)
```bash
python seed_data.py
```
This creates sample data including test users, menu items, and orders.

---

## ▶️ Running the Application

### Start Backend Server
```bash
# Make sure virtual environment is activated
.\venv\Scripts\activate

# Start the FastAPI server
.\venv\Scripts\uvicorn.exe app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

### Start Frontend Server
Open a **new terminal** and run:
```bash
cd frontend
python -m http.server 3000
```

The frontend will be available at:
- Student App: http://localhost:3000
- Admin Dashboard: http://localhost:3000/admin.html

### Test Credentials
```
Email: rahul@college.edu
Password: password123
```

---

## 📱 Using the Application

### For Students

1. **Open** http://localhost:3000
2. **Browse Menu** - Click "Browse Menu" or use the Menu tab
3. **Filter Items** - Use category tabs (Breakfast, Lunch, etc.)
4. **Add to Cart** - Click "Add to Cart" on items
5. **View Cart** - Click the Cart tab
6. **Choose Order Type**:
   - **Pickup**: Select a time slot
   - **Delivery**: Choose classroom/hostel + ₹5 charge
7. **Place Order** - Click "Place Order"
8. **Track Order** - Go to "My Orders" to see status

### For Canteen Staff (Admin)

1. **Open** http://localhost:3000/admin.html
2. **View Orders** - See all orders with their status
3. **Filter by Status** - Click New, Preparing, Ready, or Delivered
4. **Update Status**:
   - New order → Click "Start Preparing"
   - Preparing → Click "Mark Ready"
   - Ready → Click "Mark Delivered"
5. **View Details** - Click "View Details" for full info
6. **Manage Menu** - Toggle item availability
7. **View Reports** - Check daily revenue

---

## 🔌 API Endpoints

### Students
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/students/register` | Register new student |
| POST | `/api/students/login` | Login student |
| GET | `/api/students/{id}` | Get student details |
| GET | `/api/students/{id}/orders` | Get student's orders |

### Menu
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/menu` | Get all menu items |
| GET | `/api/menu/{id}` | Get specific item |
| PUT | `/api/menu/{id}/toggle` | Toggle availability |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/orders` | Create new order |
| GET | `/api/orders/{id}` | Get order details |
| PUT | `/api/orders/{id}/status` | Update order status |
| GET | `/api/orders/status/{status}` | Get orders by status |

### Reports
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reports/revenue` | Get daily revenue report |

---

## 🎓 For Viva Preparation

### Common Questions & Answers

**Q1: What is the purpose of this project?**
> To demonstrate a practical application of database management concepts including normalization, CRUD operations, and relational database design.

**Q2: Why did you use SQLite?**
> SQLite is a zero-configuration database that's perfect for development and small-scale applications. It can be easily replaced with MySQL or PostgreSQL for production.

**Q3: Explain the normalization in your database.**
> The database is in 3NF:
> - 1NF: All values are atomic (no arrays)
> - 2NF: No partial dependencies (all attributes depend on the full primary key)
> - 3NF: No transitive dependencies (hostel_name is in hostels table, not students)

**Q4: What is an ORM and why use it?**
> ORM (Object-Relational Mapper) maps Python classes to database tables. SQLAlchemy allows us to:
> - Write database operations in Python instead of SQL
> - Automatic SQL injection prevention
> - Database-agnostic code

**Q5: How is password security handled?**
> Passwords are hashed using bcrypt before storing. Plain passwords are never stored in the database.

**Q6: Explain the order lifecycle.**
> PLACED → PREPARING → READY → DELIVERED
> Each status change is validated - you can't skip steps.

**Q7: What are foreign key constraints?**
> Foreign keys ensure referential integrity. For example, an order must reference a valid student_id that exists in the students table.

**Q8: How are concurrent orders handled?**
> SQLAlchemy sessions are scoped per request, and transactions ensure data consistency. If an error occurs, all changes are rolled back.

### Key SQL Queries to Know

```sql
-- Join query (Orders with Student Details)
SELECT o.order_id, s.name, o.total_amount
FROM orders o
JOIN students s ON o.student_id = s.student_id;

-- Aggregate query (Daily Revenue)
SELECT DATE(order_date) as date,
       COUNT(*) as total_orders,
       SUM(total_amount) as revenue
FROM orders
GROUP BY DATE(order_date);

-- Subquery (Students who ordered today)
SELECT * FROM students
WHERE student_id IN (
    SELECT student_id FROM orders
    WHERE DATE(order_date) = DATE('now')
);
```

---

## 📞 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 already in use | Kill the process or use a different port |
| Module not found | Activate virtual environment: `.\venv\Scripts\activate` |
| Database error | Delete `canteen.db` and run `seed_data.py` again |
| CORS error in browser | Make sure backend is running on port 8000 |
| Frontend not updating | Clear browser cache (Ctrl+Shift+R) |

---

## 📄 License

This project is developed for academic purposes as a DBMS Mini Project.

---

**Made with ❤️ for DBMS Mini Project**
