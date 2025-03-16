@echo off
title Fiji News Intelligence Agent
echo Starting Fiji News Intelligence Agent...
echo.

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8 or higher.
    echo Visit https://www.python.org/downloads/ to download Python.
    pause
    exit /b 1
)

REM Check if virtual environment exists, if not create it
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Failed to create virtual environment. Please install virtualenv using: pip install virtualenv
        pause
        exit /b 1
    )
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment...
call venv\Scripts\activate

REM Check if requirements are installed
if not exist "venv\Lib\site-packages\flask" (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo Failed to install dependencies. Please check your internet connection and try again.
        pause
        exit /b 1
    )
)

REM Create data directory if it doesn't exist
if not exist "data" (
    echo Creating data directory...
    mkdir data
)

REM Create img directory for flag if it doesn't exist
if not exist "static\img\fiji_flag.png" (
    echo Note: You may want to download the Fiji flag image and place it in static\img\fiji_flag.png
)

REM Run the application
echo.
echo Starting Fiji News Intelligence Agent...
echo Access the application at http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

REM Deactivate virtual environment when done
call venv\Scripts\deactivate
echo Fiji News Intelligence Agent stopped.
pause 