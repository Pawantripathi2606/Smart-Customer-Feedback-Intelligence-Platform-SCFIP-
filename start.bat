@echo off
REM Quick Start Script for Smart Customer Feedback Intelligence Platform
REM This script helps you set up and run the project

echo ============================================================
echo Smart Customer Feedback Intelligence Platform (SCFIP)
echo Quick Start Script
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python is installed
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Virtual environment not found. Creating one...
    python -m venv venv
    echo [OK] Virtual environment created
    echo.
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
echo [INFO] Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies... This may take 5-10 minutes
    pip install -r requirements.txt
    echo [OK] Dependencies installed
    echo.
) else (
    echo [OK] Dependencies already installed
    echo.
)

REM Download NLTK data
echo [INFO] Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True); nltk.download('punkt_tab', quiet=True)"
echo [OK] NLTK data downloaded
echo.

REM Check if models are trained
if not exist "ml\models\sentiment_model.h5" (
    echo [INFO] Models not found. Training models...
    echo [INFO] This will take 5-10 minutes
    echo.
    python ml\train_models.py
    echo.
    echo [OK] Models trained successfully
    echo.
) else (
    echo [OK] Models already trained
    echo.
)

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next Steps:
echo.
echo 1. Start the FastAPI backend:
echo    python backend\main.py
echo.
echo 2. In a NEW terminal, start the Streamlit dashboard:
echo    streamlit run streamlit_app\dashboard.py
echo.
echo 3. Open your browser:
echo    - API Docs: http://localhost:8000/docs
echo    - Dashboard: http://localhost:8501
echo.
echo ============================================================
echo.

choice /C YN /M "Do you want to start the FastAPI backend now"
if errorlevel 2 goto end
if errorlevel 1 goto start_backend

:start_backend
echo.
echo [INFO] Starting FastAPI backend...
echo [INFO] After the backend starts, open a NEW terminal and run:
echo        streamlit run streamlit_app\dashboard.py
echo.
python backend\main.py

:end
echo.
echo Thank you for using SCFIP!
pause
