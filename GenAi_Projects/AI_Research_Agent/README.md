<h1>AI Research Agent</h1>

<p>
  <img src="https://img.shields.io/badge/python-3.11-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python 3.11">
  <img src="https://img.shields.io/badge/langgraph-1A1A2E?style=flat-square&logo=langchain&logoColor=white" alt="LangGraph">
  <img src="https://img.shields.io/badge/groq-F55036?style=flat-square&logo=groq&logoColor=white" alt="Groq">
  <img src="https://img.shields.io/badge/tavily-1A1A1A?style=flat-square" alt="Tavily">
  <img src="https://img.shields.io/badge/streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/fastapi-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/tests-70%20passed-2ea44f?style=flat-square" alt="70 passed">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<blockquote><em>Ask a question. It searches the web, reads the pages, and writes a cited report. A follow-up in the Streamlit chat is sent in as context.</em></blockquote>

<hr>

<h2>The question</h2>

<p>I wanted a research helper that is not stuck on one dataset. You type a question. It should look it up, keep the pages, and say where each claim came from. If I ask a follow-up in the same chat, the planner and the report writer should still see what was just said.</p>

<p>This is a local app. It is not a public search service.</p>

<hr>

<h2>Live Demo</h2>

<p>🔗 <strong><a href="https://projects-4vtuq5ybps6g3rgyzg84ry.streamlit.app/">projects-4vtuq5ybps6g3rgyzg84ry.streamlit.app</a></strong></p>

<p>Try it now — ask a research question; the agent searches the web and writes a cited report. No login required. Uses your Streamlit secrets for Groq/Tavily.</p>

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
    <tr><td><code>RESEARCH_DEV=1 python -m pytest tests/ -q</code></td><td><strong>70 passed</strong></td></tr>
    <tr><td><code>python -m eval.run_eval --mock</code></td><td><strong>15/15</strong> scorer smoke</td></tr>
    <tr><td>Live run of the 15 gold questions</td><td>Not run</td></tr>
  </tbody>
</table>

<p>The 70 tests do not call Groq, Tavily or a local LLM server. They cover config, LLM provider selection (Groq default vs OpenAI-compatible), the planner fallback, the memory window, extract URL blocks, and the API auth matrix (503 / 401 / 200). The 15/15 line only proves the scorer and <code>eval/gold_questions.json</code> load. It is not a web-accuracy percent.</p>

<p>Live eval is <code>python -m eval.run_eval</code>. That is about 15 full pipelines, 100+ API calls, and 30–60 minutes. Skip it unless you accept the Groq and Tavily cost. Without keys, that command skips instead of failing.</p>

<hr>

<h2>How to run</h2>

<pre><code>python3.11 -m venv .venv
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

<p>Docs for the API: <a href="http://127.0.0.1:8000/docs">http://127.0.0.1:8000/docs</a>. Do not commit a real <code>.env</code>. CI refuses one.</p>

<hr>

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
streamlit run app.py          # TAVILY_API_KEY is still needed for web search</code></pre>

<ul>
  <li><strong>Not benchmarked locally.</strong> No live eval has been run with Groq or with a local model, so there are no accuracy numbers to compare.</li>
  <li><strong>Thinking models.</strong> Reasoning tokens count against the output cap. llama-server normally returns them in a separate <code>reasoning_content</code> field, and the app strips any <code>&lt;think&gt;…&lt;/think&gt;</code> block left in the answer. If replies come back empty or cut off, raise <code>LLM_MAX_TOKENS</code> or turn thinking off (for example <code>llama-server --reasoning-budget 0</code>).</li>
  <li><strong>Web search is not local.</strong> Tavily still does the searching and still needs <code>TAVILY_API_KEY</code>. Only the LLM calls move to your machine.</li>
  <li><strong>Structured output.</strong> The planner asks for a JSON list of 3–5 queries. It retries once and then falls back to searching the raw question, so a weaker model degrades search breadth rather than crashing. The pipeline does not use tool calling.</li>
  <li><strong>Context size.</strong> The synthesizer and report writer get several page summaries at once (report cap 4096 output tokens). Start llama-server with a large enough <code>-c</code> (for example 32768) or prompts get truncated or rejected.</li>
  <li><strong>Hosted demo.</strong> An app on Streamlit Cloud cannot reach <code>localhost</code> on your PC. Use local mode when you run the app on your own machine.</li>
</ul>

<hr>

<h2>Layout</h2>

<pre><code>AI_Research_Agent/
├── app.py                         Streamlit
├── api.py                         FastAPI /health and /research
├── .env.example                   Variable names only (no secrets)
├── LICENSE                        MIT
├── src/
│   ├── config.py                  keys, model, limits
│   ├── llm.py                     Groq (default) or OpenAI-compatible provider switch
│   ├── orchestrator.py            LangGraph, linear
│   ├── memory.py                  sliding window of turns
│   ├── agents/                    planner, searcher, synthesizer, report writer
│   └── tools/                     Tavily, extract, summarize
├── eval/gold_questions.json       15 questions
├── tests/                         70 tests, no paid keys
└── (repo) .github/workflows/genai-tests.yml   CI for all three GenAI suites
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
