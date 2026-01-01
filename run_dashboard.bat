@echo off
REM Start Streamlit Dashboard
echo ============================================================
echo Starting Streamlit Dashboard
echo ============================================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo [INFO] Starting Streamlit dashboard...
echo [INFO] Dashboard will be available at: http://localhost:8501
echo [INFO] Press Ctrl+C to stop the dashboard
echo.
echo [IMPORTANT] Make sure the FastAPI backend is running!
echo [IMPORTANT] Run 'run_backend.bat' in another terminal if not started
echo.
echo ============================================================
echo.

streamlit run streamlit_app\dashboard.py

pause
