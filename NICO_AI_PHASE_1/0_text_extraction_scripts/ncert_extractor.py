"""
NCERT Parallel Content Extractor
==================================

A production-ready script for extracting parallel content from English and Hindi 
NCERT textbook PDFs (Classes 10, 11, 12) with robust table handling and Indic 
language normalization.

Installation Instructions:
--------------------------
Install the required Python libraries using pip:

    pip install PyMuPDF pdfplumber indic-nlp-library typing

Required Libraries:
- PyMuPDF (fitz): Fast, reliable text extraction and structural analysis
- pdfplumber: Robust table detection and extraction
- indic-nlp-library: Script-specific normalization for Hindi (Devanagari)
- typing: Type hinting support

Author: NICO AI
Date: 2025-11-29
"""

import fitz  # PyMuPDF
import pdfplumber
import re
from typing import List, Tuple
from pathlib import Path

# Indic NLP imports
try:
    from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
    from indicnlp.tokenize import indic_tokenize
    INDIC_NLP_AVAILABLE = True
except ImportError:
    INDIC_NLP_AVAILABLE = False
    print("Warning: indic-nlp-library not available. Hindi normalization will be limited.")


def general_cleaner(text: str) -> str:
    """
    Clean and normalize general text extracted from PDFs.
    
    This function performs:
    - Hyphenation removal (re-joining broken words)
    - Boilerplate removal (page numbers, headers/footers)
    - Whitespace cleanup
    
    Args:
        text: Raw text extracted from PDF
        
    Returns:
        Cleaned and normalized text
    """
    if not text:
        return ""
    
    # Remove soft hyphens and line-ending hyphens
    # Pattern: word- \n word becomes wordword
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    
    # Remove common PDF artifacts and boilerplate
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines (will be consolidated later)
        if not line:
            continue
            
        # Skip lines that are only page numbers
        if re.match(r'^\d+$', line):
            continue
            
        # Skip common NCERT headers/footers patterns
        if re.match(r'^(Chapter|CHAPTER)\s+\d+', line):
            continue
        if re.match(r'^(Science|SCIENCE|Mathematics|MATHEMATICS|Biology|BIOLOGY)', line) and len(line) < 30:
            continue
            
        cleaned_lines.append(line)
    
    # Join lines and consolidate whitespace
    text = '\n'.join(cleaned_lines)
    
    # Consolidate multiple newlines into double newlines (paragraph breaks)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Consolidate multiple spaces
    text = re.sub(r' {2,}', ' ', text)
    
    return text.strip()


def indic_normalize(text: str, lang: str) -> str:
    """
    Normalize Indic language text (specifically Hindi/Devanagari).
    
    This function performs:
    - ZWJ/ZWNJ removal
    - Nukta canonicalization
    - Pipe character replacement with Hindi poorna virama
    
    Args:
        text: Text to normalize
        lang: Language code ('hi' for Hindi)
        
    Returns:
        Normalized text
    """
    if lang != 'hi' or not text:
        return text
    
    # Replace pipe character with Hindi poorna virama (।)
    text = text.replace('|', '।')
    
    if INDIC_NLP_AVAILABLE:
        try:
            # Initialize the normalizer factory for Hindi
            factory = IndicNormalizerFactory()
            normalizer = factory.get_normalizer(lang)
            
            # Perform normalization
            # This handles ZWJ/ZWNJ removal and Nukta canonicalization
            text = normalizer.normalize(text)
            
        except Exception as e:
            print(f"Warning: Indic normalization failed: {e}")
            # Fall back to basic normalization
            pass
    
    # Manual fallback for basic normalization if library not available
    # Remove Zero Width Joiner (U+200D) and Zero Width Non-Joiner (U+200C)
    text = text.replace('\u200D', '')  # ZWJ
    text = text.replace('\u200C', '')  # ZWNJ
    
    return text


def extract_tables_from_page(page) -> List[Tuple[str, int]]:
    """
    Extract tables from a pdfplumber page and convert to Markdown format.
    
    Args:
        page: pdfplumber page object
        
    Returns:
        List of tuples (markdown_table, approximate_y_position)
    """
    tables_data = []
    
    try:
        tables = page.find_tables()
        
        for table in tables:
            # Extract table data
            table_data = table.extract()
            
            if not table_data:
                continue
            
            # Convert to Markdown format
            markdown_lines = []
            markdown_lines.append("[TABLE START]")
            
            # Add header row
            if len(table_data) > 0:
                header = table_data[0]
                # Clean None values
                header = [str(cell).strip() if cell else "" for cell in header]
                markdown_lines.append("| " + " | ".join(header) + " |")
                
                # Add separator
                markdown_lines.append("| " + " | ".join(["---"] * len(header)) + " |")
                
                # Add data rows
                for row in table_data[1:]:
                    row = [str(cell).strip() if cell else "" for cell in row]
                    markdown_lines.append("| " + " | ".join(row) + " |")
            
            markdown_lines.append("[TABLE END]")
            
            markdown_table = "\n".join(markdown_lines)
            
            # Get approximate Y position for ordering
            y_position = table.bbox[1] if hasattr(table, 'bbox') else 0
            
            tables_data.append((markdown_table, y_position))
            
    except Exception as e:
        print(f"Warning: Table extraction failed: {e}")
    
    return tables_data


