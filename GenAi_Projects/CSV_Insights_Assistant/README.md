<h1>CSV Insights Assistant</h1>

<p>
  <img src="https://img.shields.io/badge/python-3.11-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python 3.11">
  <img src="https://img.shields.io/badge/langgraph-1A1A2E?style=flat-square&logo=langchain&logoColor=white" alt="LangGraph">
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas">
  <img src="https://img.shields.io/badge/DuckDB-FFF000?style=flat-square&logo=duckdb&logoColor=black" alt="DuckDB">
  <img src="https://img.shields.io/badge/groq-F55036?style=flat-square&logo=groq&logoColor=white" alt="Groq">
  <img src="https://img.shields.io/badge/streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/fastapi-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <a href="https://github.com/MacAns-117/Projects/actions/workflows/genai-tests.yml"><img src="https://github.com/MacAns-117/Projects/actions/workflows/genai-tests.yml/badge.svg" alt="GenAI tests"></a>
  <a href="https://portfolio-wtvyr5raavdyaknbh4jml6.streamlit.app/"><img src="https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Live Demo"></a>
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<blockquote><em>Ask plain-English questions about a CSV and get answers computed with pandas or DuckDB SQL, plus a Plotly chart when you ask for one.</em></blockquote>

<hr>

<h2>Overview</h2>

<p>Can a small tool-calling graph answer questions about whatever table you load, not a hard-coded hotel schema? Numbers in the answer come from tool output (pandas or SQL), not the model's memory, and charts are Plotly figures drawn in the UI.</p>

<p>The default file is the Antonio / Almeida / Nunes hotel demand table (arrivals July 2015 – August 2017). Upload another CSV and the schema card and tools switch to its columns. This is a portfolio assistant, not a hosted BI product.</p>

<hr>

<h2>Live demo</h2>

<p><a href="https://portfolio-wtvyr5raavdyaknbh4jml6.streamlit.app/">portfolio-wtvyr5raavdyaknbh4jml6.streamlit.app</a></p>

<p>The hotel sample loads by default, or upload any CSV and ask questions. No login required.</p>

<hr>

<h2>What it does</h2>

<ul>
  <li>Loads one CSV (upload, or the hotel sample).</li>
  <li>Builds a schema card (dtype, nunique, example values) and injects it into the agent prompt.</li>
  <li>LangGraph router: <code>data</code> / <code>viz</code> / <code>both</code> / <code>general</code>.</li>
  <li>Analyst tools: filter, aggregate, value counts, stats, segment compare, correlation, read-only SQL on table <code>data</code>.</li>
  <li>Viz tools write a Plotly figure into a chart buffer; Streamlit draws that figure.</li>
  <li>Report writer summarizes only the tool output.</li>
  <li>FastAPI wrapper: <code>GET /health</code>, <code>GET /schema</code>, <code>POST /ingest</code>, <code>POST /ask</code>.</li>
</ul>

<pre><code>User → Router → Data analyst (pandas / DuckDB)
                 ↘ Viz agent (Plotly) → Report writer → chat + chart
</code></pre>

<hr>

<h2>Results</h2>

<p>Facts on the default hotel table, checked against pandas by <code>python -m eval.run_eval</code> (no API key):</p>

<table>
  <thead><tr><th>Fact</th><th>Value</th></tr></thead>
  <tbody>
    <tr><td>Clean rows</td><td>87,230 (from 119,390 raw)</td></tr>
    <tr><td>Cancellation rate</td><td>27.52%</td></tr>
    <tr><td>City vs Resort cancel</td><td>30.10% vs 23.48%</td></tr>
    <tr><td>Mean lead time (canceled / stayed)</td><td>105.7 / 70.2 days</td></tr>
    <tr><td>Busiest arrival month</td><td>August (11,242)</td></tr>
    <tr><td>corr(lead_time, is_canceled)</td><td>0.1845</td></tr>
    <tr><td>Pandas gold checks</td><td>19/19 (20 questions; the capabilities question has no numeric check)</td></tr>
    <tr><td>Unit tests (<code>python -m pytest tests/ -q</code>, no API keys)</td><td>88 passed (run 27 Oct 2026 on the merged code)</td></tr>
  </tbody>
</table>

<p>Full table: <a href="eval/results.md"><code>eval/results.md</code></a>. Optional <code>--llm</code> runs the graph end to end; it needs an LLM, is a phrase check rather than a faithfulness score, and has not been run for the published results.</p>

<hr>

<h2>Tech stack</h2>

<table>
  <thead>
    <tr><th>Layer</th><th>Tools</th></tr>
  </thead>
  <tbody>
    <tr><td>Language</td><td>Python 3.11</td></tr>
    <tr><td>Orchestration</td><td>LangGraph (router + tool-calling agents), LangChain</td></tr>
    <tr><td>LLM</td><td>Groq <code>openai/gpt-oss-120b</code> (default) or any OpenAI-compatible server (llama.cpp, Ollama, LM Studio)</td></tr>
    <tr><td>Data tools</td><td>pandas, NumPy, DuckDB (read-only, in-memory SQL)</td></tr>
    <tr><td>Charts</td><td>Plotly</td></tr>
    <tr><td>Web UI</td><td>Streamlit</td></tr>
    <tr><td>REST API</td><td>FastAPI (/health, /schema, /ingest, /ask)</td></tr>
    <tr><td>Eval / tests</td><td>Pandas gold checks (<code>eval/run_eval.py</code>), pytest (88 tests, no API keys) in GitHub Actions</td></tr>
    <tr><td>Deployment</td><td>Streamlit Community Cloud</td></tr>
  </tbody>
