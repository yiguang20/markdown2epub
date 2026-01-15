@echo off
REM Windows launcher for Markdown to EPUB/MOBI Converter

echo ========================================
echo Markdown to EPUB/MOBI Converter
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://www.python.org
    echo.
    pause
    exit /b 1
)

echo Checking dependencies...
python -c "import markdown, ebooklib" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing required dependencies...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        echo Please run: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Starting application...
echo.
python run.py

if errorlevel 1 (
    echo.
    echo Application closed with errors
    pause
)
