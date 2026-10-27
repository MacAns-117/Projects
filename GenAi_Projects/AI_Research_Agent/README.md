<h1>AI Research Agent</h1>

<p>
  <img src="https://img.shields.io/badge/python-3.11-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python 3.11">
  <img src="https://img.shields.io/badge/langgraph-1A1A2E?style=flat-square&logo=langchain&logoColor=white" alt="LangGraph">
  <img src="https://img.shields.io/badge/groq-F55036?style=flat-square&logo=groq&logoColor=white" alt="Groq">
  <img src="https://img.shields.io/badge/tavily-1A1A1A?style=flat-square" alt="Tavily">
  <img src="https://img.shields.io/badge/streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/fastapi-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <a href="https://github.com/MacAns-117/Projects/actions/workflows/genai-tests.yml"><img src="https://github.com/MacAns-117/Projects/actions/workflows/genai-tests.yml/badge.svg" alt="GenAI tests"></a>
  <a href="https://projects-4vtuq5ybps6g3rgyzg84ry.streamlit.app/"><img src="https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Live Demo"></a>
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<blockquote><em>Ask a question. It searches the web, reads the pages, and writes a report that cites each source as [1], [2]. A follow-up in the Streamlit chat sees the previous report.</em></blockquote>

<hr>

<h2>Overview</h2>

<p>I wanted a research helper that is not tied to one dataset. You type a question; it plans a few searches, reads the pages, and says where each claim came from. A follow-up in the same chat is sent to the planner and the report writer as context.</p>

<p>It runs as a local app or on Streamlit Cloud. It is not a public search service.</p>

<hr>

<h2>Live demo</h2>

<p><a href="https://projects-4vtuq5ybps6g3rgyzg84ry.streamlit.app/">projects-4vtuq5ybps6g3rgyzg84ry.streamlit.app</a> (Streamlit Community Cloud, no login).</p>

<hr>

<h2>What it does</h2>

<p>The LangGraph graph is one straight line. It does not search again if the first pass is thin.</p>

<pre><code>question (+ chat context in Streamlit)
    → Planner          3–5 search queries (JSON list)
    → Searcher         Tavily (5 results per query), read the page, short summary
    → Synthesizer      what the pages agree on, and where they do not
    → Report writer    Markdown with [1], [2]
    → END
</code></pre>

<ul>
  <li>If the planner returns nothing usable after one retry, it searches the question itself.</li>
  <li>Page text comes from trafilatura. A failed extract keeps the search snippet instead of dropping the hit.</li>
  <li>Fetches are http/https only. Private, loopback and link-local addresses are refused, and the body is capped at 2 MiB.</li>
  <li>Streamlit stores the chat and passes it in as <code>context</code>. <em>Clear Conversation</em> in the sidebar wipes it.</li>
  <li>The API (<code>GET /health</code>, <code>POST /research</code>) runs the same graph with an empty context and binds to <code>127.0.0.1</code>. <code>POST /research</code> needs an <code>X-API-Token</code> header matching <code>RESEARCH_API_TOKEN</code>. If that token is unset, the route works only with <code>RESEARCH_DEV=1</code> and returns 503 otherwise. A wrong token returns 401.</li>
</ul>

<hr>

<h2>Results</h2>

<table>
  <thead>
    <tr><th>Check</th><th>Result</th></tr>
  </thead>
  <tbody>
    <tr><td><code>RESEARCH_DEV=1 python -m pytest tests/ -q</code></td><td>70 passed (run 27 Oct 2026 on the merged code)</td></tr>
    <tr><td><code>python -m eval.run_eval --mock</code></td><td>15/15 scorer smoke test</td></tr>
    <tr><td>Live run of the 15 gold questions</td><td>Not run</td></tr>
  </tbody>
</table>

<p>The tests do not call Groq, Tavily or a local LLM server. They cover config, LLM provider selection, the planner fallback, the memory window, URL blocking in the extractor, and the API auth cases (503 / 401 / 200). The 15/15 line only shows that the scorer and <code>eval/gold_questions.json</code> load; it is not an accuracy figure.</p>

<p>The live eval is <code>python -m eval.run_eval</code>: 15 full pipelines, 100+ API calls, roughly 30–60 minutes of Groq and Tavily usage. Without keys it skips instead of failing.</p>

<hr>

<h2>Tech stack</h2>

<table>
  <thead>
    <tr><th>Layer</th><th>Tools</th></tr>
  </thead>
  <tbody>
    <tr><td>Language</td><td>Python 3.11</td></tr>
    <tr><td>Orchestration</td><td>LangGraph (linear 4-node graph), LangChain</td></tr>
    <tr><td>LLM</td><td>Groq <code>openai/gpt-oss-120b</code> (default) or any OpenAI-compatible server (llama.cpp, Ollama, LM Studio)</td></tr>
    <tr><td>Search / extraction</td><td>Tavily (<code>tavily-python</code>), trafilatura, requests</td></tr>
    <tr><td>Web UI</td><td>Streamlit</td></tr>
    <tr><td>REST API</td><td>FastAPI (/health, /research) with token auth</td></tr>
    <tr><td>Eval / tests</td><td>15-question gold file (<code>eval/run_eval.py</code>), pytest (70 tests, no API keys) in GitHub Actions</td></tr>
    <tr><td>Deployment</td><td>Streamlit Community Cloud</td></tr>
  </tbody>
