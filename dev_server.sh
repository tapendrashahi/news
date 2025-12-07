#!/bin/bash

# Start both Django and React development servers

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Starting Development Servers...${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${BLUE}Stopping servers...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup EXIT INT TERM

# Start Django backend
echo -e "${BLUE}Starting Django backend on http://localhost:8000${NC}"
source venv/bin/activate
python manage.py runserver &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start React frontend
echo -e "${BLUE}Starting React frontend on http://localhost:3000${NC}"
cd frontend
npm start &
FRONTEND_PID=$!

echo ""
echo -e "${GREEN}Both servers are running!${NC}"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for processes
wait
