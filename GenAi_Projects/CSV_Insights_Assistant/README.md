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

<h2>Layout</h2>

<pre><code>Hotel_Insights_Assistant/
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
