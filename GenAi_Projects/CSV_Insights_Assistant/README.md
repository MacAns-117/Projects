<h1>CSV Insights Assistant</h1>

<p>
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/langgraph-1A1A2E?style=flat-square&logo=langchain&logoColor=white" alt="LangGraph">
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas">
  <img src="https://img.shields.io/badge/DuckDB-FFF000?style=flat-square&logo=duckdb&logoColor=black" alt="DuckDB">
  <img src="https://img.shields.io/badge/groq-F55036?style=flat-square&logo=groq&logoColor=white" alt="Groq">
  <img src="https://img.shields.io/badge/streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<blockquote><em>LangGraph analytics over one CSV at a time — pandas + DuckDB tools, Plotly charts that actually render, hotel bookings as the default sample.</em></blockquote>

<hr>

<h2>The question</h2>

<p>Can a small tool-calling graph answer questions about <strong>whatever table you load</strong>, not a hard-coded hotel schema?</p>

<p>Default file is the Antonio / Almeida / Nunes hotel demand table (arrivals <strong>July 2015 – August 2017</strong>). After dropping exact duplicates and all-zero guest rows: <strong>87,230</strong> bookings, <strong>27.52%</strong> canceled. Upload another CSV and the schema card + tools switch to those columns.</p>

<p>This is a portfolio assistant, not a hosted BI product.</p>

<hr>

<h2>Live Demo</h2>

<p>🔗 <strong><a href="https://portfolio-wtvyr5raavdyaknbh4jml6.streamlit.app/">portfolio-wtvyr5raavdyaknbh4jml6.streamlit.app</a></strong></p>

<p>Try it now — the hotel sample loads by default, or upload any CSV and ask questions. No login required.</p>

<h2>What it does</h2>

<ul>
  <li>Loads one CSV (upload, or the hotel sample).</li>
  <li>Builds a schema card (dtype, nunique, example values) and injects it into the agent prompt.</li>
  <li>LangGraph router: <code>data</code> / <code>viz</code> / <code>both</code> / <code>general</code>.</li>
  <li>Analyst tools: filter, aggregate, value counts, stats, segment compare, correlation, read-only SQL on table <code>data</code>.</li>
  <li>Viz tools write a Plotly figure into a chart buffer; Streamlit draws that figure (not a “chart generated” caption).</li>
  <li>Report writer summarizes only the tool output.</li>
</ul>

<pre><code>User → Router → Data analyst (pandas / DuckDB)
                 ↘ Viz agent (Plotly) → Report writer → chat + chart
</code></pre>

<hr>

<h2>Numbers on the default table</h2>

<table>
  <thead><tr><th>Fact</th><th>Value</th></tr></thead>
  <tbody>
    <tr><td>Clean rows</td><td>87,230 (from 119,390 raw)</td></tr>
    <tr><td>Cancellation rate</td><td>27.52%</td></tr>
    <tr><td>City vs Resort cancel</td><td>30.10% vs 23.48%</td></tr>
    <tr><td>Mean lead time (canceled / stayed)</td><td>105.7 / 70.2 days</td></tr>
    <tr><td>Busiest arrival month</td><td>August (11,242)</td></tr>
    <tr><td>corr(lead_time, is_canceled)</td><td>0.1845</td></tr>
    <tr><td>Pandas gold checks</td><td>19/19 (see <code>eval/results.md</code>)</td></tr>
  </tbody>
</table>

<p>Those figures are computed in <code>python -m eval.run_eval</code> (no API key). Optional <code>--llm</code> runs the graph; that path needs Groq and is a phrase check, not faithfulness.</p>

<hr>

<h2>How to run</h2>

<pre><code>python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
cp .env.example .env               # then set GROQ_API_KEY

streamlit run app.py
# uvicorn api:app --reload         # optional  /health /schema /ingest /ask
python -m eval.run_eval
python -m pytest tests/ -q
</code></pre>

<p>Try <code>data/sample_sales.csv</code> in the sidebar if you want a table with no hotel columns.</p>

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
streamlit run app.py
# python -m eval.run_eval --llm      # router/answer phrase check against your local model</code></pre>

<ul>
  <li><strong>Not benchmarked locally.</strong> The table figures above come from pandas and do not use an LLM. The optional <code>--llm</code> phrase check has not been run against a local model in this repo.</li>
  <li><strong>Thinking models.</strong> Reasoning tokens count against the output cap. llama-server normally returns them in a separate <code>reasoning_content</code> field, and the app strips any <code>&lt;think&gt;…&lt;/think&gt;</code> block left in the answer. If replies come back empty or cut off, raise <code>LLM_MAX_TOKENS</code> or turn thinking off (for example <code>llama-server --reasoning-budget 0</code>).</li>
  <li><strong>Tool calling.</strong> The data analyst and the chart agent depend on OpenAI-style tool calls. Your server must support <code>tools</code> (llama.cpp with Jinja templates, recent Ollama and LM Studio do, if the model's chat template supports tools). Smaller local models are more likely to pick the wrong column, send malformed arguments, or stop after the 6-step limit. Tool errors go back to the model as text, so a bad call does not crash the turn, but the answer can come back incomplete.</li>
  <li><strong>Router.</strong> The router expects one word (<code>data</code>/<code>viz</code>/<code>both</code>/<code>general</code>). Anything else falls back to <code>data</code>.</li>
  <li><strong>Hosted demo.</strong> An app on Streamlit Cloud cannot reach <code>localhost</code> on your PC. Use local mode when you run the app on your own machine.</li>
</ul>

<hr>

<h2>Layout</h2>

<pre><code>CSV_Insights_Assistant/
├── app.py
├── api.py
├── src/
│   ├── config.py
│   ├── schema.py              # runtime schema card
│   ├── data_loader.py         # any CSV; hotel guest heuristic only if those cols exist
│   ├── chart_buffer.py        # Plotly side-channel (tools return strings)
│   ├── orchestrator.py        # LangGraph
│   ├── memory.py              # sliding window of turns
│   ├── tools/                 # pandas + DuckDB + Plotly
│   └── agents/
├── eval/gold_questions.json   # 20 questions; no year outside 2015–2017
├── tests/
└── data/hotel_bookings.csv
</code></pre>

<hr>

<h2>Limits</h2>

<ul>
  <li><strong>One table per session.</strong> No joins across files, no warehouse.</li>
  <li><strong>Caps:</strong> 50 MB / 200k rows on load; SQL result 200 rows; chart 5,000 points.</li>
  <li><strong>SQL is read-only</strong> SELECT/WITH on in-memory DuckDB. No persistence.</li>
  <li><strong>Cleaning is light.</strong> Exact duplicate drop. All-zero guest rows dropped only when <code>adults</code>, <code>children</code>, and <code>babies</code> are all present. Other CSVs are left as-is besides unnamed index columns and obvious date parse.</li>
  <li><strong>Follow-ups</strong> are previous turns pasted onto the next question. Restart clears them.</li>
  <li><strong>Charts:</strong> last figure of the turn is shown. The API returns <code>has_chart</code> + a caption, not a PNG.</li>
  <li><strong>Eval without <code>--llm</code></strong> checks pandas facts, not whether Groq cited them.</li>
  <li>Needs a Groq key for chat. Tests and pandas eval do not.</li>
</ul>

<hr>

<h2>License</h2>

<p>Code is MIT. Hotel data: Antonio, Almeida & Nunes, Scientific Data (2019). See <code>data/README.md</code>.</p>
