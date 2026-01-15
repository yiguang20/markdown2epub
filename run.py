"""
Main launcher script for the Markdown to EPUB/MOBI Converter
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    try:
        from gui import main
        main()
    except ImportError as e:
        print(f"Error: Missing dependencies - {e}")
        print("\nPlease install required packages:")
        print("  pip install -r requirements.txt")
        input("\nPress Enter to exit...")
    except Exception as e:
        print(f"Error starting application: {e}")
        input("\nPress Enter to exit...")
