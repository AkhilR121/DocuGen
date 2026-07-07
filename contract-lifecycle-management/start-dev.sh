#!/bin/bash

# Contract Lifecycle Management - Development Startup Script

echo "=========================================="
echo "Starting CLM Development Environment"
echo "=========================================="

# Check if ports are available
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 5000 is already in use. Please stop the existing process."
    exit 1
fi

if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 3000 is already in use. Please stop the existing process."
    exit 1
fi

# Start backend server
echo ""
echo "🚀 Starting Backend Server (Flask)..."
cd server
python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to be ready..."
sleep 3

# Start frontend server
echo ""
echo "🎨 Starting Frontend Server (Vite)..."
cd client
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "=========================================="
echo "✅ Development environment started!"
echo "=========================================="
echo ""
echo "Backend:  http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "=========================================="

# Trap Ctrl+C to kill both processes
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit 0" INT

# Wait for processes
wait
