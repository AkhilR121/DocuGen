#!/bin/bash

echo "======================================"
echo "DocuGen Project Setup"
echo "======================================"

# Client setup
echo ""
echo "Setting up client (React + TypeScript + Vite)..."
cd client

if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

echo "Installing client dependencies..."
echo "Note: You need Node.js 18+ and npm 9+ installed"
echo "Run: npm install"

cd ..

# Server setup
echo ""
echo "Setting up server (Python FastAPI)..."
cd server

if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

echo "Creating Python virtual environment..."
python -m venv venv

echo ""
echo "======================================"
echo "Setup Instructions"
echo "======================================"
echo ""
echo "CLIENT:"
echo "  1. cd client"
echo "  2. npm install"
echo "  3. npm run dev"
echo "  -> Opens at http://localhost:5173"
echo ""
echo "SERVER:"
echo "  1. cd server"
echo "  2. Activate virtual environment:"
echo "     - Windows: venv\\Scripts\\activate"
echo "     - Mac/Linux: source venv/bin/activate"
echo "  3. pip install -r requirements.txt"
echo "  4. uvicorn app.main:app --reload"
echo "  -> Opens at http://localhost:8000"
echo "  -> Docs at http://localhost:8000/docs"
echo ""
echo "======================================"
echo "Setup complete!"
echo "======================================"
