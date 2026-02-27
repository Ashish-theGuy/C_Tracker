@echo off
echo ========================================
echo YOLOv8 Person Detection - Installation
echo ========================================
echo.

REM Try different Python commands
echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python
    goto install
)

py --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=py
    goto install
)

python3 --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python3
    goto install
)

echo ERROR: Python not found!
echo Please install Python from https://www.python.org/downloads/
pause
exit /b 1

:install
echo Found Python: %PYTHON_CMD%
echo.
echo Installing dependencies...
%PYTHON_CMD% -m pip install -r requirements.txt

if %errorlevel% == 0 (
    echo.
    echo ========================================
    echo Installation successful!
    echo ========================================
    echo.
    echo Testing setup...
    %PYTHON_CMD% test_setup.py
    echo.
    echo ========================================
    echo Next steps:
    echo 1. Place an image file in this folder
    echo 2. Run: %PYTHON_CMD% person_detector.py --input your_image.jpg --output result.jpg
    echo ========================================
) else (
    echo.
    echo ERROR: Installation failed!
    echo Try: %PYTHON_CMD% -m pip install --upgrade pip
    echo Then run this script again
)

pause