def extract_ncert_content(pdf_path: str, lang: str, output_path: str) -> None:
    """
    Extract content from NCERT PDF with table handling and text normalization.
    
    This is the main extraction function that:
    1. Detects and extracts tables using pdfplumber
    2. Extracts general text using PyMuPDF
    3. Integrates tables into the reading flow
    4. Applies cleaning and normalization
    
    Args:
        pdf_path: Path to the input PDF file
        lang: Language code ('en' for English, 'hi' for Hindi)
        output_path: Path to the output text file
    """
    print(f"Processing: {pdf_path}")
    print(f"Language: {lang}")
    print(f"Output: {output_path}")
    
    all_content = []
    
    try:
        # Open PDF with both libraries
        pdf_fitz = fitz.open(pdf_path)
        pdf_plumber = pdfplumber.open(pdf_path)
        
        total_pages = len(pdf_fitz)
        print(f"Total pages: {total_pages}")
        
        for page_num in range(total_pages):
            print(f"Processing page {page_num + 1}/{total_pages}...", end='\r')
            
            # Get pages from both libraries
            fitz_page = pdf_fitz[page_num]
            plumber_page = pdf_plumber.pages[page_num]
            
            # Extract tables with positions
            tables = extract_tables_from_page(plumber_page)
            
            # Extract text using PyMuPDF (preserves reading order better)
            text = fitz_page.get_text("text")
            
            # If tables were found, we need to integrate them
            if tables:
                # For simplicity, append tables at the end of page content
                # A more sophisticated approach would use coordinates to insert them
                page_content = text
                for table_md, _ in tables:
                    page_content += "\n\n" + table_md + "\n\n"
            else:
                page_content = text
            
            # Apply general cleaning
            page_content = general_cleaner(page_content)
            
            # Apply Indic normalization if Hindi
            if lang == 'hi':
                page_content = indic_normalize(page_content, lang)
            
            if page_content:
                all_content.append(page_content)
        
        # Close PDFs
        pdf_fitz.close()
        pdf_plumber.close()
        
        print(f"\nExtraction complete. Writing to {output_path}...")
        
        # Write output with one paragraph per line
        with open(output_path, 'w', encoding='utf-8') as f:
            for page_content in all_content:
                # Split by paragraph breaks
                paragraphs = page_content.split('\n\n')
                for para in paragraphs:
                    para = para.strip()
                    if para:
                        # Replace internal newlines with spaces (except for tables)
                        if '[TABLE START]' not in para:
                            para = para.replace('\n', ' ')
                        f.write(para + '\n')
        
        print(f"✓ Successfully extracted content to {output_path}")
        
    except Exception as e:
        print(f"\n✗ Error processing {pdf_path}: {e}")
        raise


if __name__ == "__main__":
    """
    Demonstration block for Class 10 NCERT Science textbooks.
    
    Update the PDF paths to match your actual file locations.
    """
    
    # Define base directory (update this to your actual directory)
    base_dir = Path(__file__).parent
    
    # Class 10 Science - English
    english_pdf = base_dir / "NCERT_Class10_Science_EN.pdf"
    english_output = base_dir / "NCERT_Class10_Science_EN.txt"
    
    # Class 10 Science - Hindi
    hindi_pdf = base_dir / "NCERT_Class10_Science_HI.pdf"
    hindi_output = base_dir / "NCERT_Class10_Science_HI.txt"
    
    # Process English PDF
    if english_pdf.exists():
        extract_ncert_content(
            pdf_path=str(english_pdf),
            lang='en',
            output_path=str(english_output)
        )
    else:
        print(f"Warning: English PDF not found at {english_pdf}")
    
    print("\n" + "="*60 + "\n")
    
    # Process Hindi PDF
    if hindi_pdf.exists():
        extract_ncert_content(
            pdf_path=str(hindi_pdf),
            lang='hi',
            output_path=str(hindi_output)
        )
    else:
        print(f"Warning: Hindi PDF not found at {hindi_pdf}")
    
    print("\n" + "="*60)
    print("Extraction complete!")
    print("Output files are ready for sentence alignment.")
    print("="*60)
