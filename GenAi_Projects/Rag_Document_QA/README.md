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
  <li>System retrieves candidates via <strong>hybrid search</strong> (BM25 + vector cosine, weight 0.6), then optionally <strong>cross-encoder reranks</strong> top-20 → top-k</li>
  <li>LLM generates an answer grounded in retrieved context, with inline citations like <code>[doc1.pdf, p.3]</code></li>
  <li>Anti-hallucination: honestly says "I don't know" when context doesn't contain the answer</li>
  <li>FastAPI wrapper also available for programmatic access (<code>/health</code>, <code>/ingest</code>, <code>/ask</code>)</li>
</ul>

<h2>Measured retrieval quality</h2>

<p>Tested on a 24-question gold set (22 in-scope + 2 out-of-scope) across 2 public arXiv papers.
<strong>Run:</strong> 2026-10-27 Asia/Calcutta · corpus = full arXiv PDFs (132 chunks) · MiniLM embeddings · hybrid weight 0.6 ·
<code>cross-encoder/ms-marco-MiniLM-L-6-v2</code> rerank (CPU, top-20 → 8) · CE logit floor −9.0 for OOS.</p>

<table>
  <thead>
    <tr><th>Method</th><th>Hit@8</th><th>MRR</th><th>Hits</th><th>OOS refuse</th></tr>
  </thead>
  <tbody>
    <tr><td>Cosine similarity</td><td>68.2%</td><td>0.406</td><td>15/22</td><td>0/2</td></tr>
    <tr><td>similarity + rerank</td><td>72.7%</td><td>0.499</td><td>16/22</td><td>2/2</td></tr>
    <tr><td>MMR</td><td>68.2%</td><td>0.411</td><td>15/22</td><td>0/2</td></tr>
    <tr><td>MMR + rerank</td><td>68.2%</td><td>0.534</td><td>15/22</td><td>2/2</td></tr>
    <tr><td>Hybrid (BM25 + vector)</td><td>77.3%</td><td>0.412</td><td>17/22</td><td>0/2</td></tr>
    <tr><td><strong>Hybrid + rerank (default when model loads)</strong></td><td><strong>77.3%</strong></td><td><strong>0.524</strong></td><td><strong>17/22</strong></td><td><strong>2/2</strong></td></tr>
  </tbody>
</table>

<p>Hit@8 = at least one retrieved chunk's source page matches the gold page. MRR = mean reciprocal rank of the first gold-page hit.
Rerank keeps Hit@8 on hybrid and lifts MRR (0.412 → 0.524); the CE logit floor fixes OOS refusal (0/2 → 2/2).
Full table: <code>eval/results.md</code>.</p>

<p>Unit tests ship tiny synthetic PDFs under <code>data/sample_pdfs/</code>. The table above used full arXiv PDFs in <code>data/arxiv_pdfs/</code> (gitignored) — see <code>data/README.md</code>.</p>

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
    <tr><td>Reranker</td><td>cross-encoder/ms-marco-MiniLM-L-6-v2 (CPU, optional)</td></tr>
    <tr><td>LLM</td><td>Groq openai/gpt-oss-120b (free tier)</td></tr>
    <tr><td>PDF parsing</td><td>pdfplumber 0.11.4</td></tr>
    <tr><td>OCR fallback</td><td>Tesseract + pytesseract + pdf2image</td></tr>
    <tr><td>Web UI</td><td>Streamlit 1.40.1</td></tr>
    <tr><td>REST API</td><td>FastAPI (/health, /ingest, /ask)</td></tr>
    <tr><td>Testing</td><td>pytest (retrieval + rerank + OOS + faithfulness mocks)</td></tr>
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

# Retrieval eval (no LLM key; prefers data/arxiv_pdfs/)
python -m eval.run_eval

# Faithfulness / OOS judge (Groq key, or a local server via LLM_* — see below)
# python -m eval.run_faithfulness

# Run the tests (no API keys)
python -m pytest tests/ -q</code></pre>

<h2>Run with a local model (llama.cpp / Ollama / LM Studio)</h2>

<p>Groq is the default and nothing changes if you leave the new variables unset (the hosted demo keeps using Groq). Set <code>LLM_PROVIDER=openai_compatible</code> to send every chat call to any server that speaks the OpenAI Chat Completions API instead. The provider switch lives in <code>src/llm.py</code>.</p>

<pre><code># 1. Start a server (pick one)
#    llama.cpp:  llama-server -m /path/to/model.gguf --alias my-model --port 8080 -c 32768 --jinja
#                (--jinja is the default in current builds; older builds need it for tool calls)
#    Ollama:     ollama serve            -> LLM_BASE_URL=http://localhost:11434/v1, LLM_MODEL=&lt;ollama tag&gt;
#    LM Studio:  start the local server  -> LLM_BASE_URL=http://localhost:1234/v1