</table>

<hr>

<h2>How to run</h2>

<pre><code>git clone https://github.com/MacAns-117/Projects.git
cd Projects/GenAi_Projects/CSV_Insights_Assistant

python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
cp .env.example .env               # then set GROQ_API_KEY (or use a local model, below)

streamlit run app.py
# uvicorn api:app --reload         # optional API: /health /schema /ingest /ask
python -m eval.run_eval            # pandas gold checks, no API key
python -m pytest tests/ -q         # no API keys
</code></pre>

<p>Upload <code>data/sample_sales.csv</code> in the sidebar to try a table with no hotel columns.</p>

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
streamlit run app.py
# python -m eval.run_eval --llm      # router/answer phrase check against your local model</code></pre>

<ul>
  <li>Not benchmarked locally. The table figures above come from pandas and do not use an LLM. The optional <code>--llm</code> phrase check has not been run against a local model in this repo.</li>
  <li>Thinking models. Reasoning tokens count against the output cap. llama-server normally returns them in a separate <code>reasoning_content</code> field, and the app strips any <code>&lt;think&gt;…&lt;/think&gt;</code> block left in the answer. If replies come back empty or cut off, raise <code>LLM_MAX_TOKENS</code> or turn thinking off (for example <code>llama-server --reasoning-budget 0</code>).</li>
  <li>Tool calling. The data analyst and the chart agent depend on OpenAI-style tool calls. Your server must support <code>tools</code> (llama.cpp with Jinja templates, recent Ollama and LM Studio do, if the model's chat template supports tools). Smaller local models are more likely to pick the wrong column, send malformed arguments, or stop after the 6-step limit. Tool errors go back to the model as text, so a bad call does not crash the turn, but the answer can come back incomplete.</li>
  <li>Router. The router expects one word (<code>data</code>/<code>viz</code>/<code>both</code>/<code>general</code>). Anything else falls back to <code>data</code>.</li>
  <li>Hosted demo. An app on Streamlit Cloud cannot reach <code>localhost</code> on your PC. Use local mode when you run the app on your own machine.</li>
</ul>

<hr>

<h2>Project structure</h2>

<pre><code>CSV_Insights_Assistant/
├── app.py                     # Streamlit UI (upload, chat, charts)
├── api.py                     # FastAPI wrapper
├── src/
│   ├── config.py              # model, caps, paths
│   ├── llm.py                 # Groq (default) or OpenAI-compatible provider switch
│   ├── schema.py              # runtime schema card
│   ├── data_loader.py         # any CSV; hotel guest heuristic only if those cols exist
│   ├── routing.py             # data / viz / both / general
│   ├── orchestrator.py        # LangGraph graph
│   ├── chart_buffer.py        # Plotly side-channel (tools return strings)
│   ├── memory.py              # sliding window of turns
│   ├── tools/                 # pandas query + stats, DuckDB SQL, Plotly viz
│   └── agents/                # data analyst, viz agent, report writer
├── eval/
│   ├── gold_questions.json    # 20 questions; no year outside 2015–2017
│   ├── run_eval.py            # pandas checks (+ optional --llm)
│   └── results.md / results.json
├── tests/                     # 88 tests, no paid keys
├── data/
│   ├── hotel_bookings.csv     # default sample (see data/README.md)
│   ├── sample_sales.csv       # 10-row second schema
│   └── README.md
├── .env.example               # variable names only, no secrets
├── requirements.txt
├── pytest.ini
└── LICENSE                    # MIT
</code></pre>

<hr>

<h2>Limitations</h2>


<ul>
  <li>One table per session. No joins across files, no warehouse.</li>
  <li>Caps: 50 MB / 200k rows on load; SQL result 200 rows; chart 5,000 points.</li>
  <li>SQL is read-only SELECT/WITH on in-memory DuckDB. No persistence.</li>
  <li>Cleaning is light. Exact duplicate drop. All-zero guest rows dropped only when <code>adults</code>, <code>children</code>, and <code>babies</code> are all present. Other CSVs are left as-is besides unnamed index columns and obvious date parse.</li>
  <li>Follow-ups are previous turns pasted onto the next question. Restart clears them.</li>
  <li>Charts: last figure of the turn is shown. The API returns <code>has_chart</code> + a caption, not a PNG.</li>
  <li>Eval without <code>--llm</code> checks pandas facts, not whether Groq cited them.</li>
  <li>Chat needs an LLM: a Groq key, or a local OpenAI-compatible server. Tests and the pandas eval need neither.</li>
</ul>

<hr>

<h2>License</h2>

<p>Code is MIT (<a href="LICENSE"><code>LICENSE</code></a>). Hotel data: Antonio, Almeida &amp; Nunes, <em>Hotel booking demand datasets</em>, Scientific Data (2019). See <a href="data/README.md"><code>data/README.md</code></a>.</p>
