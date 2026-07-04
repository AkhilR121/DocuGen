# Troubleshooting Guide

## Common Issues and Solutions

### 1. ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'

**Error:**
```
ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'
```

**Cause:**
- You're using the wrong virtual environment
- The error shows `C:\Users\Technoidentity\Desktop\venv` instead of the project's `venv`

**Solution:**

#### Option A: Use the Startup Scripts (Recommended)

**Windows:**
```bash
cd server
start_server.bat
```

**Mac/Linux/Git Bash:**
```bash
cd server
chmod +x start_server.sh
./start_server.sh
```

#### Option B: Manual Steps

1. **Navigate to the server directory:**
   ```bash
   cd C:\Users\Technoidentity\Desktop\DocuGen\server
   ```

2. **Activate the CORRECT virtual environment:**
   
   **Windows (CMD):**
   ```bash
   venv\Scripts\activate.bat
   ```
   
   **Windows (PowerShell):**
   ```bash
   venv\Scripts\Activate.ps1
   ```
   
   **Windows (Git Bash):**
   ```bash
   source venv/Scripts/activate
   ```
   
   **Mac/Linux:**
   ```bash
   source venv/bin/activate
   ```

3. **Verify you're in the correct environment:**
   ```bash
   which python  # Should show the venv path
   python -c "import fastapi; print('FastAPI OK')"
   ```

4. **Start the server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
   ```

---

### 2. FastAPI Not Installed

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
cd server
source venv/Scripts/activate  # Activate venv first!
pip install -r requirements.txt
```

---

### 3. Wrong Directory

**Error:**
```
ERROR: No module named 'app.main'
```

**Cause:** You're not in the server directory

**Solution:**
```bash
cd C:\Users\Technoidentity\Desktop\DocuGen\server
# Then activate venv and start server
```

---

### 4. Port Already in Use

**Error:**
```
ERROR: [Errno 10048] Only one usage of each socket address
```

**Solution:**

**Find and kill the process using port 8080:**

**Windows:**
```bash
# Find the process
netstat -ano | findstr :8080

# Kill it (replace <PID> with the actual process ID)
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
# Find and kill the process
lsof -ti:8080 | xargs kill -9
```

---

### 5. CORS Configuration Error

**Error:**
```
SettingsError: error parsing value for field "CORS_ORIGINS"
```

**Solution:**
This has been fixed in the latest code. Ensure you have the updated files:

1. Check `server/app/core/config.py` uses `CORS_ORIGINS_STR`
2. Check `.env` file uses `CORS_ORIGINS_STR=http://localhost:5173,http://localhost:3000`

If issues persist:
```bash
cd server
git checkout server/app/core/config.py
cp .env.example .env
```

---

### 6. Database Connection Issues

**Error:**
```
sqlalchemy.exc.OperationalError: unable to open database file
```

**Solution:**
```bash
cd server
# Ensure the directory has write permissions
# The SQLite database will be created automatically
```

---

## Server Startup Checklist

✅ **Step 1:** Navigate to server directory
```bash
cd C:\Users\Technoidentity\Desktop\DocuGen\server
```

✅ **Step 2:** Check if virtual environment exists
```bash
ls venv/  # Should show Scripts/ folder
```

✅ **Step 3:** Activate virtual environment
```bash
source venv/Scripts/activate  # Git Bash
# OR
venv\Scripts\activate.bat     # CMD
```

✅ **Step 4:** Verify Python is from venv
```bash
which python  # Should show: .../DocuGen/server/venv/Scripts/python
```

✅ **Step 5:** Test imports
```bash
python -c "import fastapi, pydantic; print('OK')"
```

✅ **Step 6:** Check .env file exists
```bash
ls .env  # Should exist
```

✅ **Step 7:** Start server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

✅ **Step 8:** Verify server is running
Open browser: http://localhost:8080/docs

---

## Quick Commands

### Check Current Directory
```bash
pwd
# Should output: /c/Users/Technoidentity/Desktop/DocuGen/server
```

### Check Active Python
```bash
which python
# Should output: /c/Users/Technoidentity/Desktop/DocuGen/server/venv/Scripts/python
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Reinstall All Dependencies
```bash
cd server
source venv/Scripts/activate
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

## Environment Variables

Ensure your `.env` file has these values:

```env
# Application
APP_NAME=DocuGen API
APP_VERSION=0.1.0
DEBUG=True
ENVIRONMENT=development

# Server
HOST=0.0.0.0
PORT=8080

# Database
DATABASE_URL=sqlite:///./docugen.db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS_STR=http://localhost:5173,http://localhost:3000
```

---

## Testing the Server

Once the server starts, test these endpoints:

```bash
# Health check
curl http://localhost:8080/health
# Expected: {"status":"healthy"}

# Root endpoint
curl http://localhost:8080/
# Expected: {"message":"Welcome to DocuGen API",...}

# Example API
curl http://localhost:8080/api/v1/example/
# Expected: []
```

---

## Still Having Issues?

1. **Delete and recreate virtual environment:**
   ```bash
   cd server
   rm -rf venv
   python -m venv venv
   source venv/Scripts/activate
   pip install -r requirements.txt
   ```

2. **Check Python version:**
   ```bash
   python --version
   # Should be 3.11 or higher
   ```

3. **Check for typos in commands:**
   - Use `source venv/Scripts/activate` (Git Bash)
   - NOT `source venv/bin/activate` on Windows

4. **Ensure you're in the server directory:**
   ```bash
   cd C:\Users\Technoidentity\Desktop\DocuGen\server
   pwd  # Verify location
   ```

---

## Success Indicators

When the server starts correctly, you should see:

```
INFO:     Will watch for changes in these directories: ['C:\\Users\\Technoidentity\\Desktop\\DocuGen\\server']
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**URLs to verify:**
- 🌐 http://localhost:8080 - Root endpoint
- 📚 http://localhost:8080/docs - API documentation
- ✅ http://localhost:8080/health - Health check

---

**Need more help?** Check the main [README.md](../README.md) or [QUICK_START.md](../QUICK_START.md)