# 2. Point the app at it (or put these in .env)
export LLM_PROVIDER=openai_compatible
export LLM_BASE_URL=http://localhost:8080/v1
export LLM_MODEL=my-model           # required; `curl $LLM_BASE_URL/models` lists names
# export LLM_API_KEY=...            # only if your server checks a key; a dummy is sent otherwise
# export LLM_MAX_TOKENS=8192        # optional; raise it for "thinking" models
# export LLM_TIMEOUT=600            # optional, seconds (default 300)
streamlit run app.py
# generation + faithfulness judge both use the LLM_* vars:
# python -m eval.run_faithfulness</code></pre>

<ul>
  <li><strong>Not benchmarked locally.</strong> Retrieval numbers (Hit@k, MRR) do not depend on the LLM at all. Embeddings and the reranker already run locally. Answer quality does depend on the model, so measure your local model with <code>python -m eval.run_faithfulness</code> before quoting anything.</li>
  <li><strong>Thinking models.</strong> Reasoning tokens count against the output cap. llama-server normally returns them in a separate <code>reasoning_content</code> field, and the app strips any <code>&lt;think&gt;…&lt;/think&gt;</code> block left in the answer. If replies come back empty or cut off, raise <code>LLM_MAX_TOKENS</code> or turn thinking off (for example <code>llama-server --reasoning-budget 0</code>).</li>
  <li><strong>Plain prompt, no tools.</strong> RAG generation is a single prompt per question, so it is the least sensitive of the three apps to the model choice. Citations and the "I don't know" refusal are still prompt instructions, and smaller models follow them less reliably.</li>
  <li><strong>Judge override.</strong> <code>OPENAI_BASE_URL</code>, <code>OPENAI_API_KEY</code> and <code>JUDGE_MODEL</code> still work as judge-only overrides (for example, generate locally and judge with a different model).</li>
  <li><strong>Hosted demo.</strong> An app on Streamlit Cloud cannot reach <code>localhost</code> on your PC. Use local mode when you run the app on your own machine.</li>
</ul>

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
│   ├── retriever.py                # Hybrid / MMR / similarity + OOS gates
│   ├── reranker.py                 # Optional ms-marco MiniLM cross-encoder
│   ├── llm.py                      # Provider switch: Groq gpt-oss-120b (default) or OpenAI-compatible
│   └── chain.py                    # End-to-end RAG with citation + refuse prompt
├── eval/
│   ├── gold_qa.json                # 24 labelled questions on 2 arXiv PDFs
│   ├── run_eval.py                 # Hit@k + MRR ± rerank (no Groq key)
│   ├── faithfulness.py             # LLM-as-judge helpers (OpenAI-compatible)
│   ├── run_faithfulness.py         # Answer groundedness + OOS refuse eval
│   ├── results.md                  # Measured Hit@8 / MRR table
│   ├── results.json                # Machine-readable results
│   └── figures/
│       └── hit_at_8.png            # Bar chart of retrieval method comparison
├── tests/
│   ├── conftest.py                 # Shared fixtures
│   ├── test_loader.py              # PDF extraction tests (synthetic sample PDFs)
│   ├── test_chunker.py             # Chunk ID stability + overlap tests
│   ├── test_retriever.py           # Hybrid retrieval + clear / replace-on-reingest
│   ├── test_gold.py                # Gold file + config validation
│   └── test_chain_prompt.py        # Prompt rules validation
├── data/
│   ├── sample_pdfs/                # Tiny synthetic fixtures for CI (see data/README.md)
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
  <li><strong>Hit@8 is retrieval-only.</strong> It measures whether the right page appears in the top-8 chunks — not whether the LLM's answer is correct. Answer faithfulness is a separate script (<code>python -m eval.run_faithfulness</code>) against any OpenAI-compatible endpoint; it is <strong>not run in CI</strong> and was <strong>not run against paid APIs</strong> for this commit (see placeholder note in <code>eval/</code>).</li>
  <li><strong>Hybrid (+rerank) still misses 5 in-scope questions</strong> on this gold set (tables / obscure lines). MRR improved; Hit@8 on hybrid stayed 17/22.</li>
  <li><strong>Reranker is optional and CPU-sized</strong> (ms-marco-MiniLM-L-6-v2). If the model fails to load, the app fails open to unre-ranked hybrid. Toggle in the Streamlit sidebar; <code>use_reranker</code> on <code>POST /ask</code>.</li>
  <li><strong>OOS refusal needs the cross-encoder path</strong> (CE logit floor). Without rerank, hybrid alone still returns chunks for the 2 OOS questions (0/2); with rerank it is 2/2.</li>
  <li><strong>Streamlit Cloud is ephemeral.</strong> The vector DB doesn't persist across reboots — users re-upload PDFs on each session. Prefer leaving rerank off on very small Cloud instances if memory is tight.</li>
  <li><strong>Not a hosted document product.</strong> This is a portfolio RAG, not a production system. No auth, no rate limiting, no monitoring, no persistence layer.</li>
</ul>

<h2>Status</h2>

<p>✅ <strong>Live</strong> — deployed on Streamlit Community Cloud. Auto-redeploys on every push to main.</p>

<h2>License</h2>

<p>MIT</p>
