"""
PDF loader module — extracts page-level text from PDF files.

Tries normal text extraction first (fast). If a page returns 0 chars
(scanned/image-based PDF), falls back to OCR via Tesseract (slower).

Returns a list of Page objects, each containing the source filename,
page number (1-indexed), and the extracted text. This granularity is
what lets the RAG system cite back to specific pages later.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pdfplumber

# OCR imports — loaded lazily so the module doesn't fail if Tesseract isn't installed
try:
    import pytesseract
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


@dataclass
class Page:
    """A single page extracted from a PDF."""
    source: str
    page_num: int
    text: str
    extraction_method: str = "text"  # "text" or "ocr"


def _ocr_page(pdf_path: str, page_num: int) -> str:
    """OCR a single page of a PDF using Tesseract.

    Converts the PDF page to an image, then runs Tesseract OCR on it.
    """
    # convert_from_path is 1-indexed for the page number
    images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num, dpi=300)
    if not images:
        return ""
    text = pytesseract.image_to_string(images[0])
    return text.strip()


def load_pdf(file_path: str | Path) -> list[Page]:
    """Load a single PDF file and extract text page-by-page.

    For each page:
      1. Try normal text extraction (fast, ~0.1 sec/page)
      2. If 0 chars extracted, fall back to OCR (slow, ~3-5 sec/page)

    Args:
        file_path: Path to the PDF file.

    Returns:
        List of Page objects, one per page with non-empty text.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Not a PDF file: {path}")

    pages: list[Page] = []
    source_name = path.name

    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            # Step 1: try fast text extraction
            text = (page.extract_text() or "").strip()
            method = "text"

            # Step 2: if no text, try OCR fallback
            if not text and OCR_AVAILABLE:
                print(f"    → Page {i}: no text found, trying OCR...")
                try:
                    text = _ocr_page(str(path), i)
                    method = "ocr"
                    if text:
                        print(f"    ✓ OCR extracted {len(text)} chars from page {i}")
                    else:
                        print(f"    ✗ OCR found no text on page {i}")
                except Exception as e:
                    print(f"    ✗ OCR failed on page {i}: {e}")

            if text:
                pages.append(
                    Page(
                        source=source_name,
                        page_num=i,
                        text=text,
                        extraction_method=method,
                    )
                )

    return pages


def load_pdfs(file_paths: list[str | Path]) -> list[Page]:
    """Load multiple PDF files and return a combined list of pages."""
    all_pages: list[Page] = []
    for fp in file_paths:
        try:
            pages = load_pdf(fp)
            all_pages.extend(pages)
            text_count = sum(1 for p in pages if p.extraction_method == "text")
            ocr_count = sum(1 for p in pages if p.extraction_method == "ocr")
            print(f"  ✓ Loaded {len(pages)} pages from {Path(fp).name} "
                  f"({text_count} text, {ocr_count} OCR)")
        except (FileNotFoundError, ValueError) as e:
            print(f"  ✗ Skipped {fp}: {e}")
    return all_pages


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    import sys

    if not OCR_AVAILABLE:
        print("⚠ OCR not available. Install with:")
        print("  pip install pytesseract pdf2image")
        print("  conda install -c conda-forge poppler")
        print("  + Install Tesseract OCR engine\n")

    if len(sys.argv) < 2:
        print("Usage: python -m src.pdf_loader <pdf_path> [pdf_path2 ...]")
        sys.exit(1)

    pdf_paths = sys.argv[1:]
    pages = load_pdfs(pdf_paths)

    print(f"\nLoaded {len(pages)} pages total.")
    if pages:
        first = pages[0]
        preview = first.text[:200].replace("\n", " ")
        print(f"\nFirst page: {first.source} p.{first.page_num} ({first.extraction_method})")
        print(f"Preview: {preview}...")