</table>

<hr>

<h2>How to run</h2>

<pre><code>git clone https://github.com/MacAns-117/Projects.git
cd Projects/GenAi_Projects/AI_Research_Agent

python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
cp .env.example .env               # GROQ_API_KEY (or local LLM_*), TAVILY_API_KEY
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

<p>With the API running, interactive docs are at <code>http://127.0.0.1:8000/docs</code>. <code>.env</code> is gitignored; do not commit a real one.</p>

<hr>

<h2>Run with a local model (llama.cpp / Ollama / LM Studio)</h2>

<p>Groq is the default and nothing changes if you leave the <code>LLM_*</code> variables unset (the hosted demo keeps using Groq). Set <code>LLM_PROVIDER=openai_compatible</code> to send every chat call to any server that speaks the OpenAI Chat Completions API instead. The provider switch lives in <code>src/llm.py</code>.</p>

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
streamlit run app.py          # TAVILY_API_KEY is still needed for web search</code></pre>

<ul>
  <li>Not benchmarked locally. No live eval has been run with Groq or with a local model, so there are no accuracy numbers to compare.</li>
  <li>Thinking models. Reasoning tokens count against the output cap. llama-server normally returns them in a separate <code>reasoning_content</code> field, and the app strips any <code>&lt;think&gt;…&lt;/think&gt;</code> block left in the answer. If replies come back empty or cut off, raise <code>LLM_MAX_TOKENS</code> or turn thinking off (for example <code>llama-server --reasoning-budget 0</code>).</li>
  <li>Web search is not local. Tavily still does the searching and still needs <code>TAVILY_API_KEY</code>. Only the LLM calls move to your machine.</li>
  <li>Structured output. The planner asks for a JSON list of 3–5 queries. It retries once and then falls back to searching the raw question, so a weaker model degrades search breadth rather than crashing. The pipeline does not use tool calling.</li>
  <li>Context size. The synthesizer and report writer get several page summaries at once (report cap 4096 output tokens). Start llama-server with a large enough <code>-c</code> (for example 32768) or prompts get truncated or rejected.</li>
  <li>Hosted demo. An app on Streamlit Cloud cannot reach <code>localhost</code> on your PC. Use local mode when you run the app on your own machine.</li>
</ul>

<hr>

<h2>Project structure</h2>

<pre><code>AI_Research_Agent/
├── app.py                         # Streamlit chat
├── api.py                         # FastAPI /health and /research
├── src/
│   ├── config.py                  # keys, model, search limits
│   ├── llm.py                     # Groq (default) or OpenAI-compatible provider switch
│   ├── orchestrator.py            # LangGraph, linear
│   ├── memory.py                  # sliding window of turns
│   ├── agents/                    # planner, searcher, synthesizer, report writer
│   └── tools/                     # Tavily search, page extract, summarize
├── eval/
│   ├── gold_questions.json        # 15 questions
│   └── run_eval.py                # live run, or --mock scorer smoke test
├── tests/                         # 70 tests, no paid keys
├── .env.example                   # variable names only, no secrets
├── requirements.txt
└── LICENSE                        # MIT
</code></pre>

<p>CI for all three GenAI test suites: <a href="../../.github/workflows/genai-tests.yml"><code>.github/workflows/genai-tests.yml</code></a>.</p>

<hr>

<h2>Limitations</h2>


<ul>
  <li>One pass. The graph does not plan again when it has few sources. A thin web result still becomes the report.</li>
  <li>Follow-ups are Streamlit-only. The chat context goes to the planner and the report writer. <code>POST /research</code> sends an empty context, so the API does not remember the last call.</li>
  <li>The whole report is stored in memory. A long chat makes the next prompt large. Clear the conversation when that happens.</li>
  <li>Page text is trafilatura. A site that only renders in the browser comes back as a snippet.</li>
  <li>Streamlit can show the raw error string. The API does not. A failed research call returns a generic 500 and the detail stays in the server log.</li>
  <li>The token check is a plain string compare. Enough for a local app. Not a reason to expose the port.</li>
  <li>No live accuracy number. Do not quote one until <code>python -m eval.run_eval</code> has been run and the results file is in front of you.</li>
  <li>Search and the model need your own keys. This folder does not ship a <code>.env</code>.</li>
</ul>

<hr>

<h2>License</h2>

<p>Code is MIT (<a href="LICENSE"><code>LICENSE</code></a>). Tavily and Groq are separate services with their own terms.</p>
