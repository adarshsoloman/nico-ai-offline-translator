"""
NCERT Batch PDF Extractor
==========================

Batch processing script to extract all NCERT Science PDFs (Class 10)
from the pdfs/ directory and save organized outputs.

Usage:
    python main.py
    # or
    uv run main.py

Author: NICO AI
Date: 2025-11-29
"""

from pathlib import Path
from ncert_extractor import extract_ncert_content
import sys


def main():
    """
    Batch process all NCERT PDFs in the pdfs/ directory.
    
    Directory structure:
        pdfs/
        ├── science-en/  (English PDFs)
        └── science-hi/  (Hindi PDFs)
    
    Output structure:
        outputs/
        ├── science-en/  (English text files)
        └── science-hi/  (Hindi text files)
    """
    
    # Define base directories
    base_dir = Path(__file__).parent
    pdfs_dir = base_dir / "pdfs"
    outputs_dir = base_dir / "outputs"
    
    # Create output directories
    outputs_dir.mkdir(exist_ok=True)
    (outputs_dir / "science-en").mkdir(exist_ok=True)
    (outputs_dir / "science-hi").mkdir(exist_ok=True)
    
    print("=" * 70)
    print("NCERT BATCH PDF EXTRACTOR")
    print("=" * 70)
    print(f"\nInput directory:  {pdfs_dir}")
    print(f"Output directory: {outputs_dir}\n")
    
    # Process English PDFs
    english_pdfs_dir = pdfs_dir / "science-en"
    english_output_dir = outputs_dir / "science-en"
    
    if english_pdfs_dir.exists():
        english_pdfs = sorted(english_pdfs_dir.glob("*.pdf"))
        print(f"📚 Found {len(english_pdfs)} English PDFs")
        print("-" * 70)
        
        for idx, pdf_path in enumerate(english_pdfs, 1):
            output_path = english_output_dir / f"{pdf_path.stem}.txt"
            
            print(f"\n[{idx}/{len(english_pdfs)}] Processing: {pdf_path.name}")
            
            try:
                extract_ncert_content(
                    pdf_path=str(pdf_path),
                    lang='en',
                    output_path=str(output_path)
                )
            except Exception as e:
                print(f"❌ ERROR: {e}")
                continue
    else:
        print(f"⚠️  English PDFs directory not found: {english_pdfs_dir}")
    
    print("\n" + "=" * 70)
    
    # Process Hindi PDFs
    hindi_pdfs_dir = pdfs_dir / "science-hi"
    hindi_output_dir = outputs_dir / "science-hi"
    
    if hindi_pdfs_dir.exists():
        hindi_pdfs = sorted(hindi_pdfs_dir.glob("*.pdf"))
        print(f"📚 Found {len(hindi_pdfs)} Hindi PDFs")
        print("-" * 70)
        
        for idx, pdf_path in enumerate(hindi_pdfs, 1):
            output_path = hindi_output_dir / f"{pdf_path.stem}.txt"
            
            print(f"\n[{idx}/{len(hindi_pdfs)}] Processing: {pdf_path.name}")
            
            try:
                extract_ncert_content(
                    pdf_path=str(pdf_path),
                    lang='hi',
                    output_path=str(output_path)
                )
            except Exception as e:
                print(f"❌ ERROR: {e}")
                continue
    else:
        print(f"⚠️  Hindi PDFs directory not found: {hindi_pdfs_dir}")
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ BATCH EXTRACTION COMPLETE!")
    print("=" * 70)
    
    # Count output files
    en_outputs = list(english_output_dir.glob("*.txt"))
    hi_outputs = list(hindi_output_dir.glob("*.txt"))
    
    print(f"\n📊 Summary:")
    print(f"   English texts: {len(en_outputs)} files in {english_output_dir}")
    print(f"   Hindi texts:   {len(hi_outputs)} files in {hindi_output_dir}")
    print(f"\n   Total:         {len(en_outputs) + len(hi_outputs)} text files extracted")
    print("\n" + "=" * 70)
    print("🎯 Next step: Sentence alignment")
    print("=" * 70)


if __name__ == "__main__":
    main()
