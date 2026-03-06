# 🚀 Quick Start Guide
## College Canteen Food Ordering System

This guide will help you get the project running quickly.

---

## Prerequisites

1. **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
2. **pip** - Usually comes with Python

---

## Step-by-Step Setup

### 1️⃣ Open Terminal in Project Directory

```powershell
cd d:\dbms-project
```

### 2️⃣ Create Virtual Environment

```powershell
python -m venv venv
```

### 3️⃣ Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```powershell
pip install -r requirements.txt
```

### 5️⃣ Start the Server

```powershell
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started reloader process
✅ Database tables created successfully!
✅ Application ready!
```

### 6️⃣ Seed Sample Data (Optional)

In a new terminal (with venv activated):
```powershell
python seed_data.py
```

---

## 🔗 Access Points

| Description | URL |
|-------------|-----|
| **API Root** | http://localhost:8000 |
| **Swagger UI** (Interactive API Docs) | http://localhost:8000/docs |
| **ReDoc** (Alternative API Docs) | http://localhost:8000/redoc |

---

## 📝 Test the API

### Using Swagger UI (Recommended)

1. Open http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

### Using curl

**Get all menu items:**
```bash
curl http://localhost:8000/api/menu
```

**Create a student:**
```bash
curl -X POST http://localhost:8000/api/students/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Student",
    "email": "test@college.edu",
    "roll_number": "TEST001",
    "password": "password123"
  }'
```

**Place an order:**
```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "canteen_id": 1,
    "order_type": "PICKUP",
    "items": [
      {"item_id": 1, "quantity": 2},
      {"item_id": 3, "quantity": 1}
    ]
  }'
```

---

## 📊 Test Credentials (After Seeding)

| Email | Password |
|-------|----------|
| rahul@college.edu | password123 |
| priya@college.edu | password123 |
| amit@college.edu | password123 |
| sneha@college.edu | password123 |

---

## 🗄️ Database Location

By default, SQLite database is created at:
```
d:\dbms-project\canteen.db
```

To view the database, you can use:
- [DB Browser for SQLite](https://sqlitebrowser.org/)
- VS Code SQLite extension
- Python's sqlite3 command line

---

## 📂 Project Structure

```
dbms-project/
├── app/
│   ├── __init__.py          # Package init
│   ├── database.py          # DB connection & session
│   ├── models.py            # ORM models (tables)
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # CRUD operations
│   ├── main.py              # FastAPI app
│   └── routers/
│       ├── __init__.py
│       ├── students.py      # Student endpoints
│       ├── menu.py          # Menu endpoints
│       ├── orders.py        # Order endpoints
│       ├── payments.py      # Payment endpoints
│       └── canteen.py       # Canteen endpoints
├── docs/
│   └── DATABASE_SCHEMA.md   # Schema documentation
├── .env                     # Environment config
├── .env.example             # Config template
├── requirements.txt         # Dependencies
├── seed_data.py             # Sample data script
├── sql_queries.py           # SQL reference
└── README.md                # Project overview
```

---

## 🆘 Troubleshooting

### "Module not found" Error
Make sure virtual environment is activated (you should see `(venv)` in terminal)

### "Port already in use"
```powershell
uvicorn app.main:app --reload --port 8001
```

### Database locked
Stop the server (Ctrl+C) and try again

### PowerShell Execution Policy Error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🎓 For DBMS Viva

1. **Review** `docs/DATABASE_SCHEMA.md` for ER diagram and table details
2. **Study** `app/models.py` for ORM model definitions with SQL comments
3. **Examine** `sql_queries.py` for SQL equivalents
4. **Run** the API and trace SQL logs (enabled by default)

---

*Happy Learning! 🍽️*
