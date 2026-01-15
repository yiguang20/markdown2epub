"""
Markdown to EPUB/MOBI converter module
Handles the actual conversion logic
"""
import os
import markdown
from ebooklib import epub
from datetime import datetime
from pathlib import Path
import re
from typing import List, Tuple, Dict
from bs4 import BeautifulSoup
import hashlib


class MarkdownConverter:
    """Convert markdown files to EPUB format"""

    def __init__(self):
        self.md = markdown.Markdown(extensions=[
            'extra',
            'codehilite',
            'toc',
            'tables',
            'fenced_code'
        ])
        self.heading_counter = 0

    def read_markdown_file(self, filepath: str) -> Tuple[str, str]:
        """Read markdown file and extract title"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Try to extract title from first heading
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title = Path(filepath).stem

        return content, title

    def markdown_to_html(self, md_content: str) -> str:
        """Convert markdown content to HTML"""
        return self.md.convert(md_content)

    def extract_headings(self, md_content: str) -> List[Dict]:
        """
        Extract headings from markdown content with their levels
        Returns list of dicts: [{'level': 1, 'text': 'Title', 'id': 'title'}, ...]
        """
        headings = []
        lines = md_content.split('\n')

        for line in lines:
            # Match ATX-style headings (# Heading)
            match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                # Remove markdown formatting from heading text
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
                text = re.sub(r'\*(.+?)\*', r'\1', text)  # Italic
                text = re.sub(r'`(.+?)`', r'\1', text)  # Code
                text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # Links

                # Generate a unique ID for this heading
                heading_id = self.generate_heading_id(text)

                headings.append({
                    'level': level,
                    'text': text,
                    'id': heading_id
                })

        return headings

    def generate_heading_id(self, text: str) -> str:
        """Generate a unique ID for a heading"""
        # Create a URL-friendly ID from text
        heading_id = re.sub(r'[^\w\s-]', '', text.lower())
        heading_id = re.sub(r'[-\s]+', '-', heading_id).strip('-')

        # Add counter to ensure uniqueness
        self.heading_counter += 1
        heading_id = f"{heading_id}-{self.heading_counter}"

        return heading_id

    def add_ids_to_html_headings(self, html_content: str, headings: List[Dict]) -> str:
        """Add ID attributes to HTML headings for navigation"""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all heading tags
        all_headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        # Match headings with their IDs
        heading_idx = 0
        for tag in all_headings:
            if heading_idx < len(headings):
                # Add ID attribute
                tag['id'] = headings[heading_idx]['id']
                heading_idx += 1

        return str(soup)

    def build_nested_toc(self, headings: List[Dict], chapter: epub.EpubHtml) -> List:
        """
        Build a nested table of contents structure from headings
        Returns a nested list/tuple structure suitable for epub.toc
        """
        if not headings:
            return [chapter]

        toc_structure = []
        stack = [(0, toc_structure)]  # (level, current_list)

        for heading in headings:
            level = heading['level']

            # Create link object
            link = epub.Link(
                f"{chapter.file_name}#{heading['id']}",
                heading['text'],
                heading['id']
            )

            # Find the appropriate parent level
            while stack and stack[-1][0] >= level:
                stack.pop()

            if not stack:
                stack = [(0, toc_structure)]

            current_list = stack[-1][1]

            # If this is a potential parent (has lower level number), prepare for children
            if level < 6:  # Can have sub-headings
                children = []
                current_list.append((link, children))
                stack.append((level, children))
            else:
                current_list.append(link)

        return toc_structure

    def create_epub_chapter(self, title: str, content: str, filename: str,
                          headings: List[Dict] = None) -> epub.EpubHtml:
        """Create an EPUB chapter from HTML content with proper heading IDs"""
        chapter = epub.EpubHtml(
            title=title,
            file_name=filename,
            lang='en'
        )

        # Add IDs to headings if provided
        if headings:
            content = self.add_ids_to_html_headings(content, headings)

        # Add CSS styling
        css = """
        body {
            font-family: Georgia, serif;
            line-height: 1.6;
            margin: 2em;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: Arial, sans-serif;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            color: #333;
        }
        h1 { font-size: 2em; }
        h2 { font-size: 1.5em; }
        h3 { font-size: 1.3em; }
        code {
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background-color: #f4f4f4;
            padding: 1em;
            border-radius: 5px;
            overflow-x: auto;
        }
        pre code {
            background-color: transparent;
            padding: 0;
        }
        blockquote {
            border-left: 4px solid #ddd;
            padding-left: 1em;
            color: #666;
            margin: 1em 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f4f4f4;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        """

        chapter.content = f"""
        <html>
        <head>
            <title>{title}</title>
            <style>{css}</style>
        </head>
        <body>
            {content}
        </body>
        </html>
        """

        return chapter

    def convert_single_file(self, input_file: str, output_file: str,
                          book_title: str = None, author: str = "Unknown") -> bool:
        """Convert a single markdown file to EPUB with hierarchical TOC"""
        try:
            # Reset heading counter for new conversion
            self.heading_counter = 0

            # Read markdown file
            md_content, extracted_title = self.read_markdown_file(input_file)

            # Use provided title or extracted title
            title = book_title if book_title else extracted_title

            # Extract headings for TOC
            headings = self.extract_headings(md_content)

            # Convert to HTML
            html_content = self.markdown_to_html(md_content)

            # Create EPUB book
            book = epub.EpubBook()

            # Set metadata
            book.set_identifier(f'md2epub_{datetime.now().timestamp()}')
            book.set_title(title)
            book.set_language('en')
            book.add_author(author)

            # Create chapter with heading IDs
            chapter = self.create_epub_chapter(title, html_content, 'chapter_1.xhtml', headings)
            book.add_item(chapter)

            # Build nested TOC from headings
            if headings:
                toc_structure = self.build_nested_toc(headings, chapter)
                book.toc = toc_structure
            else:
                book.toc = (chapter,)

            # Add navigation
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())

            # Define spine
            book.spine = ['nav', chapter]

            # Write EPUB file
            epub.write_epub(output_file, book)

            return True

        except Exception as e:
            raise Exception(f"Error converting file: {str(e)}")

    def convert_multiple_files(self, input_files: List[str], output_file: str,
                              book_title: str = "Compiled Book", author: str = "Unknown") -> bool:
        """Convert multiple markdown files into a single EPUB with hierarchical TOC"""
        try:
            # Reset heading counter for new conversion
            self.heading_counter = 0

            # Create EPUB book
            book = epub.EpubBook()

            # Set metadata
            book.set_identifier(f'md2epub_{datetime.now().timestamp()}')
            book.set_title(book_title)
            book.set_language('en')
            book.add_author(author)

            chapters = []
            toc = []

            # Process each markdown file
            for idx, input_file in enumerate(input_files, 1):
                md_content, chapter_title = self.read_markdown_file(input_file)

                # Extract headings for this chapter
                headings = self.extract_headings(md_content)

                # Convert to HTML
                html_content = self.markdown_to_html(md_content)

                # Create chapter with heading IDs
                chapter = self.create_epub_chapter(
                    chapter_title,
                    html_content,
                    f'chapter_{idx}.xhtml',
                    headings
                )

                book.add_item(chapter)
                chapters.append(chapter)

                # Build TOC for this chapter
                if headings:
                    # Create a section with chapter title and nested headings
                    chapter_toc = self.build_nested_toc(headings, chapter)
                    # Add chapter as main entry with its sub-headings
                    toc.append((
                        epub.Section(chapter_title),
                        chapter_toc
                    ))
                else:
                    # Just add the chapter as a simple entry
                    toc.append(chapter)

            # Add navigation
            book.toc = tuple(toc)
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())

            # Define spine
            book.spine = ['nav'] + chapters

            # Write EPUB file
            epub.write_epub(output_file, book)

            return True

        except Exception as e:
            raise Exception(f"Error converting files: {str(e)}")

    def convert_to_mobi(self, epub_file: str, mobi_file: str) -> Tuple[bool, str]:
        """
        Convert EPUB to MOBI using Calibre's ebook-convert
        Returns (success, message)
        """
        import subprocess
        import shutil

        # Check if ebook-convert is available
        if not shutil.which('ebook-convert'):
            return False, "Calibre not found. Please install Calibre from https://calibre-ebook.com/"

        try:
            # Run ebook-convert command
            result = subprocess.run(
                ['ebook-convert', epub_file, mobi_file],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                return True, "MOBI conversion successful"
            else:
                return False, f"MOBI conversion failed: {result.stderr}"

        except subprocess.TimeoutExpired:
            return False, "MOBI conversion timed out"
        except Exception as e:
            return False, f"MOBI conversion error: {str(e)}"
