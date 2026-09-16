from src.chunker import chunk_id, chunk_page
from src.config import CHUNK_OVERLAP, CHUNK_SIZE
from src.pdf_loader import Page


def test_chunk_id_is_stable():
    from src.chunker import Chunk

    a = Chunk("attention_is_all_you_need.pdf", 3, "hello", 0)
    b = Chunk("attention_is_all_you_need.pdf", 3, "hello", 0)
    assert chunk_id(a) == chunk_id(b)
    assert "p3" in chunk_id(a)


def test_short_page_is_one_chunk():
    page = Page("demo.pdf", 1, "Short page.", "text")
    chunks = chunk_page(page)
    assert len(chunks) == 1
    assert chunks[0].source == "demo.pdf"
    assert chunks[0].page_num == 1


def test_long_page_overlaps():
    text = ("Transformer layer. " * 80).strip()
    page = Page("demo.pdf", 2, text, "text")
    chunks = chunk_page(page, chunk_size=120, chunk_overlap=30)
    assert len(chunks) >= 2
    assert CHUNK_SIZE == 1000
    assert CHUNK_OVERLAP == 200
