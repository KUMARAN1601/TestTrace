@echo off
REM TestTrace Recorder - Build Script
REM Creates standalone executable

echo ========================================
echo TestTrace Recorder - Build Script
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found
    echo Please run INSTALL.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found, installing...
    pip install pyinstaller
)

echo [1/2] Building executable with PyInstaller...
echo This may take 1-2 minutes...
echo.

pyinstaller build.spec

if errorlevel 1 (
    echo.
    echo ERROR: Build failed
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo [2/2] Build completed successfully!
echo.
echo Executable location: dist\TestTrace.exe
echo File size: ~50-80 MB (single file)
echo.
echo You can now distribute TestTrace.exe to any Windows PC
echo No Python installation required on target machines
echo.

REM Open dist folder
if exist dist\TestTrace.exe (
    echo Opening dist folder...
    explorer dist
)

pause
