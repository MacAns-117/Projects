<h1>IMDb Movie Analysis</h1>

<p>
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas">
  <img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=sqlite&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Excel-217346?style=flat-square&logo=microsoft-excel&logoColor=white" alt="Excel">
  <img src="https://img.shields.io/badge/python--pptx-CB2B5A?style=flat-square" alt="python-pptx">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<blockquote><em>Kaggle IMDb dump (5,043 rows → 4,916 unique titles) — what drives a high IMDb score? Genre, runtime, and director move the score; budget moves gross. Five assigned questions answered in pandas, SQLite, and Excel.</em></blockquote>

<hr>

<h2>The question</h2>

<p>Kaggle IMDb dump (5,043 rows). I cleaned it to <strong>4,916 unique titles</strong> and answered the five assigned questions with <strong>pandas, SQLite, and Excel</strong>.</p>

<p>Question in the brief: <em>what is tied to a high IMDb score?</em> Short version: <strong>genre mix, runtime, and who directed it</strong> move the score more than <strong>budget</strong>. Budget does move <strong>gross</strong>.</p>

<p>This is a practice project. Scores are IMDb user averages, not box office "success." Gross is mostly US theatrical.</p>

<hr>

<h2>Cleaning</h2>

<ul>
  <li>Trailing <code>\xa0</code> on titles.</li>
  <li>45 exact duplicate rows dropped.</li>
  <li>82 extra copies of the same title: kept the row with more votes.</li>
  <li>1,458-style mean-fill is not used here. Missing budget/gross stay missing (884 gross, 492 budget on the raw file).</li>
  <li>10 budgets above $400M look like <strong>local currency</strong> (Lady Vengeance KRW, Princess Mononoke JPY, Fateless HUF). Those rows are excluded from correlation and profit.</li>
</ul>

<hr>

<h2>Answers</h2>

<p><strong>A. Genre.</strong> Drama is the most common tag (<strong>2,532</strong>). Highest mean IMDb among genres with ≥50 tags: <strong>Documentary 7.18</strong>, <strong>Biography 7.15</strong>, <strong>History 7.09</strong>, <strong>War 7.07</strong>. Lowest: <strong>Horror 5.80</strong>. Comedy is common (1,847) and sits below the all-movie mean (6.19 vs 6.44).</p>

<p><strong>B. Duration.</strong> Mean 107.1 min, median 103, mode <strong>90</strong>, std 25.3 (n = 4,901). Pearson <strong>r = 0.265</strong> with IMDb (Spearman 0.322). Bins: &lt;90 → 6.11, 90–120 → 6.32, 120–150 → 6.97, <strong>&gt;150 → 7.44</strong>. Longer films score higher <em>on average</em>. That is not "add 40 minutes."</p>

<p><strong>C. Language.</strong> English is <strong>4,582 / 4,916 (93%)</strong>, mean <strong>6.39</strong>. Smaller languages look better (Japanese 7.35 n=17, German 7.34 n=19, French 7.04 n=73) because this file mostly keeps the famous foreign titles, not a random catalogue.</p>

<p><strong>D. Directors.</strong> 2,397 names; 1,523 have one film. Ranking uses <strong>214 directors with ≥5 films</strong>. Top mean: <strong>Christopher Nolan 8.425</strong> (8 films). Then Tarantino 8.20, Capra 8.06, Kubrick 8.05, Cameron 7.91. 90th percentile of those means is <strong>7.41</strong>; 95th is <strong>7.63</strong>. Nolan is at the 100th percentile of that set. A 9.5 from a one-film / TV row (Towering Inferno, John Blanchard) is not a director ranking.</p>

<p><strong>E. Budget vs money.</strong> 3,789 rows have both budget and gross. Raw Pearson <strong>r = 0.22</strong> because of the FX rows. After dropping 10 &gt;$400M budgets: <strong>r = 0.627</strong> (Spearman 0.646). Budget vs IMDb is almost zero (<strong>r ≈ 0.04</strong>). Highest profit (gross − budget): <strong>Avatar $523.5M</strong>, Jurassic World $502.2M, Titanic $458.7M, Star Wars (1977) $449.9M, E.T. $424.4M.</p>

