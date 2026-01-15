# Quick Start Guide

## Getting Started in 3 Steps

### Step 1: Install Dependencies

Open terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 2: Launch the Application

**Windows:**
- Double-click `start.bat`, OR
- Run: `python run.py`

**Linux/macOS:**
- Run: `chmod +x start.sh && ./start.sh`, OR
- Run: `python3 run.py`

### Step 3: Convert Your First Ebook

1. Click "Select Single File" or "Select Multiple Files"
2. Browse to your markdown file(s)
3. Set book title and author
4. Choose output format (epub, mobi, or both)
5. Click "Convert"
6. Done! Your ebook is ready

## First Time Setup

### Windows Users

1. **Install Python** (if not already installed):
   - Download from https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Restart your computer after installation

2. **Install Dependencies**:
   - Open Command Prompt in the project folder
   - Run: `pip install -r requirements.txt`

3. **For MOBI Support** (optional):
   - Download Calibre from https://calibre-ebook.com/download_windows
   - Install with default settings
   - Restart your computer

### macOS Users

1. **Install Python** (if not already installed):
   - Python 3 is usually pre-installed
   - If not, download from https://www.python.org/downloads/

2. **Install Dependencies**:
   - Open Terminal in the project folder
   - Run: `pip3 install -r requirements.txt`

3. **For MOBI Support** (optional):
   - Download Calibre from https://calibre-ebook.com/download_osx
   - Install by dragging to Applications folder

### Linux Users

1. **Install Python** (usually pre-installed):
   ```bash
   sudo apt-get install python3 python3-pip  # Ubuntu/Debian
   ```

2. **Install Dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **For MOBI Support** (optional):
   ```bash
   sudo apt-get install calibre  # Ubuntu/Debian
   ```

## Test the Converter

Try converting the included sample file:

1. Launch the application
2. Click "Select Single File"
3. Navigate to `examples/sample.md`
4. Click "Convert"
5. Check your output directory for the generated ebook

## Common Issues

### "Module not found" error
Run: `pip install -r requirements.txt`

### "Calibre not found" (for MOBI)
- Install Calibre from https://calibre-ebook.com
- Or convert to EPUB only (works without Calibre)

### Python not recognized
- Reinstall Python and check "Add to PATH"
- Restart your computer

## Need Help?

See the full README.md for:
- Detailed usage instructions
- Troubleshooting guide
- Feature documentation
- Advanced options
