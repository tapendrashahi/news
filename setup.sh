#!/bin/bash

# React + Django News Portal Setup Script
# This script sets up the complete development environment

set -e  # Exit on error

echo "======================================"
echo "React + Django Setup Script"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo -e "${RED}Error: manage.py not found. Please run this script from the project root.${NC}"
    exit 1
fi

# Backend Setup
echo -e "${BLUE}[1/5] Setting up Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate

echo -e "${BLUE}[2/5] Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Install additional packages for React integration
pip install djangorestframework django-cors-headers markdown django-filter

echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Update requirements.txt
pip freeze > requirements.txt

# Frontend Setup
echo -e "${BLUE}[3/5] Setting up React frontend...${NC}"
cd frontend

if [ ! -f "package.json" ]; then
    echo -e "${RED}Error: package.json not found in frontend directory${NC}"
    exit 1
fi

echo "Installing Node.js dependencies..."
npm install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
fi

cd ..

# Database Setup
echo -e "${BLUE}[4/5] Setting up database...${NC}"
python manage.py migrate

echo -e "${GREEN}✓ Database migrations completed${NC}"

# Create superuser prompt
echo -e "${BLUE}[5/5] Create Django superuser...${NC}"
echo "Would you like to create a superuser now? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
fi

echo ""
echo -e "${GREEN}======================================"
echo "Setup Complete! 🎉"
echo "======================================${NC}"
echo ""
echo "To start development:"
echo ""
echo -e "${BLUE}Terminal 1 - Django Backend:${NC}"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo -e "${BLUE}Terminal 2 - React Frontend:${NC}"
echo "  cd frontend"
echo "  npm start"
echo ""
echo -e "${BLUE}Access:${NC}"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000/api"
echo "  Django Admin: http://localhost:8000/admin"
echo ""
