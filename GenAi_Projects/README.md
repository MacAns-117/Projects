<h1>GenAI Projects</h1>

<p>
  <img src="https://img.shields.io/badge/python-3.11-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python 3.11">
  <img src="https://img.shields.io/badge/langchain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" alt="LangChain">
  <img src="https://img.shields.io/badge/langgraph-1A1A2E?style=flat-square&logo=langchain&logoColor=white" alt="LangGraph">
  <img src="https://img.shields.io/badge/chromadb-FF6F00?style=flat-square&logo=chroma&logoColor=white" alt="ChromaDB">
  <img src="https://img.shields.io/badge/groq-F55036?style=flat-square&logo=groq&logoColor=white" alt="Groq">
  <img src="https://img.shields.io/badge/streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/fastapi-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <a href="https://github.com/MacAns-117/Projects/actions/workflows/genai-tests.yml"><img src="https://github.com/MacAns-117/Projects/actions/workflows/genai-tests.yml/badge.svg" alt="GenAI tests"></a>
</p>

<p>Three LLM apps: PDF question answering with citations, a LangGraph analyst for any CSV, and a web research agent that writes a cited report. Each has a Streamlit UI, a FastAPI wrapper, a test suite that needs no API keys, and an eval script. Open a folder for details and run steps.</p>

<hr>

<h2>Projects</h2>

<table>
  <thead>
    <tr><th>Project</th><th>What it does</th><th>Measured</th><th>Demo</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="Rag_Document_QA/">Rag_Document_QA</a></td>
      <td>Answers questions over uploaded PDFs with file + page citations. Hybrid BM25 + vector retrieval, optional cross-encoder rerank, OCR fallback.</td>
      <td>Hit@8 77.3% (17/22), MRR 0.524, out-of-scope refused 2/2 · 62 tests</td>
      <td><a href="https://projects-wktkeuxu6u3nqmz9vdyith.streamlit.app/">Live</a></td>
    </tr>
    <tr>
      <td><a href="CSV_Insights_Assistant/">CSV_Insights_Assistant</a></td>
      <td>Answers questions about any loaded CSV with pandas and read-only DuckDB SQL tools, and draws Plotly charts.</td>
      <td>Pandas gold checks 19/19 on the hotel sample (87,230 rows) · 88 tests</td>
      <td><a href="https://portfolio-wtvyr5raavdyaknbh4jml6.streamlit.app/">Live</a></td>
    </tr>
    <tr>
      <td><a href="AI_Research_Agent/">AI_Research_Agent</a></td>
      <td>Plans searches, reads pages via Tavily + trafilatura, and writes a Markdown report citing [1], [2].</td>
      <td>70 tests · live 15-question eval not run</td>
      <td><a href="https://projects-4vtuq5ybps6g3rgyzg84ry.streamlit.app/">Live</a></td>
    </tr>
  </tbody>
</table>

<p>Test counts are from <code>python -m pytest tests/ -q</code> in each folder on 27 Oct 2026 (the research agent needs <code>RESEARCH_DEV=1</code>). CI runs all three suites without API keys: <a href="../.github/workflows/genai-tests.yml"><code>.github/workflows/genai-tests.yml</code></a>.</p>

<p>What the numbers mean:</p>

<ul>
  <li>RAG: retrieval only, on 24 gold questions (22 in-scope, 2 out-of-scope) over two arXiv papers. Hit@8 means the gold page is in the top 8 chunks; it does not grade the answer text. The faithfulness judge exists but has no published score. See <a href="Rag_Document_QA/eval/results.md"><code>Rag_Document_QA/eval/results.md</code></a>.</li>
  <li>CSV: the 19 checks compare pandas facts on the hotel table. The optional <code>--llm</code> run has not been done. See <a href="CSV_Insights_Assistant/eval/results.md"><code>CSV_Insights_Assistant/eval/results.md</code></a>.</li>
  <li>Research agent: <code>python -m eval.run_eval --mock</code> gives 15/15, which only shows the scorer loads. No live accuracy number exists yet.</li>
</ul>

<hr>

<h2>Tech stack</h2>

<table>
  <thead>
    <tr><th>Layer</th><th>Tools</th></tr>
  </thead>
  <tbody>
    <tr><td>Language</td><td>Python 3.11</td></tr>
    <tr><td>LLM</td><td>Groq <code>openai/gpt-oss-120b</code> by default; any OpenAI-compatible server (llama.cpp, Ollama, LM Studio) via <code>LLM_PROVIDER=openai_compatible</code></td></tr>
    <tr><td>Orchestration</td><td>LangChain (RAG), LangGraph (CSV, research agent)</td></tr>
    <tr><td>Retrieval</td><td>pdfplumber, Tesseract OCR, MiniLM embeddings, Chroma, rank-bm25, ms-marco MiniLM cross-encoder</td></tr>
    <tr><td>Structured data</td><td>pandas, DuckDB, Plotly</td></tr>
    <tr><td>Web research</td><td>Tavily, trafilatura</td></tr>
    <tr><td>UI / API</td><td>Streamlit, FastAPI</td></tr>
    <tr><td>Tests / CI</td><td>pytest, GitHub Actions</td></tr>
  </tbody>
</table>

<hr>

<h2>Running any of them</h2>

<pre><code>cd GenAi_Projects/&lt;project&gt;
python3.11 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env          # GROQ_API_KEY; the research agent also needs TAVILY_API_KEY
streamlit run app.py
python -m pytest tests/ -q    # no keys needed (research agent: RESEARCH_DEV=1)</code></pre>

<p>To use a local model instead of Groq, set <code>LLM_PROVIDER=openai_compatible</code>, <code>LLM_BASE_URL</code> and <code>LLM_MODEL</code>. Each README has a section on this, including what changes for tool calling and "thinking" models. The RAG retrieval eval, the CSV pandas eval and all unit tests need no LLM.</p>

<hr>

<h2>Layout</h2>

<pre><code>GenAi_Projects/
├── README.md                  # this index
├── Rag_Document_QA/           # PDF Q&amp;A with citations
├── CSV_Insights_Assistant/    # LangGraph CSV analyst
└── AI_Research_Agent/         # web research + cited report</code></pre>

<hr>

<h2>License</h2>

<p>Each app folder has an MIT <code>LICENSE</code>. Data: the RAG eval uses two public arXiv papers that you download yourself (<a href="Rag_Document_QA/data/README.md"><code>Rag_Document_QA/data/README.md</code></a>). The hotel sample is from Antonio, Almeida &amp; Nunes, Scientific Data (2019) (<a href="CSV_Insights_Assistant/data/README.md"><code>CSV_Insights_Assistant/data/README.md</code></a>). The research agent ships no dataset.</p>
