"""
Quick Usage Example for NCERT Extractor
========================================

This script demonstrates how to use the ncert_extractor module
for extracting content from NCERT PDFs.
"""

from ncert_extractor import extract_ncert_content
from pathlib import Path

def main():
    """
    Example usage of the NCERT extractor.
    
    Modify the paths below to match your PDF locations.
    """
    
    # Define your PDF paths
    base_dir = Path(__file__).parent
    
    # Example 1: Class 10 Science - English
    print("=" * 60)
    print("Example 1: Extracting English NCERT PDF")
    print("=" * 60)
    
    extract_ncert_content(
        pdf_path=str(base_dir / "NCERT_Class10_Science_EN.pdf"),
        lang='en',
        output_path=str(base_dir / "output_en.txt")
    )
    
    print("\n" + "=" * 60)
    print("Example 2: Extracting Hindi NCERT PDF")
    print("=" * 60)
    
    # Example 2: Class 10 Science - Hindi
    extract_ncert_content(
        pdf_path=str(base_dir / "NCERT_Class10_Science_HI.pdf"),
        lang='hi',
        output_path=str(base_dir / "output_hi.txt")
    )
    
    print("\n" + "=" * 60)
    print("✓ Extraction Complete!")
    print("=" * 60)
    print("\nOutput files:")
    print("  - output_en.txt (English)")
    print("  - output_hi.txt (Hindi)")
    print("\nThese files are ready for sentence alignment.")


if __name__ == "__main__":
    main()
