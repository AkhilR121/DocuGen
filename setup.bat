@echo off
echo ======================================
echo DocuGen Project Setup
echo ======================================

REM Client setup
echo.
echo Setting up client (React + TypeScript + Vite)...
cd client

if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
)

echo Installing client dependencies...
echo Note: You need Node.js 18+ and npm 9+ installed
echo Run: npm install

cd ..

REM Server setup
echo.
echo Setting up server (Python FastAPI)...
cd server

if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
)

echo Creating Python virtual environment...
python -m venv venv

cd ..

echo.
echo ======================================
echo Setup Instructions
echo ======================================
echo.
echo CLIENT:
echo   1. cd client
echo   2. npm install
echo   3. npm run dev
echo   -^> Opens at http://localhost:5173
echo.
echo SERVER:
echo   1. cd server
echo   2. Activate virtual environment: venv\Scripts\activate
echo   3. pip install -r requirements.txt
echo   4. uvicorn app.main:app --reload
echo   -^> Opens at http://localhost:8000
echo   -^> Docs at http://localhost:8000/docs
echo.
echo ======================================
echo Setup complete!
echo ======================================

pause
