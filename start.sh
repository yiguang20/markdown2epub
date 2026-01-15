#!/bin/bash
# Linux/macOS launcher for Markdown to EPUB/MOBI Converter

echo "========================================"
echo "Markdown to EPUB/MOBI Converter"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Check if dependencies are installed
echo "Checking dependencies..."
python3 -c "import markdown, ebooklib" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "Installing required dependencies..."
    echo ""
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: Failed to install dependencies"
        echo "Please run: pip3 install -r requirements.txt"
        exit 1
    fi
fi

echo ""
echo "Starting application..."
echo ""
python3 run.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Application closed with errors"
    read -p "Press Enter to exit..."
fi
