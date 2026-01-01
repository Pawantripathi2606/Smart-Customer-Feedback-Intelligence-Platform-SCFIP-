@echo off
REM Start FastAPI Backend
echo ============================================================
echo Starting FastAPI Backend Server
echo ============================================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Check if models exist
if not exist "ml\models\sentiment_model.h5" (
    echo [WARNING] Models not found!
    echo [INFO] Please run: python ml\train_models.py
    echo.
    choice /C YN /M "Do you want to train models now (takes 5-10 minutes)"
    if errorlevel 2 goto skip_training
    if errorlevel 1 goto train_models
)

goto start_server

:train_models
echo.
echo [INFO] Training models...
python ml\train_models.py
echo.

:start_server
echo [INFO] Starting FastAPI server...
echo [INFO] API will be available at: http://localhost:8000
echo [INFO] API Documentation: http://localhost:8000/docs
echo [INFO] Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

python backend\main.py

goto end

:skip_training
echo.
echo [INFO] Skipping model training
echo [WARNING] API may not work without trained models
echo.
goto start_server

:end
pause
