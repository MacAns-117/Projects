"""
Streamlit web app for Multi-Doc RAG Q&A with Citations.

Users can:
1. Upload one or more PDFs
2. Click "Process PDFs" to ingest them into the vector DB
3. Type questions in a chat box
4. See answers with clickable citations

Run with:
    streamlit run app.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st

# Silence Chroma telemetry warnings (harmless but noisy)
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY_DISABLED"] = "1"

# Make sure src/ is importable
sys.path.insert(0, str(Path(__file__).parent))

from src.pdf_loader import load_pdfs, OCR_AVAILABLE
from src.chunker import chunk_pages, DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP
from src.vectorstore import ingest_chunks, clear_vectorstore, DEFAULT_DB_PATH
from src.chain import ask


# --- Page config ---
st.set_page_config(
    page_title="Multi-Doc RAG Q&A",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- Session state ---
def init_state():
    """Initialize session state variables."""
    if "processed" not in st.session_state:
        st.session_state.processed = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "num_pdfs" not in st.session_state:
        st.session_state.num_pdfs = 0
    if "num_chunks" not in st.session_state:
        st.session_state.num_chunks = 0


init_state()


# --- Sidebar ---
with st.sidebar:
    st.header("📚 Document Manager")

    # Upload PDFs
    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload 1-10 PDF files. Text-based PDFs process in seconds; "
             "scanned PDFs use OCR (slower).",
    )

    if uploaded_files:
        st.info(f"{len(uploaded_files)} file(s) ready to process")

    # Process button
    if st.button("🔄 Process PDFs", type="primary", disabled=not uploaded_files):
        # Save uploaded files to temp location
        temp_dir = Path("data/uploaded_pdfs")
        temp_dir.mkdir(parents=True, exist_ok=True)

        saved_paths = []
        for f in uploaded_files:
            path = temp_dir / f.name
            with open(path, "wb") as out:
                out.write(f.getbuffer())
            saved_paths.append(str(path))

        # Load + chunk + ingest
        with st.spinner("Loading PDFs..."):
            pages = load_pdfs(saved_paths)
            if not pages:
                st.error("No text could be extracted from these PDFs.")
                st.stop()

        with st.spinner("Chunking pages..."):
            chunks = chunk_pages(
                pages,
                chunk_size=DEFAULT_CHUNK_SIZE,
                chunk_overlap=DEFAULT_CHUNK_OVERLAP,
            )

        with st.spinner("Embedding + ingesting into vector DB (may take a few seconds)..."):
            count = ingest_chunks(chunks, db_path=DEFAULT_DB_PATH)

        st.session_state.processed = True
        st.session_state.num_pdfs = len(set(p.source for p in pages))
        st.session_state.num_chunks = count
        st.success(
            f"✅ Processed {st.session_state.num_pdfs} PDF(s) "
            f"→ {st.session_state.num_chunks} chunks ingested"
        )

    # Clear DB button
    if st.button("🗑️ Clear Vector DB"):
        clear_vectorstore(db_path=DEFAULT_DB_PATH)
        st.session_state.processed = False
        st.session_state.chat_history = []
        st.success("Vector DB cleared. Upload new PDFs to start over.")

    # Status
    st.divider()
    st.subheader("Status")
    if st.session_state.processed:
        st.success(f"✅ Ready — {st.session_state.num_chunks} chunks indexed")
    else:
        st.warning("⚠ Upload + process PDFs to start asking questions")

    # OCR status
    st.caption(f"OCR fallback: {'✅ Available' if OCR_AVAILABLE else '❌ Not installed'}")

    # Tech info
    st.divider()
    st.caption("**Tech stack:**")
    st.caption("• LangChain 0.3.7")
    st.caption("• Chroma 0.5.20 (persistent)")
    st.caption("• HuggingFace all-MiniLM-L6-v2")
    st.caption("• Groq openai/gpt-oss-120b")
    st.caption("• Streamlit 1.40.1")


# --- Main panel ---
st.title("📄 Multi-Doc RAG Q&A with Citations")
st.markdown(
    "Ask questions across your PDF documents and get answers with "
    "**clickable citations** back to the source pages."
)

if not st.session_state.processed:
    st.info("👈 Upload PDFs in the sidebar and click **Process PDFs** to begin.")
    st.stop()

# --- Chat interface ---
st.divider()
st.subheader("💬 Ask a question")

# Display chat history
for msg in st.session_state.chat_history:
    role = msg["role"]
    with st.chat_message(role):
        if role == "user":
            st.write(msg["content"])
        else:
            st.write(msg["content"])
            if msg.get("citations"):
                st.caption("**Sources:**")
                for i, c in enumerate(msg["citations"], 1):
                    st.caption(f"[{i}] {c}")

# Input box
question = st.chat_input("Ask a question about your documents...")

if question:
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": question})

    # Display user message
    with st.chat_message("user"):
        st.write(question)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = ask(
                question=question,
                db_path=DEFAULT_DB_PATH,
                top_k=4,
            )

        st.write(result.answer)

        if result.citations:
            st.caption("**Sources:**")
            for i, c in enumerate(result.citations, 1):
                st.caption(f"[{i}] {c.citation} (score: {c.score:.4f})")

    # Add assistant message to history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": result.answer,
        "citations": [c.citation for c in result.citations],
    })