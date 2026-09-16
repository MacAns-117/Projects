<h1>Multi-Doc RAG Q&amp;A with Citations</h1>

<p>
  <img src="https://img.shields.io/badge/projects-1-blue?style=flat-square" alt="1 project">
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/langchain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" alt="LangChain">
  <img src="https://img.shields.io/badge/chromadb-FF6F00?style=flat-square&logo=chroma&logoColor=white" alt="ChromaDB">
  <img src="https://img.shields.io/badge/groq-F55036?style=flat-square&logo=groq&logoColor=white" alt="Groq">
  <img src="https://img.shields.io/badge/streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Live Demo">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<p>A portfolio RAG system — upload PDFs, ask questions, get cited answers. Hybrid retrieval (BM25 + vector cosine), OCR fallback for scanned docs, measured on a 24-question gold set.</p>

<h2>Live Demo</h2>

<p>🔗 <strong><a href="https://projects-wktkeuxu6u3nqmz9vdyith.streamlit.app/">projects-wktkeuxu6u3nqmz9vdyith.streamlit.app</a></strong></p>

<p>Try it now — upload any PDF (text-based or scanned) and ask questions. No login required.</p>

<h2>What it does</h2>

<ul>
  <li>User uploads 1-10 PDFs via the Streamlit UI</li>
  <li>System chunks and embeds them into a persistent Chroma vector database</li>
  <li>OCR fallback (Tesseract) automatically handles scanned/image-based PDFs</li>
  <li>User asks a question in natural language via chat interface</li>
  <li>System retrieves the top-K most relevant chunks via <strong>hybrid search</strong> (BM25 keyword + vector cosine, weight 0.6)</li>
  <li>LLM generates an answer grounded in retrieved context, with inline citations like <code>[doc1.pdf, p.3]</code></li>
  <li>Anti-hallucination: honestly says "I don't know" when context doesn't contain the answer</li>
  <li>FastAPI wrapper also available for programmatic access (<code>/health</code>, <code>/ingest</code>, <code>/ask</code>)</li>
</ul>

<h2>Measured retrieval quality</h2>

<p>Tested on a 24-question gold set (22 in-scope + 2 out-of-scope) across 2 public arXiv papers:</p>

<table>
  <thead>
    <tr><th>Retrieval Method</th><th>Hit@8</th><th>Hits</th><th>Default?</th></tr>
  </thead>
  <tbody>
    <tr><td>Cosine similarity (MiniLM only)</td><td>59.1%</td><td>13/22</td><td>—</td></tr>
    <tr><td>MMR (diversity-aware)</td><td>68.2%</td><td>15/22</td><td>—</td></tr>
    <tr><td><strong>Hybrid (BM25 + vector)</strong></td><td><strong>77.3%</strong></td><td><strong>17/22</strong></td><td><strong>✓ Yes</strong></td></tr>
  </tbody>
</table>

<p>Hit@8 = at least one retrieved chunk's source page matches the gold page. Hybrid is the default in the app and API because it won on this set.</p>

<h2>Tech stack</h2>

<table>
  <thead>
    <tr><th>Layer</th><th>Tools</th></tr>
  </thead>
  <tbody>
    <tr><td>Language</td><td>Python 3.11</td></tr>
    <tr><td>Orchestration</td><td>LangChain 0.3.7</td></tr>
    <tr><td>Vector DB</td><td>Chroma 0.5.20 (persistent)</td></tr>
    <tr><td>Embeddings</td><td>HuggingFace all-MiniLM-L6-v2 (384-dim, local, free)</td></tr>
    <tr><td>Hybrid search</td><td>rank-bm25 + vector cosine (weight 0.6)</td></tr>
    <tr><td>LLM</td><td>Groq openai/gpt-oss-120b (free tier)</td></tr>
    <tr><td>PDF parsing</td><td>pdfplumber 0.11.4</td></tr>
    <tr><td>OCR fallback</td><td>Tesseract + pytesseract + pdf2image</td></tr>
    <tr><td>Web UI</td><td>Streamlit 1.40.1</td></tr>
    <tr><td>REST API</td><td>FastAPI (/health, /ingest, /ask)</td></tr>
    <tr><td>Testing</td><td>pytest (12 tests, 11 pass)</td></tr>
    <tr><td>Deployment</td><td>Streamlit Community Cloud (free)</td></tr>
  </tbody>
</table>