<p>Excel <code>=CORREL()</code> lives on sheet <code>E_correl</code> and will recalc in Excel.</p>

<hr>

<h2>Five whys (on the duration pattern)</h2>

<ol>
  <li><strong>Why do longer films have higher IMDb?</strong> They cluster with prestige drama / biography / war, not 90-minute horror.</li>
  <li><strong>Why those genres run long?</strong> Story and awards-circuit habit, plus editors keeping footage when it works.</li>
  <li><strong>Why does that raise the average?</strong> IMDb voters who finish a 160-minute film are already bought in; cheap horror pads the short-runtime bin with 5.x scores.</li>
  <li><strong>Why isn't this a production lever?</strong> Stretching a weak script does not turn it into Shawshank.</li>
  <li><strong>Why it still matters:</strong> runtime is a <strong>proxy for intent</strong>, not a cause. If you only "optimize IMDb," you are looking at the wrong number for a studio P&amp;L anyway — budget tracks gross, not score.</li>
</ol>

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
    <tr><td>Spreadsheet</td><td>Microsoft Excel — <code>=CORREL()</code>, <code>COUNTIF</code>-style tables, manual cross-check</td></tr>
    <tr><td>Visualization</td><td>matplotlib, seaborn</td></tr>
    <tr><td>Deck generation</td><td><code>python-pptx</code></td></tr>
    <tr><td>Notebook</td><td>Jupyter</td></tr>
  </tbody>
</table>

<hr>

<h2>How to rerun</h2>

<pre><code>python -m pip install -r requirements.txt
jupyter notebook notebooks/imdb_analysis.ipynb</code></pre>

<p>Open the xlsx in Excel/LibreOffice for COUNTIF-style tables and the <code>CORREL</code> formula. SQLite is in the notebook (stdlib).</p>

<hr>

<h2>Layout</h2>

<pre><code>README.md
requirements.txt
data/imdb_movies.csv
data/genre_imdb_stats.csv
excel/imdb_analysis.xlsx      Notes, A–E sheets, =CORREL
sql/queries.sql
notebooks/imdb_analysis.ipynb
reports/IMDB_Report.pptx
docs/IMDB_Movie_Analysis_Info.docx</code></pre>

<hr>

<h2>Limits</h2>

<ul>
  <li><strong>Survivorship bias in foreign languages.</strong> The dataset keeps the famous foreign titles (Kurosawa, Park Chan-wook, Fellini), not a random catalogue. The Japanese mean of 7.35 is a list of classics, not a representative sample of Japanese cinema.</li>
  <li><strong>Budget FX contamination.</strong> 10 rows with budgets above $400M are local currency miscoded as USD. They are excluded from correlation and profit, but I cannot fix the upstream Kaggle entry.</li>
  <li><strong>Missing budget/gross not imputed.</strong> 884 gross and 492 budget values stay missing. Mean-filling would have invented numbers; I would rather lose the rows than fake the data.</li>
  <li><strong>Director ranking uses ≥5 films.</strong> A one-film director with a 9.5 (e.g., John Blanchard's <em>Towering Inferno</em>) is excluded because it is not a director ranking — it is a single-film rating.</li>
  <li><strong>IMDb score is user average, not "success."</strong> A 7.5 IMDb does not equal a hit. Budget tracks gross (r ≈ 0.63), not score (r ≈ 0.04). Optimizing IMDb alone is the wrong objective for a studio P&amp;L.</li>
  <li><strong>Gross is mostly US theatrical.</strong> Streaming, international, and home video are not in this dataset.</li>
</ul>

<hr>

<h2>License</h2>

<p>Code is MIT. The dataset is from the Kaggle IMDb dump — see <code>docs/IMDB_Movie_Analysis_Info.docx</code> for the original brief.</p>