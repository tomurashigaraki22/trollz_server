#!/bin/bash

# Sendbox Integration Setup Script
# This script helps you set up the Sendbox integration for Trollz Store

set -e  # Exit on error

echo "========================================================================"
echo "  TROLLZ STORE - SENDBOX INTEGRATION SETUP"
echo "========================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠ .env file not found. Creating from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file${NC}"
    echo ""
    echo -e "${YELLOW}IMPORTANT: Please edit .env and add your Sendbox API key!${NC}"
    echo "  1. Register at: https://developers.staging.sendbox.co/"
    echo "  2. Create an application and copy your API key"
    echo "  3. Edit .env and set SENDBOX_API_KEY=your_key_here"
    echo ""
    read -p "Press Enter when you've updated .env with your API key..."
else
    echo -e "${GREEN}✓ .env file found${NC}"
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    echo "Please install Python 3.7 or higher"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 is installed${NC}"

# Check if required Python packages are installed
echo ""
echo "Checking Python dependencies..."
python3 -c "import pymysql" 2>/dev/null || {
    echo -e "${YELLOW}⚠ Installing pymysql...${NC}"
    pip3 install pymysql
}
python3 -c "import requests" 2>/dev/null || {
    echo -e "${YELLOW}⚠ Installing requests...${NC}"
    pip3 install requests
}
python3 -c "import dotenv" 2>/dev/null || {
    echo -e "${YELLOW}⚠ Installing python-dotenv...${NC}"
    pip3 install python-dotenv
}
echo -e "${GREEN}✓ All dependencies installed${NC}"

# Run migrations
echo ""
echo "========================================================================"
echo "  RUNNING DATABASE MIGRATIONS"
echo "========================================================================"
echo ""
python3 run_migrations.py run

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Migrations completed successfully${NC}"
else
    echo ""
    echo -e "${RED}✗ Migration failed${NC}"
    echo "Please check the error messages above and fix any issues."
    exit 1
fi

# Run setup tests
echo ""
echo "========================================================================"
echo "  VERIFYING SETUP"
echo "========================================================================"
echo ""
python3 test_sendbox_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================================================"
    echo -e "${GREEN}  ✓ SETUP COMPLETE!${NC}"
    echo "========================================================================"
    echo ""
    echo "Next steps:"
    echo "  1. Review PHASE1_SETUP_GUIDE.md for detailed information"
    echo "  2. Start implementing Phase 2 (Shipping Quotes)"
    echo "  3. See SENDBOX_INTEGRATION_PHASES.md for the full roadmap"
    echo ""
    echo "Useful commands:"
    echo "  - List migrations: python3 run_migrations.py list"
    echo "  - Test setup: python3 test_sendbox_setup.py"
    echo "  - Start server: python3 app.py"
    echo ""
else
    echo ""
    echo "========================================================================"
    echo -e "${YELLOW}  ⚠ SETUP COMPLETED WITH WARNINGS${NC}"
    echo "========================================================================"
    echo ""
    echo "Some tests failed. Common issues:"
    echo "  - Missing or invalid SENDBOX_API_KEY in .env"
    echo "  - Database connection issues"
    echo "  - Incorrect warehouse address configuration"
    echo ""
    echo "Please review the errors above and run:"
    echo "  python3 test_sendbox_setup.py"
    echo ""
fi
