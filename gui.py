"""
GUI application for Markdown to EPUB/MOBI converter
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from pathlib import Path
import threading
from converter import MarkdownConverter


class ConverterGUI:
    """Main GUI application for markdown conversion"""

    def __init__(self, root):
        self.root = root
        self.root.title("Markdown to EPUB/MOBI Converter")
        self.root.geometry("800x700")
        self.root.resizable(True, True)

        self.converter = MarkdownConverter()
        self.selected_files = []

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface"""

        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Markdown to EPUB/MOBI Converter",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 20))

        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Select Files", padding="10")
        file_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        file_frame.columnconfigure(1, weight=1)

        # File selection buttons
        ttk.Button(
            file_frame,
            text="Select Single File",
            command=self.select_single_file
        ).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        ttk.Button(
            file_frame,
            text="Select Multiple Files",
            command=self.select_multiple_files
        ).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        ttk.Button(
            file_frame,
            text="Clear Selection",
            command=self.clear_selection
        ).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        # Selected files display
        self.files_text = scrolledtext.ScrolledText(
            file_frame,
            height=6,
            width=60,
            wrap=tk.WORD,
            state='disabled'
        )
        self.files_text.grid(row=0, column=1, rowspan=3, padx=5, pady=5, sticky=(tk.W, tk.E))

        # Output settings section
        output_frame = ttk.LabelFrame(main_frame, text="Output Settings", padding="10")
        output_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(1, weight=1)

        # Output format
        ttk.Label(output_frame, text="Output Format:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.format_var = tk.StringVar(value="epub")
        format_combo = ttk.Combobox(
            output_frame,
            textvariable=self.format_var,
            values=["epub", "mobi", "both"],
            state='readonly',
            width=15
        )
        format_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Output directory
        ttk.Label(output_frame, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.output_dir_var = tk.StringVar(value=str(Path.home() / "Documents"))

        ttk.Entry(
            output_frame,
            textvariable=self.output_dir_var,
            width=40
        ).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Button(
            output_frame,
            text="Browse",
            command=self.select_output_directory
        ).grid(row=1, column=2, padx=5, pady=5)

        # Output filename
        ttk.Label(output_frame, text="Output Filename:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.output_filename_var = tk.StringVar(value="output")
        ttk.Entry(
            output_frame,
            textvariable=self.output_filename_var,
            width=40
        ).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Metadata section
        metadata_frame = ttk.LabelFrame(main_frame, text="Book Metadata", padding="10")
        metadata_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        metadata_frame.columnconfigure(1, weight=1)

        # Book title
        ttk.Label(metadata_frame, text="Book Title:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.title_var = tk.StringVar(value="My Book")
        ttk.Entry(
            metadata_frame,
            textvariable=self.title_var,
            width=40
        ).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Author
        ttk.Label(metadata_frame, text="Author:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.author_var = tk.StringVar(value="Unknown")
        ttk.Entry(
            metadata_frame,
            textvariable=self.author_var,
            width=40
        ).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Convert button
        self.convert_button = ttk.Button(
            main_frame,
            text="Convert",
            command=self.start_conversion,
            style='Accent.TButton'
        )
        self.convert_button.grid(row=4, column=0, pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.grid(row=5, column=0, pady=5)

        # Status/Log section
        log_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        log_frame.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        log_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            width=60,
            wrap=tk.WORD,
            state='disabled'
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure text tags for colored output
        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("success", foreground="green")
        self.log_text.tag_config("info", foreground="blue")

    def log_message(self, message, tag="info"):
        """Add a message to the log"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def select_single_file(self):
        """Select a single markdown file"""
        filename = filedialog.askopenfilename(
            title="Select Markdown File",
            filetypes=[("Markdown files", "*.md *.markdown"), ("All files", "*.*")]
        )

        if filename:
            self.selected_files = [filename]
            self.update_files_display()
            self.log_message(f"Selected: {filename}", "info")

    def select_multiple_files(self):
        """Select multiple markdown files"""
        filenames = filedialog.askopenfilenames(
            title="Select Markdown Files",
            filetypes=[("Markdown files", "*.md *.markdown"), ("All files", "*.*")]
        )

        if filenames:
            self.selected_files = list(filenames)
            self.update_files_display()
            self.log_message(f"Selected {len(filenames)} files", "info")

    def clear_selection(self):
        """Clear selected files"""
        self.selected_files = []
        self.update_files_display()
        self.log_message("Selection cleared", "info")

    def update_files_display(self):
        """Update the files display text area"""
        self.files_text.config(state='normal')
        self.files_text.delete(1.0, tk.END)

        if self.selected_files:
            for idx, file in enumerate(self.selected_files, 1):
                self.files_text.insert(tk.END, f"{idx}. {Path(file).name}\n")
        else:
            self.files_text.insert(tk.END, "No files selected")

        self.files_text.config(state='disabled')

    def select_output_directory(self):
        """Select output directory"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir_var.set(directory)
            self.log_message(f"Output directory: {directory}", "info")

    def validate_inputs(self):
        """Validate user inputs before conversion"""
        if not self.selected_files:
            messagebox.showerror("Error", "Please select at least one markdown file")
            return False

        if not self.output_filename_var.get().strip():
            messagebox.showerror("Error", "Please enter an output filename")
            return False

        if not os.path.exists(self.output_dir_var.get()):
            messagebox.showerror("Error", "Output directory does not exist")
            return False

        return True

    def start_conversion(self):
        """Start the conversion process in a separate thread"""
        if not self.validate_inputs():
            return

        # Disable convert button during conversion
        self.convert_button.config(state='disabled')
        self.progress.start()

        # Run conversion in separate thread to keep GUI responsive
        thread = threading.Thread(target=self.perform_conversion, daemon=True)
        thread.start()

    def perform_conversion(self):
        """Perform the actual conversion"""
        try:
            output_format = self.format_var.get()
            output_dir = self.output_dir_var.get()
            output_filename = self.output_filename_var.get().strip()
            book_title = self.title_var.get().strip()
            author = self.author_var.get().strip()

            # Create output paths
            epub_path = os.path.join(output_dir, f"{output_filename}.epub")
            mobi_path = os.path.join(output_dir, f"{output_filename}.mobi")

            self.log_message("Starting conversion...", "info")

            # Convert to EPUB
            if len(self.selected_files) == 1:
                self.log_message("Converting single file to EPUB...", "info")
                self.converter.convert_single_file(
                    self.selected_files[0],
                    epub_path,
                    book_title,
                    author
                )
            else:
                self.log_message(f"Converting {len(self.selected_files)} files to EPUB...", "info")
                self.converter.convert_multiple_files(
                    self.selected_files,
                    epub_path,
                    book_title,
                    author
                )

            self.log_message(f"EPUB created: {epub_path}", "success")

            # Convert to MOBI if requested
            if output_format in ["mobi", "both"]:
                self.log_message("Converting EPUB to MOBI...", "info")
                success, message = self.converter.convert_to_mobi(epub_path, mobi_path)

                if success:
                    self.log_message(f"MOBI created: {mobi_path}", "success")
                else:
                    self.log_message(f"MOBI conversion warning: {message}", "error")

                # If only MOBI was requested and conversion succeeded, remove EPUB
                if output_format == "mobi" and success:
                    os.remove(epub_path)
                    self.log_message("Temporary EPUB file removed", "info")

            # Show completion message
            self.root.after(0, lambda: messagebox.showinfo(
                "Success",
                "Conversion completed successfully!"
            ))

        except Exception as e:
            error_msg = f"Conversion failed: {str(e)}"
            self.log_message(error_msg, "error")
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))

        finally:
            # Re-enable convert button and stop progress bar
            self.root.after(0, lambda: self.convert_button.config(state='normal'))
            self.root.after(0, self.progress.stop)


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = ConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
