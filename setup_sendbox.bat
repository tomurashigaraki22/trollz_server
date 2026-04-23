@echo off
REM Sendbox Integration Setup Script for Windows
REM This script helps you set up the Sendbox integration for Trollz Store

echo ========================================================================
echo   TROLLZ STORE - SENDBOX INTEGRATION SETUP
echo ========================================================================
echo.

REM Check if .env exists
if not exist .env (
    echo [WARNING] .env file not found. Creating from template...
    copy .env.example .env
    echo [OK] Created .env file
    echo.
    echo IMPORTANT: Please edit .env and add your Sendbox API key!
    echo   1. Register at: https://developers.staging.sendbox.co/
    echo   2. Create an application and copy your API key
    echo   3. Edit .env and set SENDBOX_API_KEY=your_key_here
    echo.
    pause
) else (
    echo [OK] .env file found
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    echo Please install Python 3.7 or higher from https://www.python.org/
    pause
    exit /b 1
)
echo [OK] Python is installed

REM Check and install dependencies
echo.
echo Checking Python dependencies...
python -c "import pymysql" 2>nul || (
    echo [INFO] Installing pymysql...
    pip install pymysql
)
python -c "import requests" 2>nul || (
    echo [INFO] Installing requests...
    pip install requests
)
python -c "import dotenv" 2>nul || (
    echo [INFO] Installing python-dotenv...
    pip install python-dotenv
)
echo [OK] All dependencies installed

REM Run migrations
echo.
echo ========================================================================
echo   RUNNING DATABASE MIGRATIONS
echo ========================================================================
echo.
python run_migrations.py run

if errorlevel 1 (
    echo.
    echo [ERROR] Migration failed
    echo Please check the error messages above and fix any issues.
    pause
    exit /b 1
)

echo.
echo [OK] Migrations completed successfully

REM Run setup tests
echo.
echo ========================================================================
echo   VERIFYING SETUP
echo ========================================================================
echo.
python test_sendbox_setup.py

if errorlevel 1 (
    echo.
    echo ========================================================================
    echo   [WARNING] SETUP COMPLETED WITH WARNINGS
    echo ========================================================================
    echo.
    echo Some tests failed. Common issues:
    echo   - Missing or invalid SENDBOX_API_KEY in .env
    echo   - Database connection issues
    echo   - Incorrect warehouse address configuration
    echo.
    echo Please review the errors above and run:
    echo   python test_sendbox_setup.py
    echo.
) else (
    echo.
    echo ========================================================================
    echo   [OK] SETUP COMPLETE!
    echo ========================================================================
    echo.
    echo Next steps:
    echo   1. Review PHASE1_SETUP_GUIDE.md for detailed information
    echo   2. Start implementing Phase 2 (Shipping Quotes^)
    echo   3. See SENDBOX_INTEGRATION_PHASES.md for the full roadmap
    echo.
    echo Useful commands:
    echo   - List migrations: python run_migrations.py list
    echo   - Test setup: python test_sendbox_setup.py
    echo   - Start server: python app.py
    echo.
)

pause
