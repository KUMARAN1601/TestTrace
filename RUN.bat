@echo off
REM TestTrace Recorder - Quick Run Script
REM Double-click this file to run the application

echo Starting TestTrace Recorder...
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found
    echo Please run INSTALL.bat first to set up the environment
    pause
    exit /b 1
)

REM Activate virtual environment and run
call venv\Scripts\activate.bat
python main.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo Check the error messages above
    pause
)
