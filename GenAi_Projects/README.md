<h1>GenAI Projects</h1>

<p>
  <img src="https://img.shields.io/badge/projects-2-blue?style=flat-square" alt="2 projects">
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/langchain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" alt="LangChain">
  <img src="https://img.shields.io/badge/langgraph-1A1A2E?style=flat-square&logo=langchain&logoColor=white" alt="LangGraph">
  <img src="https://img.shields.io/badge/chromadb-FF6F00?style=flat-square&logo=chroma&logoColor=white" alt="ChromaDB">
  <img src="https://img.shields.io/badge/groq-F55036?style=flat-square&logo=groq&logoColor=white" alt="Groq">
  <img src="https://img.shields.io/badge/streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<blockquote><em>Two GenAI apps — PDF question-answering with citations, and a LangGraph CSV analyst. Each folder has its own README with numbers and how to run it.</em></blockquote>

<hr>

<h2>What's in here</h2>

<p>Two small projects I keep in one place:</p>

<table>
  <thead>
    <tr>
      <th>Folder</th>
      <th>What it is</th>
      <th>Headline</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="Rag_Document_QA/"><code>Rag_Document_QA</code></a></td>
      <td>Ask questions over uploaded PDFs</td>
      <td>Hybrid retrieval, Hit@8 <strong>77.3%</strong> (17/22)</td>
    </tr>
    <tr>
      <td><a href="CSV_Insights_Assistant/"><code>CSV_Insights_Assistant</code></a></td>
      <td>Ask questions over one CSV</td>
      <td>Hotel sample <strong>87,230</strong> rows, pandas gold <strong>19/19</strong></td>
    </tr>
  </tbody>
</table>

<p>Each folder has its own README with numbers, eval, and how to run it. Both need a Groq key for chat; retrieval/pandas eval does not.</p>

<hr>

<h2>Multi-doc RAG Q&A</h2>

<p>Upload 1–10 PDFs, chunk them (1000 / 200), embed with MiniLM, store in Chroma. Questions go through hybrid search (BM25 + vector cosine, weight 0.6), then Groq writes an answer with filename + page citations. OCR (Tesseract) is the fallback for scanned pages. Streamlit UI plus FastAPI <code>/health</code> <code>/ingest</code> <code>/ask</code>.</p>

<p>Gold set: 24 questions (22 in-scope, 2 out-of-scope) on two public arXiv papers (Vaswani <em>Attention Is All You Need</em> and Lewis <em>RAG</em>).</p>

<table>
  <thead>
    <tr><th>Method</th><th>Hit@8</th><th>Hits</th></tr>
  </thead>
  <tbody>
    <tr><td>Cosine (MiniLM only)</td><td>59.1%</td><td>13/22</td></tr>
    <tr><td>MMR</td><td>68.2%</td><td>15/22</td></tr>
    <tr><td><strong>Hybrid (BM25 + vector)</strong></td><td><strong>77.3%</strong></td><td><strong>17/22</strong></td></tr>
  </tbody>
</table>

<p>Hit@8 = the gold page shows up in the top-8 chunks. It is <strong>not</strong> whether the LLM sentence is correct. Hybrid still misses 6 in-scope items (tables and author lines). The two out-of-scope questions still retrieve chunks — the 0.22 score floor is not a refuse gate. Streamlit Cloud wipes the vector store on reboot.</p>

<p>Live demo: <a href="https://projects-wktkeuxu6u3nqmz9vdyith.streamlit.app/">projects-wktkeuxu6u3nqmz9vdyith.streamlit.app</a></p>

<pre><code>cd Rag_Document_QA
python -m pip install -r requirements.txt
cp .env.example .env          # GROQ_API_KEY=
streamlit run app.py
python -m eval.run_eval
python -m pytest tests/ -q</code></pre>

<p>Stack: LangChain, Chroma, sentence-transformers, rank-bm25, pdfplumber, Tesseract, Groq, Streamlit, FastAPI.</p>

<hr>

<h2>CSV Insights Assistant</h2>

<p>LangGraph router (<code>data</code> / <code>viz</code> / <code>both</code> / <code>general</code>) over <strong>whatever CSV is loaded</strong>. Tools: pandas filter / aggregate / stats / compare / correlation, plus read-only DuckDB SQL on table <code>data</code>. Viz writes a Plotly figure into a buffer; Streamlit draws that figure. Schema card (dtypes, nunique, examples) is injected at runtime so the prompt is not hard-coded to hotel columns.</p>

<p>Default sample is the Antonio / Almeida / Nunes hotel demand table (arrivals <strong>July 2015 – August 2017</strong>). 119,390 raw → <strong>87,230</strong> after exact dups and all-zero guest rows. Upload another CSV (or <code>data/sample_sales.csv</code>) and the tools follow those columns.</p>

<table>
  <thead>
    <tr><th>Fact (hotel sample)</th><th>Value</th></tr>
  </thead>
  <tbody>
    <tr><td>Clean rows</td><td>87,230</td></tr>
    <tr><td>Cancellation rate</td><td>27.52%</td></tr>
    <tr><td>City vs Resort cancel</td><td>30.10% vs 23.48%</td></tr>
    <tr><td>Mean lead time (canceled / stayed)</td><td>105.7 / 70.2 days</td></tr>
    <tr><td>Busiest arrival month</td><td>August (11,242)</td></tr>
    <tr><td>Pandas gold checks</td><td><strong>19/19</strong></td></tr>
  </tbody>
</table>

<p>One table per session. Caps: 50 MB / 200k rows, SQL 200 rows, chart 5,000 points. Follow-ups are previous turns pasted onto the next question. Pandas eval does not need Groq; <code>--llm</code> is a phrase check, not faithfulness.</p>

<pre><code>cd CSV_Insights_Assistant
python -m pip install -r requirements.txt
cp .env.example .env          # GROQ_API_KEY=
streamlit run app.py
python -m eval.run_eval
python -m pytest tests/ -q</code></pre>

<p>Stack: LangGraph, pandas, DuckDB, Plotly, Groq, Streamlit, FastAPI.</p>

<hr>

<h2>Tech stack across both</h2>

<table>
  <thead>
    <tr><th>Layer</th><th>Tools</th></tr>
  </thead>
  <tbody>
    <tr><td>Language</td><td>Python 3.11</td></tr>
    <tr><td>LLM</td><td>Groq <code>openai/gpt-oss-120b</code></td></tr>
    <tr><td>Orchestration</td><td>LangChain (RAG) · LangGraph (CSV)</td></tr>
    <tr><td>Unstructured</td><td>pdfplumber, Chroma, MiniLM, BM25, Tesseract</td></tr>
    <tr><td>Structured</td><td>pandas, DuckDB, Plotly</td></tr>
    <tr><td>UI / API</td><td>Streamlit, FastAPI</td></tr>
    <tr><td>Eval / tests</td><td>gold JSON + pytest (no key for retrieval/pandas eval)</td></tr>
  </tbody>
</table>

<hr>

<h2>Layout</h2>

<pre><code>README.md                         this file
Rag_Document_QA/                  PDF Q&A + citations
CSV_Insights_Assistant/           LangGraph CSV analyst</code></pre>

<p>Open a folder and use that README to run it. This file is only the index.</p>

<hr>

<h2>License</h2>

<p>Code is MIT unless a child README says otherwise. PDFs are public arXiv papers. Hotel rows: Antonio, Almeida & Nunes, Scientific Data (2019) — see each <code>data/README.md</code>.</p>