<h2>How to run locally</h2>

<pre><code># Clone the Projects repo
git clone https://github.com/MacAns-117/Projects.git
cd "Projects/GenAi_Projects/Rag_Document_QA"

# Create venv (Python 3.11)
conda create -n rag-qa python=3.11 -y
conda activate rag-qa

# Install deps
pip install -r requirements.txt

# Add your Groq API key
cp .env.example .env
# Edit .env and paste your GROQ_API_KEY (get one free at console.groq.com)

# Run the Streamlit app
streamlit run app.py

# Or run the FastAPI server
uvicorn api:app --reload

# Run the evaluation (no Groq key needed)
python -m eval.run_eval

# Run the tests
python -m pytest tests/ -q</code></pre>

<h2>Repo layout</h2>

<pre><code>Rag_Document_QA/
├── app.py                          # Streamlit UI (multi-PDF upload + chat)
├── api.py                          # FastAPI wrapper (/health /ingest /ask)
├── src/
│   ├── config.py                   # Centralized config (chunk size, top_k, model, weights)
│   ├── pdf_loader.py               # PDF loading + parsing (with OCR fallback)
│   ├── chunker.py                  # RecursiveCharacterTextSplitter (1000-char, 200-overlap)
│   ├── embeddings.py               # HuggingFace all-MiniLM-L6-v2 (cached)
│   ├── vectorstore.py               # Persistent Chroma DB with replace-on-reingest
│   ├── retriever.py                # Hybrid retrieval (BM25 + vector, MMR, similarity)
│   ├── llm.py                      # Groq openai/gpt-oss-120b wrapper (cached)
│   └── chain.py                    # End-to-end RAG with 7-rule citation prompt
├── eval/
│   ├── gold_qa.json                # 24 labelled questions on 2 arXiv PDFs
│   ├── run_eval.py                 # Eval runner (no Groq key needed)
│   ├── results.md                  # Measured Hit@8 table
│   ├── results.json                # Machine-readable results
│   └── figures/
│       └── hit_at_8.png            # Bar chart of retrieval method comparison
├── tests/
│   ├── conftest.py                 # Shared fixtures
│   ├── test_pdf_loader.py          # PDF extraction tests
│   ├── test_chunker.py             # Chunk ID stability + overlap tests
│   ├── test_vectorstore.py         # Replace-on-reingest tests
│   ├── test_retriever.py           # Hybrid retrieval + clear tests
│   ├── test_gold_qa.py             # Gold file validation tests
│   └── test_prompt.py              # Prompt rules validation tests
├── data/
│   ├── sample_pdfs/                # 2 shipped arXiv papers (Attention + Lewis RAG)
│   └── README.md
├── .env.example
├── .gitignore
├── requirements.txt
├── packages.txt                    # Tesseract + poppler-utils for Streamlit Cloud
├── pytest.ini
├── LICENSE                         # MIT
└── README.md</code></pre>

<h2>Limits</h2>

<ul>
  <li><strong>Hit@8 is retrieval-only.</strong> It measures whether the right page appears in the top-8 chunks — not whether the LLM's answer is correct. A full RAGAS evaluation (faithfulness scoring) would require Groq calls on every gold answer.</li>
  <li><strong>Hybrid still misses 6 questions.</strong> Positional encodings, dropout, the Lewis email line, Table 7 NQ train size, T5-11B vs RAG-Sequence, and the cross-paper "who introduced the Transformer" question. Tables and author lines are where MiniLM is weakest.</li>
  <li><strong>No reranker.</strong> A cross-encoder re-ranker (e.g., bge-reranker) could improve Hit@8 further by re-scoring the top candidates.</li>
  <li><strong>No OOS refusal gate.</strong> The score floor (0.22) doesn't block out-of-scope questions — they still retrieve chunks. The 2 OOS questions in the gold set retrieved results instead of being refused.</li>
  <li><strong>Streamlit Cloud is ephemeral.</strong> The vector DB doesn't persist across reboots — users re-upload PDFs on each session.</li>
  <li><strong>Not a hosted document product.</strong> This is a portfolio RAG, not a production system. No auth, no rate limiting, no monitoring, no persistence layer.</li>
</ul>

<h2>Status</h2>

<p>✅ <strong>Live</strong> — deployed on Streamlit Community Cloud. Auto-redeploys on every push to main.</p>

<h2>License</h2>

<p>MIT</p>
