# Markdown to EPUB/MOBI Converter

A user-friendly Python GUI application to convert markdown files (single or multiple) into EPUB and MOBI ebook formats.

## Features

- **Easy-to-use GUI**: Simple and intuitive interface built with tkinter
- **Single or Multiple Files**: Convert one markdown file or combine multiple files into a single ebook
- **EPUB and MOBI Support**: Export to EPUB format directly, or convert to MOBI (requires Calibre)
- **Hierarchical Table of Contents**: Automatically generates a multi-level TOC from markdown headings (H1-H6)
  - Navigate easily through chapters and sections
  - Supports nested heading structures
  - Clickable bookmarks in ebook readers
- **Customizable Metadata**: Set book title, author, and output filename
- **Proper Formatting**: Preserves markdown formatting including:
  - Headings and text styles
  - Code blocks with syntax highlighting
  - Tables
  - Blockquotes
  - Images
  - Lists
- **Real-time Status**: View conversion progress and status messages
- **Error Handling**: Comprehensive error handling with helpful messages

## Requirements

- Python 3.7 or higher
- Calibre (optional, only for MOBI conversion)

## Installation

### Step 1: Install Python Dependencies

1. Open terminal/command prompt
2. Navigate to the project directory:
   ```bash
   cd md_to_ebook_converter
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Install Calibre (Optional - for MOBI conversion)

If you want to convert to MOBI format, you need to install Calibre:

- **Windows**: Download from https://calibre-ebook.com/download_windows
- **macOS**: Download from https://calibre-ebook.com/download_osx
- **Linux**:
  ```bash
  sudo apt-get install calibre  # Ubuntu/Debian
  sudo dnf install calibre      # Fedora
  ```

Make sure `ebook-convert` command is available in your system PATH.

## Usage

### Method 1: Run with Python

```bash
python gui.py
```

### Method 2: Run the launcher script

**Windows:**
```bash
python run.py
```

**Linux/macOS:**
```bash
python3 run.py
```

### Using the GUI

1. **Select Files**:
   - Click "Select Single File" to convert one markdown file
   - Click "Select Multiple Files" to combine multiple markdown files into one ebook
   - Selected files will appear in the display area

2. **Configure Output**:
   - Choose output format: `epub`, `mobi`, or `both`
   - Select output directory (default: Documents folder)
   - Enter output filename (without extension)

3. **Set Metadata**:
   - Enter book title (will be displayed in ebook readers)
   - Enter author name

4. **Convert**:
   - Click "Convert" button
   - Monitor progress in the status area
   - Success message will appear when complete

## File Structure

```
md_to_ebook_converter/
├── converter.py         # Core conversion logic
├── gui.py              # GUI application
├── run.py              # Application launcher
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── examples/          # Sample markdown files
    └── sample.md
```

## Markdown Support

The converter supports standard markdown syntax including:

- **Headings**: `# H1`, `## H2`, `### H3`, etc. (automatically added to table of contents)
- **Text Formatting**: `*italic*`, `**bold**`, `***bold italic***`
- **Lists**: Ordered and unordered lists
- **Links**: `[text](url)`
- **Images**: `![alt](image.jpg)`
- **Code**: Inline `` `code` `` and code blocks with ` ``` `
- **Tables**: GitHub-flavored markdown tables
- **Blockquotes**: `> quote`
- **Horizontal Rules**: `---` or `***`

### Table of Contents Generation

The converter automatically creates a hierarchical table of contents based on your markdown headings:

- **H1 (`#`)**: Top-level entries
- **H2 (`##`)**: Main sections
- **H3 (`###`)**: Subsections
- **H4-H6**: Deeper nesting levels

**Example:**
```markdown
# Book Title

## Chapter 1

### Section 1.1

#### Subsection 1.1.1

### Section 1.2

## Chapter 2

### Section 2.1
```

This creates a navigable TOC in your ebook reader where you can jump directly to any section!

## Troubleshooting

### MOBI Conversion Fails

**Error**: "Calibre not found"
- **Solution**: Install Calibre and ensure `ebook-convert` is in your system PATH
- **Workaround**: Convert to EPUB only (all modern ebook readers support EPUB)

### Import Errors

**Error**: "ModuleNotFoundError: No module named 'X'"
- **Solution**: Run `pip install -r requirements.txt` again
- Make sure you're using the correct Python version (3.7+)

### Permission Errors

**Error**: "Permission denied" when writing output file
- **Solution**: Choose a different output directory where you have write permissions
- Try using your Documents folder or Desktop

### File Encoding Issues

**Error**: "UnicodeDecodeError"
- **Solution**: Ensure your markdown files are saved in UTF-8 encoding
- Most modern text editors save in UTF-8 by default

## Examples

### Example 1: Single File Conversion

1. Select your markdown file (e.g., `chapter1.md`)
2. Set title: "My First Ebook"
3. Set author: "John Doe"
4. Choose format: "epub"
5. Click Convert

Result: `My First Ebook.epub` in your output directory

### Example 2: Multiple Files to Single Ebook

1. Select multiple files: `chapter1.md`, `chapter2.md`, `chapter3.md`
2. Set title: "Complete Guide"
3. Set author: "Jane Smith"
4. Choose format: "both"
5. Click Convert

Result:
- `Complete Guide.epub`
- `Complete Guide.mobi`

Each markdown file becomes a chapter in the ebook.

## Tips

- **Chapter Titles**: Start each markdown file with a `# Heading` for the chapter title
- **Table of Contents**: Use proper heading hierarchy (H1, H2, H3) for best TOC structure
  - Don't skip levels (e.g., don't go from H1 to H3 without H2)
  - Each heading automatically becomes a TOC entry
- **Images**: Use relative paths for images, or place images in the same directory
- **File Order**: When selecting multiple files, they appear in the order selected
- **Large Files**: The converter handles large files efficiently, but conversion may take time
- **Testing TOC**: Open the generated EPUB in an ebook reader and check the table of contents/bookmarks

## Technical Details

### Dependencies

- **markdown**: Markdown to HTML conversion with extensions
- **ebooklib**: EPUB file creation and manipulation
- **Pillow**: Image processing
- **beautifulsoup4**: HTML parsing and cleaning
- **lxml**: XML/HTML processing

### Conversion Process

1. **Read**: Parse markdown files and extract content
2. **Convert**: Transform markdown to HTML with styling
3. **Format**: Apply CSS for proper ebook formatting
4. **Package**: Create EPUB with proper structure and metadata
5. **Optional**: Convert EPUB to MOBI using Calibre

## License

This project is provided as-is for personal and educational use.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify all dependencies are installed correctly
3. Ensure input files are valid markdown format

## Version

Current Version: 1.1.0

## Changelog

### Version 1.1.0 (TOC Enhancement)
- **NEW**: Hierarchical table of contents from markdown headings
- **NEW**: Automatic bookmark generation for all heading levels (H1-H6)
- **NEW**: Nested TOC structure for easy navigation
- **IMPROVED**: Better heading ID generation for reliable linking
- **ADDED**: Enhanced sample file (`toc_demo.md`) demonstrating TOC features

### Version 1.0.0 (Initial Release)
- Single and multiple file conversion
- EPUB and MOBI format support
- GUI interface with file selection
- Customizable metadata
- Proper markdown formatting preservation
- Error handling and status logging
