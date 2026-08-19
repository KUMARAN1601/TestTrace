@echo off
REM TestTrace Recorder - Installation Script for Windows
REM Run this script to set up the development environment

echo ========================================
echo TestTrace Recorder - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Python found:
python --version
echo.

REM Create virtual environment
echo [2/4] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping creation
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)
echo.

REM Activate virtual environment and install dependencies
echo [3/4] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Create required directories
echo [4/4] Creating required directories...
if not exist output mkdir output
if not exist temp_sessions mkdir temp_sessions
if not exist assets mkdir assets
if not exist config mkdir config
echo Directories created successfully
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To run the application:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run: python main.py
echo.
echo To build executable:
echo   pyinstaller build.spec
echo.
pause
