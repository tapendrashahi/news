#!/bin/bash

# Build React frontend for production

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Building React frontend for production...${NC}"
echo ""

cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Build
echo "Building..."
npm run build

echo ""
echo -e "${GREEN}Build complete!${NC}"
echo "Build files are in: frontend/build/"
echo ""
echo "To deploy, copy these files to Django's static directory:"
echo "  cp -r frontend/build/* static/react/"
