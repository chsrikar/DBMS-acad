# 🚀 Render Deployment Guide

## College Canteen Food Ordering System - FastAPI Backend

This guide provides step-by-step instructions for deploying the FastAPI backend on Render.

---

## ✅ Prerequisites

- GitHub account with your project repository
- Render account (free tier available at [render.com](https://render.com))
- PostgreSQL database (can be created on Render)

---

## 📋 Pre-Deployment Checklist

The following files are already configured for Render deployment:

- ✅ **runtime.txt** - Specifies Python 3.11.9 (avoiding Python 3.14 compatibility issues)
- ✅ **requirements.txt** - Contains all necessary dependencies
- ✅ **app/main.py** - FastAPI app with CORS middleware configured
- ✅ **Health check endpoint** - `/health` for monitoring

---

## 🔧 Render Configuration

### Step 1: Create a New Web Service

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the **dbms-project** repository

### Step 2: Configure Build Settings

Use the following configuration:

| Setting | Value |
|---------|-------|
| **Name** | `canteen-api` (or your choice) |
| **Region** | Choose closest to your users |
| **Branch** | `main` (or your default branch) |
| **Root Directory** | Leave empty |
| **Runtime** | `Python 3` (will use runtime.txt) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port 10000` |
| **Instance Type** | Free (or paid for production) |

### Step 3: Environment Variables

Add the following environment variables in Render dashboard:

```bash
# Database URL (if using PostgreSQL on Render)
DATABASE_URL=postgresql://user:password@host:port/database

# Or for SQLite (not recommended for production)
DATABASE_URL=sqlite:///./canteen.db

# Application Settings
ENVIRONMENT=production
DEBUG=false

# Security (generate secure random strings)
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
```

**Note:** For production, use PostgreSQL instead of SQLite. You can create a free PostgreSQL database on Render.

---

## 🗄️ Database Setup (PostgreSQL)

### Option A: Render PostgreSQL (Recommended)

1. In Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Choose a name (e.g., `canteen-db`)
3. Select region (same as web service)
4. Create database
5. Copy the **Internal Database URL**
6. Add it as `DATABASE_URL` environment variable in your web service

### Option B: External Database

If using an external PostgreSQL/MySQL database, add the connection string as `DATABASE_URL`:

```bash
# PostgreSQL
DATABASE_URL=postgresql://user:password@host:port/database

# MySQL
DATABASE_URL=mysql+pymysql://user:password@host:port/database
```

---

## 🔄 Alternative Start Commands

### Option 1: Uvicorn (Recommended - Already configured)
```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

### Option 2: Uvicorn with Workers
```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000 --workers 4
```

### Option 3: Gunicorn with Uvicorn Workers
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:10000
```

---

## 🌐 Accessing Your API

After deployment, your API will be available at:

```
https://your-service-name.onrender.com
```

### Important Endpoints

- **Root**: `https://your-service-name.onrender.com/`
- **API Docs (Swagger UI)**: `https://your-service-name.onrender.com/docs`
- **ReDoc**: `https://your-service-name.onrender.com/redoc`
- **Health Check**: `https://your-service-name.onrender.com/health`

---

## 🔍 Health Check Configuration

Render supports automatic health checks. Configure in your service settings:

- **Health Check Path**: `/health`
- **Health Check Port**: `10000`

The app already has a health check endpoint that returns:
```json
{
  "status": "healthy"
}
```

---

## 🛠️ Troubleshooting

### Build Fails with Python 3.14 Error

**Solution**: Ensure `runtime.txt` exists in the root directory with:
```
python-3.11.9
```

### Database Connection Error

**Solution**: 
1. Check `DATABASE_URL` environment variable is set correctly
2. For PostgreSQL, use the **Internal Database URL** from Render
3. Ensure database service is running

### Import Errors

**Solution**: 
1. Verify all dependencies are in `requirements.txt`
2. Check build logs for specific missing packages
3. Rebuild the service

### CORS Errors

**Solution**: 
The app is already configured with CORS middleware. To restrict origins in production, update `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.com",
        "https://www.your-frontend-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Port Issues

**Solution**: 
Render requires port `10000` for free tier. The start command is already configured correctly.

---

## 📊 Database Migrations

If using SQLAlchemy with Alembic for migrations:

### Initial Setup
```bash
# After first deployment, run in Render Shell:
alembic upgrade head
```

### For Future Migrations
1. Create migration locally:
   ```bash
   alembic revision --autogenerate -m "your migration message"
   ```
2. Push to GitHub
3. Render will rebuild
4. Run in Render Shell:
   ```bash
   alembic upgrade head
   ```

---

## 🔐 Security Best Practices

1. **Never commit sensitive data** to GitHub
2. **Use environment variables** for secrets
3. **Restrict CORS origins** in production
4. **Enable HTTPS** (Render provides this automatically)
5. **Use strong database passwords**
6. **Regularly update dependencies**

---

## 📈 Monitoring

### Render Dashboard
- View logs in real-time
- Monitor CPU and memory usage
- Track deployment history

### Custom Logging
Add structured logging in your FastAPI app:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Application started successfully")
```

---

## 💰 Render Pricing

- **Free Tier**: 
  - 750 hours/month
  - Spins down after inactivity
  - Spins up on request (cold start ~30 seconds)
  
- **Paid Plans**:
  - Always running
  - No cold starts
  - More resources
  - Custom domains

---

## 🔗 Connecting Frontend

Update your frontend API base URL to:

```javascript
const API_BASE_URL = "https://your-service-name.onrender.com/api";
```

Ensure your frontend makes requests to the deployed backend URL.

---

## ✅ Deployment Verification

After deployment, verify:

1. ✅ Service is running (shows green in Render dashboard)
2. ✅ Root endpoint returns API information: `https://your-service-name.onrender.com/`
3. ✅ API docs are accessible: `https://your-service-name.onrender.com/docs`
4. ✅ Health check returns healthy: `https://your-service-name.onrender.com/health`
5. ✅ Database connection is working (test with API calls)

---

## 🎯 Example Render Configuration Summary

```yaml
# This is for reference - Render uses dashboard config, not YAML
service: web
name: canteen-api
runtime: python3.11
buildCommand: pip install -r requirements.txt
startCommand: uvicorn app.main:app --host 0.0.0.0 --port 10000
envVars:
  - key: DATABASE_URL
    sync: false
  - key: SECRET_KEY
    generateValue: true
  - key: ENVIRONMENT
    value: production
```

---

## 📞 Support

- **Render Documentation**: [render.com/docs](https://render.com/docs)
- **FastAPI Documentation**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **GitHub Issues**: Create an issue in your repository

---

## 🎉 Success!

Your FastAPI backend should now be successfully deployed on Render!

**Next Steps:**
1. Test all API endpoints via `/docs`
2. Deploy your frontend
3. Update frontend to use deployed API URL
4. Set up database backups
5. Configure custom domain (optional)

---

*Last Updated: March 2026*
