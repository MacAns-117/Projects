<h1>Ops Analytics and the August Engagement Drop</h1>

<p>
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas">
  <img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=sqlite&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/python--pptx-CB2B5A?style=flat-square" alt="python-pptx">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<blockquote><em>Two SQL ops-analytics case studies — job-review throughput and a metric-spike investigation on a 4-month user engagement window. Scored in both pandas and SQLite, with a short deck.</em></blockquote>

<hr>

<h2>The question</h2>

<p>Two SQL case studies from an ops-analytics assignment. I loaded the tables, answered the questions in <strong>pandas and SQLite</strong>, and put the numbers in a short deck.</p>

<p>This is a practice project. Case 1 is <strong>8 rows</strong>. I still ran every query the brief asked for, and I say in the write-up when a metric is too thin to trust.</p>

<h3>What I was asked</h3>

<p><strong>Case 1 — job review ops</strong> (<code>job_data</code>, Nov 2020)</p>

<ul>
  <li>Jobs reviewed per hour per day</li>
  <li>Throughput (events per second) and a 7-day rolling average</li>
  <li>Language share, last 30 days</li>
  <li>How to show duplicate rows</li>
</ul>

<p><strong>Case 2 — metric spike</strong> (users / events / email, May–Aug 2014)</p>

<ul>
  <li>Weekly user engagement</li>
  <li>User growth</li>
  <li>Weekly retention of the signup cohort</li>
  <li>Weekly engagement by device</li>
  <li>Email engagement</li>
</ul>

<hr>

<h2>Result (actual numbers)</h2>

<h3>Case 1</h3>

<p>After dropping three empty Excel rows: <strong>8 jobs, 6 days</strong> (25–30 Nov 2020). There is <strong>no time of day</strong>, so "per hour" is jobs / 24.</p>

<table>
  <thead>
    <tr>
      <th>Date</th>
      <th>Jobs</th>
      <th>Jobs / hour</th>
      <th>Events / second</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>25 Nov</td><td>1</td><td>0.0417</td><td>0.0000116</td></tr>
    <tr><td>26 Nov</td><td>1</td><td>0.0417</td><td>0.0000116</td></tr>
    <tr><td>27 Nov</td><td>1</td><td>0.0417</td><td>0.0000116</td></tr>
    <tr><td>28 Nov</td><td>2</td><td>0.0833</td><td>0.0000231</td></tr>
    <tr><td>29 Nov</td><td>1</td><td>0.0417</td><td>0.0000116</td></tr>
    <tr><td>30 Nov</td><td>2</td><td>0.0833</td><td>0.0000231</td></tr>
  </tbody>
</table>

<p>7-day rolling throughput (running mean, we only have 6 days): ends at <strong>0.0000154</strong> events/sec. I would <strong>not</strong> use the daily number on a sample this small — one extra job doubles it. Rolling is the better habit, but it needs more days than this file has.</p>

<p>Language share (the whole file <em>is</em> the last 30 days): <strong>Persian 37.5%</strong> (3/8), everything else 12.5% each.</p>

<p>Exact duplicate rows: <strong>none</strong>. <code>job_id</code> 23 shows up three times with different actors / events. That is a repeated job, not a copied row.</p>

<h3>Case 2</h3>

<p>Product events run <strong>1 May – 31 Aug 2014</strong>. 19,066 accounts, 9,381 activated (49.2%). 340,832 events, 90,389 email rows.</p>

<p>Weekly engagement = unique users with at least one <code>engagement</code> event. Weeks start Monday. The week of 28 Apr is a partial week (data starts Thursday 1 May).</p>

<table>
  <thead>
    <tr>
      <th>Week starting</th>
      <th>Engaged users</th>
      <th>Events</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>28 Jul 2014</td><td><strong>1,443</strong> (peak)</td><td>21,472</td></tr>
    <tr><td>4 Aug 2014</td><td><strong>1,266</strong> (−12.3%)</td><td>18,341</td></tr>
    <tr><td>25 Aug 2014</td><td><strong>1,194</strong> (−17.3% vs peak)</td><td>16,166</td></tr>
  </tbody>
</table>

<p>Signups <strong>keep rising</strong> through August (476 → 406 → 473 → 468 → 514). This is not an acquisition hole. Returning users fall (1,153 → 1,055 → 943 → 908). New-to-engagement dips only in the week of 4 Aug, then recovers.</p>

<p>Pooled signup-cohort retention (May–Aug 2014 signups, 7,298 users):</p>

<table>
  <thead>
    <tr>
      <th>Weeks after signup</th>
      <th>Still engaged</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>0</td><td>50.4%</td></tr>
    <tr><td>1</td><td>34.1%</td></tr>
    <tr><td>2</td><td>20.3%</td></tr>
    <tr><td>4</td><td>10.2%</td></tr>
    <tr><td>8</td><td>4.8%</td></tr>
  </tbody>
</table>

<p>Week 0 is ~50% because only activated accounts ever engage. The denominator is <strong>all signups</strong>, which is what the brief asked for.</p>

<p>Device family, peak week vs last week (unique engaged users):</p>

