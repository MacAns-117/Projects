<h1>Social Buzz — Content Popularity</h1>

<p>
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas">
  <img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=sqlite&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Accenture-Forage-A100FF?style=flat-square" alt="Accenture Forage">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<blockquote><em>Accenture / Forage virtual experience — finding the top 5 content categories by reaction-score popularity, scored in both pandas and SQL.</em></blockquote>

<hr>

<h2>The question</h2>

<p>Forage / Accenture <strong>Data Analytics and Visualization</strong> virtual experience. The brief: take Social Buzz's sample of posts and reactions and find the <strong>top 5 content categories by popularity</strong>.</p>

<p>Popularity is the <strong>sum of reaction scores</strong>, not the number of reactions. A "super love" is 75 points; "disgust" is 0.</p>

<p>I cleaned the labels, scored every category in <strong>pandas</strong> and again in <strong>SQL (SQLite)</strong>, and put the result in a short deck. Same ranking both ways. This is a practice project, not a live client.</p>

<hr>

<h2>Result</h2>

<p>After stripping quote marks off category names there are <strong>16</strong> categories (not 17). Sample window: <strong>18 Jun 2020 – 18 Jun 2021</strong>.</p>

<table>
  <thead>
    <tr><th></th><th></th></tr>
  </thead>
  <tbody>
    <tr><td>Reactions</td><td>22,534</td></tr>
    <tr><td>Posts</td><td>962</td></tr>
    <tr><td>Users who reacted</td><td>500</td></tr>
    <tr><td>Total popularity score</td><td>893,482</td></tr>
  </tbody>
</table>

<p><strong>Top 5 by score</strong></p>

<table>
  <thead>
    <tr>
      <th>Rank</th>
      <th>Category</th>
      <th>Score</th>
      <th>Reactions</th>
      <th>Share of all score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Animals</td>
      <td>68,624</td>
      <td>1,738</td>
      <td>7.7%</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Science</td>
      <td>65,405</td>
      <td>1,646</td>
      <td>7.3%</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Healthy eating</td>
      <td>63,138</td>
      <td>1,572</td>
      <td>7.1%</td>
    </tr>
    <tr>
      <td>4</td>
      <td>Technology</td>
      <td>63,035</td>
      <td>1,557</td>
      <td>7.1%</td>
    </tr>
    <tr>
      <td>5</td>
      <td>Food</td>
      <td>61,598</td>
      <td>1,556</td>
      <td>6.9%</td>
    </tr>
  </tbody>
</table>

<p>Those five hold <strong>36.0%</strong> of all score. Mean score per reaction is almost flat across categories (about 38–41), so the ranking is mostly <strong>volume</strong>, not "people love Animals more intensely." Public speaking has the highest mean (41.0) but the smallest volume.</p>

<p><strong>Also in the sample</strong></p>

<ul>
  <li>Sentiment: 56.2% positive, 31.2% negative, 12.5% neutral.</li>
  <li>Photos carry the most total score (241k), then video, GIF, audio.</li>
  <li>Busiest month: May 2021 (1,954 reactions). January 2021 is 1,949.</li>
  <li>2020 has more reactions than 2021 in this file (12,195 vs 10,339) because the window is mid-June to mid-June, not because 2021 was quieter on purpose.</li>
</ul>

<p>Deck: <a href="reports/Social_Buzz_Insights.pptx"><code>reports/Social_Buzz_Insights.pptx</code></a>. Charts: <a href="reports/figures/"><code>reports/figures/</code></a>.</p>

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
jupyter notebook notebooks/social_buzz_analysis.ipynb</code></pre>

<p>The notebook writes the figures again and runs the SQLite query (stdlib, no extra package). Rebuild the deck with <code>python reports/build_pptx.py</code> if you change numbers.</p>

<p>The SQL by itself is <a href="sql/top_categories.sql"><code>sql/top_categories.sql</code></a>.</p>

<hr>

<h2>Layout</h2>

<pre><code>README.md
requirements.txt
data/cleaned_reactions.csv
data/README.md
docs/data_model.pdf
notebooks/social_buzz_analysis.ipynb
sql/top_categories.sql
reports/figures/*.png
reports/Social_Buzz_Insights.pptx
reports/build_pptx.py</code></pre>

<table>
  <thead>
    <tr><th>File you started with</th><th>Where it lives now</th></tr>
  </thead>
  <tbody>
    <tr><td><code>Cleaned_data.csv</code></td><td><code>data/cleaned_reactions.csv</code></td></tr>
    <tr><td><code>Data model.pdf</code></td><td><code>docs/data_model.pdf</code></td></tr>
    <tr><td><code>post_Insights.pptx</code></td><td>replaced by <code>reports/Social_Buzz_Insights.pptx</code></td></tr>
    <tr><td><code>README.md</code></td><td>this file</td></tr>
  </tbody>
</table>

<hr>

<h2>Limits</h2>

<ul>
  <li>Forage sample, not the live Social Buzz warehouse.</li>
  <li>"Posts per day" in the story (100k) is client context, not this CSV.</li>
  <li>Category labels were messy (<code>"animals"</code> vs <code>Animals</code>); I lowercased them. If two real topics were collapsed, the ranking would move.</li>
  <li>No user-level model, no A/B, no production pipeline.</li>
</ul>

<hr>

<h2>License</h2>

<p>Use the write-up as you like. The dataset is from the Forage Accenture programme.</p>
