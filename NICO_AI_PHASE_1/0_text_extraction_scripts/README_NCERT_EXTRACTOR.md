# NCERT Extractor - Documentation

## Overview

`ncert_extractor.py` is a production-ready Python script for extracting parallel content from English and Hindi NCERT textbook PDFs (Classes 10, 11, 12). The script prioritizes preserving reading order, handles tables gracefully, and performs essential text normalization for Indic languages.

## Features

✅ **Robust Table Extraction**: Uses `pdfplumber` for accurate table detection and converts tables to Markdown format  
✅ **Reading Order Preservation**: Uses `PyMuPDF` for fast, reliable text extraction that maintains document flow  
✅ **Indic Language Support**: Specialized normalization for Hindi (Devanagari) using `indic-nlp-library`  
✅ **Intelligent Cleaning**: Removes hyphenation, boilerplate, and PDF artifacts  
✅ **Production-Ready**: Comprehensive error handling and progress reporting  

## Installation

### Prerequisites

Python 3.7 or higher is required.

### Install Required Libraries

```bash
pip install PyMuPDF pdfplumber indic-nlp-library
```

**Library Details:**
- **PyMuPDF (fitz)**: Fast, reliable text extraction and structural analysis
- **pdfplumber**: Robust table detection and extraction
- **indic-nlp-library**: Script-specific normalization for Hindi (Devanagari)

## Usage

### Basic Usage

1. **Place your PDF files** in the same directory as `ncert_extractor.py` or update the paths in the script.

2. **Update the file paths** in the `if __name__ == "__main__":` block:

```python
# Update these paths to match your files
english_pdf = base_dir / "NCERT_Class10_Science_EN.pdf"
english_output = base_dir / "NCERT_Class10_Science_EN.txt"

hindi_pdf = base_dir / "NCERT_Class10_Science_HI.pdf"
hindi_output = base_dir / "NCERT_Class10_Science_HI.txt"
```

3. **Run the script**:

```bash
python ncert_extractor.py
```

### Advanced Usage

You can also import and use the functions programmatically:

```python
from ncert_extractor import extract_ncert_content

# Extract English content
extract_ncert_content(
    pdf_path="path/to/english.pdf",
    lang='en',
    output_path="output_en.txt"
)

# Extract Hindi content
extract_ncert_content(
    pdf_path="path/to/hindi.pdf",
    lang='hi',
    output_path="output_hi.txt"
)
```

## Script Architecture

### Main Function: `extract_ncert_content()`

The core extraction function that orchestrates the entire process:

1. **Table Detection**: Uses `pdfplumber.find_tables()` to identify tables
2. **Table Conversion**: Converts tables to Markdown format with `[TABLE START]` and `[TABLE END]` markers
3. **Text Extraction**: Uses PyMuPDF to extract general text content
4. **Integration**: Merges tables back into the reading flow
5. **Cleaning**: Applies `general_cleaner()` to remove artifacts
6. **Normalization**: Applies `indic_normalize()` for Hindi text

### Helper Functions

#### `general_cleaner(text: str) -> str`

Cleans and normalizes extracted text:
- **Hyphenation Removal**: Re-joins words broken across lines (e.g., `knowl-\nedge` → `knowledge`)
- **Boilerplate Removal**: Removes page numbers, headers, footers using regex patterns
- **Whitespace Cleanup**: Consolidates multiple newlines and spaces

#### `indic_normalize(text: str, lang: str) -> str`

Normalizes Hindi (Devanagari) text:
- **ZWJ/ZWNJ Removal**: Removes zero-width joiners/non-joiners
- **Nukta Canonicalization**: Standardizes Nukta-based characters
- **Punctuation Correction**: Replaces pipe (`|`) with Hindi poorna virama (`।`)

#### `extract_tables_from_page(page) -> List[Tuple[str, int]]`

Extracts tables from a pdfplumber page:
- Detects all tables on the page
- Converts to Markdown format with proper row/column structure
- Returns table content with position information

## Output Format

The script generates clean text files with:
- **One paragraph per line**: Easy to process for sentence alignment
- **Tables in Markdown**: Preserves structure with `[TABLE START]` and `[TABLE END]` markers
- **Normalized text**: Ready for downstream NLP tasks

### Example Output Structure

```
This is the first paragraph of text from the PDF.
This is the second paragraph.
[TABLE START]
| Header 1 | Header 2 | Header 3 |
| --- | --- | --- |
| Cell 1 | Cell 2 | Cell 3 |
| Cell 4 | Cell 5 | Cell 6 |
[TABLE END]
This is text that appears after the table.
```

## Supported Languages

- **English (`en`)**: Standard text extraction and cleaning
- **Hindi (`hi`)**: Enhanced with Indic-specific normalization

## Error Handling

The script includes comprehensive error handling:
- Graceful degradation if `indic-nlp-library` is not available
- Page-level error reporting without stopping the entire extraction
- File existence checks before processing

## Performance

- **Fast extraction**: PyMuPDF is optimized for speed
- **Progress reporting**: Real-time page-by-page progress updates
- **Memory efficient**: Processes pages sequentially

## Next Steps

After extraction, the output text files are ready for:
1. **Sentence Alignment**: Align parallel English-Hindi sentences
2. **Translation Memory**: Build translation databases
3. **NLP Training**: Use as training data for machine translation models

## Troubleshooting

### Issue: `indic-nlp-library` import error

**Solution**: The script will work with limited Hindi normalization. Install the library for full functionality:
```bash
pip install indic-nlp-library
```

### Issue: Tables not extracted correctly

**Solution**: Ensure `pdfplumber` is installed correctly. Some complex table layouts may require manual adjustment.

### Issue: PDF file not found

**Solution**: Check that the PDF paths in the script match your actual file locations. Use absolute paths if needed.

## License

This script is part of the NICO AI project.

## Support

For issues or questions, please refer to the project documentation or contact the development team.
