@echo off
echo ========================================
echo   Face Recognition Mobile App
echo   Testing on Desktop
echo ========================================
echo.

cd /d "%~dp0"

echo Checking Python...
py --version
if errorlevel 1 (
    echo Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
py -m pip install kivy kivymd opencv-python numpy face-recognition pillow --quiet

echo.
echo ========================================
echo   Starting App...
echo ========================================
echo.
echo Close the app window to stop.
echo.

py test_app.py

pause
