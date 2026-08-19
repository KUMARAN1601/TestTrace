@echo off
echo ============================================================
echo TestTrace Recorder - Control Panel Visibility Test
echo ============================================================
echo.
echo This script will launch the application with visibility
echo monitoring enabled.
echo.
echo What to expect:
echo   - Control panel appears in top-right corner
echo   - Visibility status logged every 2 seconds
echo   - Timer should run continuously when recording
echo   - Control panel should NEVER disappear
echo.
echo ============================================================
echo.
pause
echo.
echo Starting visibility test...
echo.
python test_control_panel_visibility.py
echo.
echo.
pause
