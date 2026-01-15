# Table of Contents Feature Guide

## Overview

The converter automatically generates a hierarchical table of contents (TOC) from your markdown headings, making it easy for readers to navigate your ebook.

## How It Works （）

### Automatic Detection

Every heading in your markdown file is automatically:
1. **Detected** - The converter finds all headings (H1 through H6)
2. **Indexed** - Each heading gets a unique ID for linking
3. **Structured** - Headings are organized in a hierarchy
4. **Linked** - TOC entries link directly to content

### Heading Levels

```markdown
# Level 1 - Main chapters
## Level 2 - Major sections
### Level 3 - Subsections
#### Level 4 - Sub-subsections
##### Level 5 - Deeper nesting
###### Level 6 - Deepest level
```

## Best Practices

### ✅ DO: Use Proper Hierarchy

```markdown
# Chapter 1
## Section 1.1
### Subsection 1.1.1
### Subsection 1.1.2
## Section 1.2
# Chapter 2
```

This creates a clean, navigable structure.

### ❌ DON'T: Skip Levels

```markdown
# Chapter 1
### Subsection (skipped H2!)
```

This can create a confusing TOC structure.

### ✅ DO: Use Descriptive Headings

```markdown
## Getting Started with Installation
### Windows Installation Steps
### macOS Installation Steps
```

Clear headings make navigation easier.

### ❌ DON'T: Use Generic Headings

```markdown
## Part 1
### Step 1
### Step 2
```

Generic headings don't help readers find what they need.

## Single File Conversion

When converting a single markdown file:

```markdown
# My Book Title

## Chapter 1: Introduction
### What You'll Learn
### Prerequisites

## Chapter 2: Getting Started
### Installation
#### Windows
#### macOS
#### Linux
### Configuration

## Chapter 3: Advanced Topics
```

**Result**: TOC shows all chapters, sections, and subsections with proper nesting.

## Multiple File Conversion

When converting multiple files:

**File 1: intro.md**
```markdown
# Introduction
## About This Book
## Who Should Read This
```

**File 2: tutorial.md**
```markdown
# Tutorial
## Lesson 1
### Exercise 1.1
### Exercise 1.2
## Lesson 2
```

**Result**: TOC shows:
- Introduction (chapter)
  - About This Book
  - Who Should Read This
- Tutorial (chapter)
  - Lesson 1
    - Exercise 1.1
    - Exercise 1.2
  - Lesson 2

## Viewing the TOC

### In EPUB Readers

Most EPUB readers show the TOC as:
- **Sidebar/Menu**: Click a menu icon to see all sections
- **Bookmarks**: Access via bookmarks/navigation panel
- **Contents Page**: Often appears as first page

### Popular Readers

- **Calibre**: View → Table of Contents (or press T)
- **Adobe Digital Editions**: Click bookmark icon
- **Apple Books**: Click contents icon (top left)
- **Google Play Books**: Tap screen → Contents
- **Amazon Kindle**: Go to → Table of Contents

## Testing Your TOC

1. **Convert your markdown file**
2. **Open the EPUB in a reader**
3. **Access the TOC/bookmarks**
4. **Click different entries** to test navigation
5. **Verify all sections appear** in proper hierarchy

## Troubleshooting

### Issue: TOC is flat (no nesting)

**Cause**: All headings are the same level
**Solution**: Use different heading levels (H2, H3, H4)

### Issue: Missing sections in TOC

**Cause**: Headings not formatted correctly
**Solution**: Ensure headings start with # at line beginning

### Issue: TOC entries have strange names

**Cause**: Heading text has special formatting
**Solution**: Keep heading text simple (the converter strips most formatting)

### Issue: Duplicate entries in TOC

**Cause**: Multiple headings with identical text
**Solution**: Make heading text unique (converter adds IDs to distinguish them)

## Example: Complete Book Structure

```markdown
# Book Title (H1 - usually just the title)

## Foreword (H2 - chapter)

## Part 1: Fundamentals (H2 - part/chapter)

### Chapter 1: Getting Started (H3 - section)
#### Installation (H4 - subsection)
#### Configuration (H4 - subsection)

### Chapter 2: Basic Concepts (H3 - section)
#### Concept A (H4 - subsection)
#### Concept B (H4 - subsection)

## Part 2: Advanced Topics (H2 - part/chapter)

### Chapter 3: Advanced Features (H3 - section)
#### Feature X (H4 - subsection)
##### Example 1 (H5 - sub-subsection)
##### Example 2 (H5 - sub-subsection)

## Appendix (H2 - chapter)

### Glossary (H3 - section)
### References (H3 - section)
```

## Quick Reference

| Markdown | HTML | TOC Level | Use For |
|----------|------|-----------|---------|
| `#` | H1 | Top | Book title |
| `##` | H2 | 1 | Chapters/Parts |
| `###` | H3 | 2 | Sections |
| `####` | H4 | 3 | Subsections |
| `#####` | H5 | 4 | Details |
| `######` | H6 | 5 | Fine details |

## Need Help?

Try converting the included example files:
- `sample.md` - Basic example
- `toc_demo.md` - Comprehensive TOC demonstration

Compare the TOC in your ebook reader with the markdown structure to understand how it works!
