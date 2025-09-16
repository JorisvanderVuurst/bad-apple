@echo off
title Bad Apple ASCII Player
color 0F

echo Bad Apple ASCII Player
echo ======================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Install from python.org
    pause
    exit /b 1
)

python -c "import cv2, numpy" >nul 2>&1
if errorlevel 1 (
    echo Installing packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install packages
        pause
        exit /b 1
    )
)

python bad_apple.py

pause
