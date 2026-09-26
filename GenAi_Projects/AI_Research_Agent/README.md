<h1>AI Research Agent</h1>

<p>
  <img src="https://img.shields.io/badge/python-3.11-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python 3.11">
  <img src="https://img.shields.io/badge/langgraph-1A1A2E?style=flat-square&logo=langchain&logoColor=white" alt="LangGraph">
  <img src="https://img.shields.io/badge/groq-F55036?style=flat-square&logo=groq&logoColor=white" alt="Groq">
  <img src="https://img.shields.io/badge/tavily-1A1A1A?style=flat-square" alt="Tavily">
  <img src="https://img.shields.io/badge/streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/fastapi-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/tests-30%20passed-2ea44f?style=flat-square" alt="30 passed">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<blockquote><em>Ask a question. It searches the web, reads the pages, and writes a cited report. A follow-up in the Streamlit chat is sent in as context.</em></blockquote>

<hr>

<h2>The question</h2>

<p>I wanted a research helper that is not stuck on one dataset. You type a question. It should look it up, keep the pages, and say where each claim came from. If I ask a follow-up in the same chat, the planner and the report writer should still see what was just said.</p>

<p>This is a local app. It is not a public search service.</p>

<hr>

<h2>What it does</h2>

<p>The graph is one straight line. It does not search again if the first pass is thin.</p>

<pre><code>question (+ chat context in Streamlit)
    → Planner          3–5 search queries
    → Searcher         Tavily, then read the page, then a short summary
    → Synthesizer      what the pages agree on, and where they do not
    → Report writer    Markdown with [1], [2]
    → END
</code></pre>

<ul>
  <li>If the planner returns nothing, the query list falls back to the question itself.</li>
  <li>Page text comes from trafilatura. A failed extract keeps the search snippet instead of dropping the hit.</li>
  <li>Fetches are http/https only. Private, loopback, and link-local addresses are refused, and the body is capped at 2 MiB.</li>
  <li>Streamlit stores the chat and passes it in as <code>context</code>. <strong>Clear Conversation</strong> in the sidebar wipes that.</li>
  <li>The API runs the same graph with an empty context. It listens on <code>127.0.0.1</code>. <code>POST /research</code> needs header <code>X-API-Token</code> matching <code>RESEARCH_API_TOKEN</code>. If that token is unset, the route is allowed only when <code>RESEARCH_DEV=1</code>. Otherwise it returns 503. A wrong token returns 401.</li>
</ul>

<hr>

<h2>Numbers I actually measured</h2>

<table>
  <thead>
    <tr><th>Check</th><th>Result</th></tr>
  </thead>
  <tbody>
    <tr><td><code>RESEARCH_DEV=1 python -m pytest tests/ -q</code></td><td><strong>30 passed</strong></td></tr>
    <tr><td><code>python -m eval.run_eval --mock</code></td><td><strong>15/15</strong> scorer smoke</td></tr>
    <tr><td>Live run of the 15 gold questions</td><td>Not run</td></tr>
  </tbody>
</table>

<p>The 30 tests do not call Groq or Tavily. They cover config, the planner fallback, the memory window, extract URL blocks, and the API auth matrix (503 / 401 / 200). The 15/15 line only proves the scorer and <code>eval/gold_questions.json</code> load. It is not a web-accuracy percent.</p>

<p>Live eval is <code>python -m eval.run_eval</code>. That is about 15 full pipelines, 100+ API calls, and 30–60 minutes. Skip it unless you accept the Groq and Tavily cost. Without keys, that command skips instead of failing.</p>

<hr>

<h2>How to run</h2>

<pre><code>python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
cp .env.example .env               # GROQ_API_KEY, TAVILY_API_KEY
                                   # RESEARCH_API_TOKEN if you use the API

streamlit run app.py

# API, local, no token:
RESEARCH_DEV=1 uvicorn api:app --host 127.0.0.1 --port 8000

# API, with a token:
# RESEARCH_API_TOKEN=secret uvicorn api:app --host 127.0.0.1 --port 8000
# curl -H "X-API-Token: secret" -H "Content-Type: application/json" \
#   -d '{"question":"What is LangGraph?"}' http://127.0.0.1:8000/research

RESEARCH_DEV=1 python -m pytest tests/ -q
python -m eval.run_eval --mock
</code></pre>

<p>Docs for the API: <a href="http://127.0.0.1:8000/docs">http://127.0.0.1:8000/docs</a>. Do not commit a real <code>.env</code>. CI refuses one.</p>

<hr>

<h2>Layout</h2>

<pre><code>AI_Research_Agent/
├── app.py                         Streamlit
├── api.py                         FastAPI /health and /research
├── src/
│   ├── config.py                  keys, model, limits
│   ├── orchestrator.py            LangGraph, linear
│   ├── memory.py                  sliding window of turns
│   ├── agents/                    planner, searcher, synthesizer, report writer
│   └── tools/                     Tavily, extract, summarize
├── eval/gold_questions.json       15 questions
├── tests/                         30 tests, no paid keys
└── .github/workflows/ci.yml       Python 3.11, pytest
</code></pre>

<hr>

<h2>Limits</h2>

<ul>
  <li><strong>One pass.</strong> The graph does not plan again when it has few sources. A thin web result still becomes the report.</li>
  <li><strong>Follow-ups are Streamlit-only.</strong> The chat context goes to the planner and the report writer. <code>POST /research</code> sends an empty context, so the API does not remember the last call.</li>
  <li><strong>The whole report is stored in memory.</strong> A long chat makes the next prompt large. Clear the conversation when that happens.</li>
  <li><strong>Page text is trafilatura.</strong> A site that only renders in the browser comes back as a snippet.</li>
  <li><strong>Streamlit can show the raw error string.</strong> The API does not. A failed research call returns a generic 500 and the detail stays in the server log.</li>
  <li><strong>The token check is a plain string compare.</strong> Enough for a local app. Not a reason to expose the port.</li>
  <li><strong>No live accuracy number.</strong> Do not quote one until <code>python -m eval.run_eval</code> has been run and the results file is in front of you.</li>
  <li>Search and the model need your own keys. This folder does not ship a <code>.env</code>.</li>
</ul>

<hr>

<h2>License</h2>

<p>Code is MIT. Tavily and Groq are their own services.</p>
