"""Page-level PDF text. Fast extract first; OCR only if a page is empty."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pdfplumber

try:
    import pytesseract
    from pdf2image import convert_from_path

    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


@dataclass
class Page:
    source: str
    page_num: int
    text: str
    extraction_method: str = "text"


def _ocr_page(pdf_path: str, page_num: int) -> str:
    images = convert_from_path(
        pdf_path, first_page=page_num, last_page=page_num, dpi=300
    )
    if not images:
        return ""
    return pytesseract.image_to_string(images[0]).strip()


def load_pdf(file_path: str | Path, verbose: bool = False) -> list[Page]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Not a PDF file: {path}")

    pages: list[Page] = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = (page.extract_text() or "").strip()
            method = "text"
            if not text and OCR_AVAILABLE:
                try:
                    text = _ocr_page(str(path), i)
                    method = "ocr"
                except Exception:
                    text = ""
            if text:
                pages.append(
                    Page(
                        source=path.name,
                        page_num=i,
                        text=text,
                        extraction_method=method,
                    )
                )
            elif verbose:
                print(f"    skip empty page {i} of {path.name}")
    return pages


def load_pdfs(file_paths: list[str | Path], verbose: bool = True) -> list[Page]:
    all_pages: list[Page] = []
    for fp in file_paths:
        try:
            pages = load_pdf(fp, verbose=verbose)
            all_pages.extend(pages)
            if verbose:
                n_text = sum(1 for p in pages if p.extraction_method == "text")
                n_ocr = sum(1 for p in pages if p.extraction_method == "ocr")
                print(
                    f"  loaded {len(pages)} pages from {Path(fp).name} "
                    f"({n_text} text, {n_ocr} OCR)"
                )
        except (FileNotFoundError, ValueError) as exc:
            if verbose:
                print(f"  skip {fp}: {exc}")
    return all_pages
