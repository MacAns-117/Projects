<h1>Play Store Apps — 14 SQL Questions</h1>

<p>
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas">
  <img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=sqlite&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/python--pptx-CB2B5A?style=flat-square" alt="python-pptx">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<blockquote><em>Kaggle Google Play Store dump — 14 assigned SQL questions answered in both pandas and SQLite, with a short deck. Includes data-cleaning callouts and a deliberate choice not to fill missing ratings.</em></blockquote>

<hr>

<h2>The question</h2>

<p>Kaggle Google Play Store dump. I cleaned the two tables, answered the <strong>14 assigned queries</strong> in pandas and SQLite, and put the numbers in a short deck.</p>

<p>This is a practice project, not a live store audit. Install counts are <strong>bucket floors</strong> (<code>10,000</code> means "10,000+"). Paid "revenue" is <code>price × installs</code>, not Google's actual take.</p>


<hr>

<h2>Cleaning</h2>

<ul>
  <li>Dropped the broken row with <code>Category = 1.9</code>.</li>
  <li>Dropped duplicate app names (kept first). <strong>9,648</strong> apps.</li>
  <li><strong>Did not fill missing ratings.</strong> 1,458 apps have no rating. Filling them with the mean (~4.19) made unrated apps look average.</li>
  <li>Review table: dropped duplicate rows. <strong>29,692</strong> unique reviews (from 37,427). Sentiment counts below use the unique file.</li>
</ul>

<hr>

<h2>Answers</h2>

<table>
  <thead>
    <tr>
      <th>#</th>
      <th>Question</th>
      <th>Answer</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1–2</td>
      <td>Highest rating</td>
      <td><strong>5.0</strong>, <strong>271 apps</strong>. Most have almost no reviews. Highest-review 5.0 app: <strong>Ríos de Fe</strong> (141 reviews, 1,000 installs). A 5.0 with 141 reviews is not "best on the store."</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Most reviews</td>
      <td><strong>Facebook</strong>, SOCIAL, <strong>78,158,306</strong> reviews, 1B+ installs.</td>
    </tr>
    <tr>
      <td>4</td>
      <td>Paid revenue (price × installs)</td>
      <td><strong>$291,097,458</strong>. Top: Minecraft $69.9M, I am rich $40.0M.</td>
    </tr>
    <tr>
      <td>5</td>
      <td>Category with most installs</td>
      <td><strong>GAME</strong>, <strong>13,878,924,415</strong>. Then COMMUNICATION.</td>
    </tr>
    <tr>
      <td>6</td>
      <td>Genre with most apps</td>
      <td><strong>Tools</strong>, <strong>824</strong>.</td>
    </tr>
    <tr>
      <td>7</td>
      <td>Games by installs</td>
      <td><strong>Subway Surfers</strong> (1B+), then Candy Crush / My Talking Tom / Pou / Temple Run 2 (500M+). 959 games.</td>
    </tr>
    <tr>
      <td>8</td>
      <td>Android Ver = 4.0.3 and up</td>
      <td><strong>1,395</strong> apps. Exact string match, not "4.0.3 or newer."</td>
    </tr>
    <tr>
      <td>9</td>
      <td>Free / paid</td>
      <td><strong>8,895 free</strong>, <strong>753 paid</strong> (92.2% / 7.8%).</td>
    </tr>
    <tr>
      <td>10</td>
      <td>Best dating app (most reviews)</td>
      <td><strong>Zoosk Dating App: Meet Singles</strong>, <strong>516,801</strong> reviews, rating 4.0.</td>
    </tr>
    <tr>
      <td>11</td>
      <td>"10 Best Foods for You" sentiment</td>
      <td>Unique: <strong>79 positive / 11 neutral / 5 negative</strong>.</td>
    </tr>
    <tr>
      <td>12</td>
      <td>ASUS SuperNote, polarity=1 and subjectivity=1</td>
      <td>One comment: <strong>"Awesome!!!!"</strong></td>
    </tr>
    <tr>
      <td>13</td>
      <td>Neutral reviews, Abs Training-Burn belly fat</td>
      <td><strong>5</strong> comments.</td>
    </tr>
    <tr>
      <td>14</td>
      <td>Negative reviews, Adobe Acrobat Reader</td>
      <td><strong>20</strong> unique comments.</td>
    </tr>
  </tbody>
</table>

<p>Among apps that have a rating: median <strong>4.3</strong>, mean <strong>4.173</strong>.</p>

<p>Unique reviews overall: 64% positive, 21% negative, 15% neutral.</p>

<p>Deck: <a href="reports/Playstore_Report.pptx"><code>reports/Playstore_Report.pptx</code></a>.</p>

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
    <tr><td>Sentiment</td><td>Pre-shipped polarity / subjectivity scores in the Kaggle reviews dataset</td></tr>
    <tr><td>Visualization</td><td>matplotlib, seaborn</td></tr>
    <tr><td>Deck generation</td><td><code>python-pptx</code></td></tr>
    <tr><td>Notebook</td><td>Jupyter</td></tr>
  </tbody>
</table>

<hr>

<h2>How to rerun</h2>

<pre><code>python -m pip install -r requirements.txt
jupyter notebook notebooks/playstore_analysis.ipynb</code></pre>

<p>SQL: <a href="sql/queries.sql"><code>sql/queries.sql</code></a>. <code>sqlite3</code> is in the stdlib. The notebook loads the CSVs into memory and checks pandas vs SQL.</p>

<hr>

<h2>Layout</h2>

<pre><code>README.md
requirements.txt
data/playstore_apps.csv
data/playstore_reviews.csv
sql/queries.sql
notebooks/playstore_analysis.ipynb
reports/Playstore_Report.pptx
reports/figures/*.png</code></pre>


<hr>

<h2>Limits</h2>

<ul>
  <li>Install counts are <strong>bucket floors</strong>, not exact numbers. "10,000+" could mean 10,001 or 50,000 — Google does not publish the precise figure. Revenue figures inherit this blur.</li>
  <li>Paid "revenue" is <code>price × installs</code>, not Google's actual take. Google takes 15–30%, and refunds / promos are not in the data.</li>
  <li>Ratings: 1,458 apps (15%) have no rating. I chose <strong>not</strong> to impute — filling with the mean (~4.19) would have made unrated apps look average. Aggregate medians and means are computed on the 8,190 apps that <em>do</em> have a rating.</li>
  <li>Question 8 is an <strong>exact string match</strong> on "4.0.3 and up", not "4.0.3 or newer". Apps labelled "4.0.3 - 6.0" or "4.1 and up" would not match.</li>
  <li>Sentiment scores are pre-shipped in the Kaggle dataset, not computed by me. If the upstream polarity model is biased, these counts are too.</li>
</ul>

<hr>

<h2>License</h2>

<p>Code is MIT. The dataset is from the Kaggle Google Play Store dump — see each <code>data/README.md</code> for attribution.</p>
