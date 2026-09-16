from pathlib import Path

from src.config import SAMPLE_PDF_DIR
from src.pdf_loader import load_pdf


def test_attention_pdf_has_transformer_on_page_1():
    pdf = SAMPLE_PDF_DIR / "attention_is_all_you_need.pdf"
    assert pdf.exists(), "sample PDF missing — do not gitignore data/sample_pdfs/"
    pages = load_pdf(pdf)
    assert len(pages) >= 10
    first = pages[0].text
    assert "Attention" in first
    assert "Vaswani" in first


def test_rag_pdf_page_count():
    pdf = SAMPLE_PDF_DIR / "rag_lewis_2020.pdf"
    pages = load_pdf(pdf)
    assert len(pages) >= 15
    assert "Retrieval-Augmented" in pages[0].text
