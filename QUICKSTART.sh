#!/usr/bin/env bash
# Aurelia Skincare App - Quick Start Guide

echo "=========================================="
echo "Aurelia Skincare App - Quick Start"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo -e "${YELLOW}Python is not installed. Please install Python 3.8+${NC}"
    exit 1
fi

echo -e "${BLUE}Step 1: Setting up Backend${NC}"
echo "==============================="
cd backend

# Check if requirements are installed
if ! python -c "import tensorflow" 2>/dev/null; then
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
fi

# Verify NLP model is created
if [ -f "nlp_model.py" ]; then
    echo -e "${GREEN}✓ NLP model file exists${NC}"
else
    echo -e "${YELLOW}Warning: nlp_model.py not found${NC}"
fi

# Test models
echo ""
echo -e "${BLUE}Testing Models...${NC}"
python -c "from nlp_model import get_chat_response; print('✓ NLP model working: ' + get_chat_response('hello')[:50])"

echo ""
echo -e "${GREEN}Backend setup complete!${NC}"
echo "Run this to start backend: python app.py"
echo "Backend will run on: http://localhost:5000"
echo ""

# Go to frontend directory
cd ../frontend

echo -e "${BLUE}Step 2: Setting up Frontend${NC}"
echo "==============================="

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing npm dependencies...${NC}"
    npm install
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
fi

echo ""
echo -e "${GREEN}Frontend setup complete!${NC}"
echo "Run this to start frontend: npm run dev"
echo "Frontend will run on: http://localhost:5173"
echo ""

echo "=========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "To run the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  python app.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "To test the backend:"
echo "  cd backend"
echo "  python test_api.py"
echo ""
echo "=========================================="
