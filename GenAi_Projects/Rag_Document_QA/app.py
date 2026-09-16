"""Streamlit UI. Upload up to 10 PDFs, pick a retrieval method, ask with citations."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st

os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY_DISABLED"] = "1"
sys.path.insert(0, str(Path(__file__).parent))

from src.chain import ask
from src.chunker import chunk_pages
from src.config import (
    DEFAULT_DB_PATH,
    DEFAULT_TOP_K,
    LLM_MODEL,
    MAX_PDFS,
    RETRIEVAL_METHODS,
    UPLOAD_DIR,
)
from src.pdf_loader import OCR_AVAILABLE, load_pdfs
from src.vectorstore import clear_vectorstore, collection_count, ingest_chunks

st.set_page_config(page_title="Multi-Doc RAG Q&A", page_icon="📄", layout="wide")


def init_state() -> None:
    st.session_state.setdefault("processed", collection_count(DEFAULT_DB_PATH) > 0)
    st.session_state.setdefault("chat_history", [])
    st.session_state.setdefault("num_chunks", collection_count(DEFAULT_DB_PATH))
    st.session_state.setdefault("method", "hybrid")


init_state()

with st.sidebar:
    st.header("Documents")
    uploaded = st.file_uploader(
        f"PDF files (max {MAX_PDFS})",
        type=["pdf"],
        accept_multiple_files=True,
    )
    method = st.selectbox("Retrieval", RETRIEVAL_METHODS, index=2)
    st.session_state.method = method
    top_k = st.slider("top_k", 2, 12, DEFAULT_TOP_K)

    process = st.button("Process PDFs", type="primary", disabled=not uploaded)
    if process:
        if len(uploaded) > MAX_PDFS:
            st.error(f"Cap is {MAX_PDFS} PDFs.")
            st.stop()
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        paths = []
        for f in uploaded:
            path = UPLOAD_DIR / Path(f.name).name
            path.write_bytes(f.getbuffer())
            paths.append(str(path))
        with st.spinner("Load → chunk → embed (replaces rows for those filenames)"):
            pages = load_pdfs(paths)
            if not pages:
                st.error("No text extracted.")
                st.stop()
            chunks = chunk_pages(pages)
            count = ingest_chunks(chunks, db_path=DEFAULT_DB_PATH, replace_sources=True)
        st.session_state.processed = True
        st.session_state.num_chunks = collection_count(DEFAULT_DB_PATH)
        st.success(f"{len(pages)} pages → {count} chunks (index now {st.session_state.num_chunks})")

    if st.button("Clear vector DB"):
        clear_vectorstore(db_path=DEFAULT_DB_PATH)
        st.session_state.processed = False
        st.session_state.chat_history = []
        st.session_state.num_chunks = 0
        st.success("Cleared.")

    st.divider()
    st.caption(f"Chunks in DB: {st.session_state.num_chunks}")
    st.caption(f"OCR: {'on' if OCR_AVAILABLE else 'off (install pytesseract + poppler)'}")
    st.caption(f"LLM: {LLM_MODEL}")
    st.caption("Citations are filenames + page numbers, not PDF deep-links.")

st.title("Multi-Doc RAG Q&A")
st.markdown(
    "Answers are grounded in retrieved chunks. Each source is `filename, p.N`. "
    "Retrieval is **hybrid (MiniLM + BM25)** unless you switch it in the sidebar."
)

if not st.session_state.processed:
    st.info("Upload PDFs and click Process, or run `python -m eval.run_eval` on the sample papers first.")
    st.stop()

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("citations"):
            st.caption("Sources: " + " · ".join(msg["citations"]))

question = st.chat_input("Ask a question about the indexed PDFs")
if question:
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Retrieve + generate"):
            result = ask(
                question=question,
                db_path=DEFAULT_DB_PATH,
                top_k=top_k,
                method=st.session_state.method,
            )
        st.write(result.answer)
        cites = []
        if result.citations:
            bits = []
            for i, c in enumerate(result.citations, 1):
                score = f"{c.score:.3f}" if c.score is not None else "—"
                bits.append(f"[{i}] {c.citation} (score {score})")
            st.caption("Sources: " + " · ".join(bits))
            cites = [f"[{i}] {c.citation}" for i, c in enumerate(result.citations, 1)]
    st.session_state.chat_history.append(
        {"role": "assistant", "content": result.answer, "citations": cites}
    )
