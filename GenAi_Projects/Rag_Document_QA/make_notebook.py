"""Generates notebooks/exploration.ipynb with the RAG pipeline test cells."""
import json
import os
from pathlib import Path

cells = [
    # Cell 1: Markdown intro
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# RAG Pipeline Exploration\n",
            "\n",
            "End-to-end test of the Multi-Doc RAG Q&A system on real PDFs.\n",
            "\n",
            "**Pipeline:** PDF → Pages → Chunks → Embeddings → Vector DB → Retrieval → LLM → Answer + Citations\n",
            "\n",
            "## Setup\n",
            "1. Drop 2-5 PDFs into `data/sample_pdfs/`\n",
            "2. Run the cells in order\n",
            "3. Ask questions in the final cell"
        ]
    },
    # Cell 2: imports
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import sys\n",
            "sys.path.append('..')\n",
            "\n",
            "from src.pdf_loader import load_pdfs\n",
            "from src.chunker import chunk_pages, DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP\n",
            "from src.vectorstore import ingest_chunks, clear_vectorstore, get_vectorstore, DEFAULT_DB_PATH\n",
            "from src.chain import ask\n",
            "\n",
            "print('✓ All modules imported')"
        ]
    },
    # Cell 3: list PDFs
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Step 1: Load PDFs\n",
            "\n",
            "Drop your PDFs into `data/sample_pdfs/` first. Then run the cell below."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from pathlib import Path\n",
            "\n",
            "pdf_dir = Path('../data/sample_pdfs')\n",
            "pdf_files = sorted(pdf_dir.glob('*.pdf'))\n",
            "\n",
            "if not pdf_files:\n",
            "    print('⚠ No PDFs found in data/sample_pdfs/')\n",
            "    print('  Drop some PDFs there, then re-run this cell.')\n",
            "else:\n",
            "    print(f'Found {len(pdf_files)} PDFs:')\n",
            "    for p in pdf_files:\n",
            "        print(f'  - {p.name}')"
        ]
    },
    # Cell 4: load
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "pages = load_pdfs([str(p) for p in pdf_files])\n",
            "print(f'\\nTotal pages loaded: {len(pages)}')"
        ]
    },
    # Cell 5: chunk
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Step 2: Chunk the pages"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "chunks = chunk_pages(pages, chunk_size=DEFAULT_CHUNK_SIZE, chunk_overlap=DEFAULT_CHUNK_OVERLAP)\n",
            "print(f'\\nTotal chunks: {len(chunks)}')"
        ]
    },
    # Cell 6: ingest
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Step 3: Ingest into vector DB\n",
            "\n",
            "First run takes ~1 sec/chunk. Subsequent runs skip (persistent DB)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "count = ingest_chunks(chunks, db_path=DEFAULT_DB_PATH)\n",
            "print(f'Ingested {count} chunks')"
        ]
    },
    # Cell 7: ask
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Step 4: Ask questions\n",
            "\n",
            "Replace the question below with your own and re-run."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "result = ask(\n",
            "    question='What is this document about?',\n",
            "    db_path=DEFAULT_DB_PATH,\n",
            "    top_k=4,\n",
            ")\n",
            "\n",
            "print('Question:', result.question)\n",
            "print('\\nAnswer:', result.answer)\n",
            "print('\\nCitations:')\n",
            "for i, c in enumerate(result.citations, 1):\n",
            "    print(f'  [{i}] {c.citation} (score: {c.score:.4f})')"
        ]
    },
    # Cell 8: try more questions
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Step 5: Try more questions\n",
            "\n",
            "Add your own questions below."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "my_questions = [\n",
            "    'What skills are mentioned?',\n",
            "    'What is the main topic?',\n",
            "]\n",
            "\n",
            "for q in my_questions:\n",
            "    result = ask(question=q, db_path=DEFAULT_DB_PATH, top_k=4)\n",
            "    print(f'\\n{\"=\"*60}')\n",
            "    print(f'Q: {q}')\n",
            "    print(f'A: {result.answer}')\n",
            "    print(f'Citations: {[c.citation for c in result.citations]}')"
        ]
    },
    # Cell 9: cleanup
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Cleanup (optional)\n",
            "\n",
            "Run this to wipe the vector DB (e.g., before re-ingesting new PDFs)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# clear_vectorstore(db_path=DEFAULT_DB_PATH)\n",
            "# print('Vector DB cleared. Re-run Step 3 to re-ingest.')"
        ]
    },
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.11"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

# Use absolute path — resolves relative to THIS script's location
# so it works no matter where you run `python make_notebook.py` from
script_dir = os.path.dirname(os.path.abspath(__file__))
notebooks_dir = os.path.join(script_dir, 'notebooks')
os.makedirs(notebooks_dir, exist_ok=True)
out = os.path.join(notebooks_dir, 'exploration.ipynb')

with open(out, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1)
print(f'✓ Created {out}')