<table>
  <thead>
    <tr>
      <th></th>
      <th>28 Jul</th>
      <th>25 Aug</th>
      <th>Change</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Computer</td><td>951</td><td>864</td><td>−9%</td></tr>
    <tr><td>Phone</td><td>589</td><td>441</td><td>−25%</td></td></tr>
    <tr><td>Tablet</td><td>250</td><td>163</td><td>−35%</td></td></tr>
  </tbody>
</table>

<p>Email, whole window: <strong>33.6% open</strong>, <strong>14.8% CTR</strong>, 44% click-to-open.</p>

<table>
  <thead>
    <tr>
      <th>Week</th>
      <th>Open rate</th>
      <th>CTR</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>28 Jul</td><td>35.2%</td><td><strong>16.1%</strong></td></tr>
    <tr><td>4 Aug</td><td>33.4%</td><td><strong>10.8%</strong></td></tr>
    <tr><td>25 Aug</td><td>35.0%</td><td>11.3%</td></tr>
  </tbody>
</table>

<p>Opens hold. Clicks do not. Event mix (home / like / inbox / login) is almost the same before and after the drop, so this is not one feature disappearing from the log.</p>

<p><strong>What I would tell ops:</strong> growth is fine; existing users, especially on phone and tablet, showed up less from the week of 4 Aug; digest click-through fell at the same time. I <strong>cannot prove</strong> a mobile bug or a broken email CTA from these tables. Those are the next checks, not the conclusion.</p>

<p>Deck: <a href="reports/Ops_Analytics_Report.pptx"><code>reports/Ops_Analytics_Report.pptx</code></a>.</p>

<hr>

<h2>Tech stack</h2>

<table>
  <thead>
    <tr><th>Layer</th><th>Tools</th></tr>
  </thead>
  <tbody>
    <tr><td>Language</td><td>Python 3</td></tr>
    <tr><td>Data</td><td>pandas, NumPy</td></tr>
    <tr><td>SQL</td><td>SQLite (stdlib <code>sqlite3</code>) — cross-checked against pandas results</td></tr>
    <tr><td>Visualization</td><td>matplotlib, seaborn</td></tr>
    <tr><td>Deck generation</td><td><code>python-pptx</code> (rebuilt via <code>reports/build_pptx.py</code>)</td></tr>
    <tr><td>Notebook</td><td>Jupyter</td></tr>
  </tbody>
</table>

<hr>

<h2>How to rerun</h2>

<pre><code>python -m pip install -r requirements.txt
jupyter notebook notebooks/ops_analytics.ipynb</code></pre>

<p>The notebook writes the figures again and runs the same ranking in SQLite (<code>sqlite3</code> is in the stdlib). SQL by itself:</p>

<ul>
  <li><a href="sql/01_job_ops.sql"><code>sql/01_job_ops.sql</code></a></li>
  <li><a href="sql/02_metric_spike.sql"><code>sql/02_metric_spike.sql</code></a></li>
</ul>

<p>Rebuild the deck with <code>python reports/build_pptx.py</code> if the numbers change.</p>

<hr>

<h2>Layout</h2>

<pre><code>README.md
requirements.txt
data/job_data.csv
data/users.csv
data/events.csv
data/email_events.csv
sql/01_job_ops.sql
sql/02_metric_spike.sql
notebooks/ops_analytics.ipynb
reports/figures/*.png
reports/Ops_Analytics_Report.pptx
docs/project_brief.docx</code></pre>

<table>
  <thead>
    <tr><th>File you started with</th><th>Where it lives now</th></tr>
  </thead>
  <tbody>
    <tr><td><code>SQL Project-1 Table.xlsx</code></td><td><code>data/job_data.xlsx</code> + cleaned <code>data/job_data.csv</code></td></tr>
    <tr><td><code>Table-1 users.csv</code></td><td><code>data/users.csv</code></td></tr>
    <tr><td><code>Table-2 events.csv</code></td><td><code>data/events.csv</code></td></tr>
    <tr><td><code>Table-3 email_events.csv</code></td><td><code>data/email_events.csv</code></td></tr>
    <tr><td><code>Operation_Analytics_and_Investigating_Metric-Spike_INFO.docx</code></td><td><code>docs/project_brief.docx</code></td></tr>
  </tbody>
</table>

<hr>

<h2>Limits</h2>

<ul>
  <li>Case 1 has 8 rows on 6 days. Daily throughput doubles with one extra job — rolling averages need more days than this file has. I report the numbers and flag them as thin.</li>
  <li>Week 0 retention (~50%) is an artifact of the denominator: only activated accounts engage, but the brief asks for retention over <em>all signups</em>. The metric is correct per the brief, but the headline number flatters no one.</li>
  <li>"What I would tell ops" is a hypothesis, not a finding. A mobile bug, a broken email CTA, or a content change could all produce the same pattern. Proving any of those needs server-side data this CSV set does not contain.</li>
  <li>No forecast, no causal model. This is descriptive analytics, not predictive.</li>
</ul>

<hr>

<h2>License</h2>

<p>Code is MIT. Dataset and brief are from the practice assignment — see <code>docs/project_brief.docx</code> for the original source.</p>
