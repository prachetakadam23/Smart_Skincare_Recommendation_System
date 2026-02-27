@echo off
REM Aurelia Skincare App - Quick Start Guide for Windows

echo ==========================================
echo Aurelia Skincare App - Quick Start (Windows)
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    color 6
    echo Python is not installed. Please install Python 3.8+
    pause
    exit /b 1
)

REM Step 1: Backend Setup
echo.
echo [STEP 1] Setting up Backend...
echo ===============================
cd backend

REM Check if pip can import tensorflow
python -c "import tensorflow" >nul 2>&1
if errorlevel 1 (
    color 3
    echo Installing Python dependencies...
    pip install -r requirements.txt
    color 2
    echo. Dependencies installed
) else (
    color 2
    echo. Dependencies already installed
)

REM Test NLP model
echo.
echo Testing NLP model...
python -c "from nlp_model import get_chat_response; print('NLP Model Working: OK')"
if errorlevel 1 (
    color 4
    echo Warning: NLP model test failed
) else (
    color 2
    echo. NLP Model verified
)

color 2
echo.
echo Backend setup complete!
echo.
echo To start the backend, run:
echo   python app.py
echo Backend will run on: http://localhost:5000
echo.
pause

REM Step 2: Frontend Setup
echo.
echo [STEP 2] Setting up Frontend...
echo ===============================
cd ..\frontend

if not exist "node_modules" (
    color 3
    echo Installing npm dependencies...
    call npm install
    color 2
    echo. Dependencies installed
) else (
    color 2
    echo. Dependencies already installed
)

color 2
echo.
echo Frontend setup complete!
echo.
echo To start the frontend, run:
echo   npm run dev
echo Frontend will run on: http://localhost:5173
echo.

echo ==========================================
color 2
echo Setup Complete!
color 7
echo ==========================================
echo.
echo HOW TO RUN:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   python app.py
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo To test the backend:
echo   cd backend
echo   python test_api.py
echo.
echo ==========================================
echo.
pause
