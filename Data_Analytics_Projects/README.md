<h1>Data Analytics Projects</h1>

<p>
  <img src="https://img.shields.io/badge/projects-5-blue?style=flat-square" alt="5 projects">
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas">
  <img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=sqlite&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<blockquote><em>Five analytics folders — content scoring, cosmetics similarity, IMDb scores, an engagement drop, and 14 Play Store queries. Each has its own README with numbers and how to run it.</em></blockquote>

<hr>

<h2>What's in here</h2>

<p>Five projects I keep in one place. Same stack in all of them: pandas, then the same numbers again in SQLite.</p>

<table>
  <thead>
    <tr>
      <th>Folder</th>
      <th>What it is</th>
      <th>Headline</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="Accenture_Data_analytics_and_Visualization/"><code>Accenture_Data_analytics_and_Visualization</code></a></td>
      <td>Top 5 Social Buzz categories by reaction <em>score</em></td>
      <td>Animals <strong>68,624</strong> — pandas and SQL agree</td>
    </tr>
    <tr>
      <td><a href="Cosmetics_Ingredient_Analysis/"><code>Cosmetics_Ingredient_Analysis</code></a></td>
      <td>Similar formulas among dry-skin moisturizers</td>
      <td>190 × 2,233 one-hot; example cosine <strong>0.535</strong></td>
    </tr>
    <tr>
      <td><a href="IMDB_Movie_Analysis/"><code>IMDB_Movie_Analysis</code></a></td>
      <td>What moves an IMDb score?</td>
      <td>4,916 titles; budget vs gross <strong>r = 0.627</strong></td>
    </tr>
    <tr>
      <td><a href="Operations_Analytics_And_Investigating_Metric_Spike/"><code>Operations_Analytics_And_Investigating_Metric_Spike</code></a></td>
      <td>Job-review ops + an August engagement drop</td>
      <td>Peak 1,443 engaged; <strong>−17.3%</strong> by 25 Aug</td>
    </tr>
    <tr>
      <td><a href="Playstore%20Apps%20Analysis%20%26%20Visualization/"><code>Playstore Apps Analysis & Visualization</code></a></td>
      <td>14 assigned Play Store questions</td>
      <td>9,648 apps; GAME installs <strong>13.9B</strong> (bucket floors)</td>
    </tr>
  </tbody>
</table>

<p>Each folder has its own README with numbers, plots or a deck, and how to run it.</p>

<hr>

<h2>Social Buzz — content popularity</h2>

<p>Accenture / Forage virtual experience. Popularity is the <strong>sum of reaction scores</strong>, not the count. Super love is 75; disgust is 0. Sample window <strong>18 Jun 2020 – 18 Jun 2021</strong>: 962 posts, 22,534 reactions, total score <strong>893,482</strong>. Sixteen categories after cleaning labels.</p>

<table>
  <thead>
    <tr><th>Rank</th><th>Category</th><th>Score</th><th>Share</th></tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>Animals</td><td>68,624</td><td>7.7%</td></tr>
    <tr><td>2</td><td>Science</td><td>65,405</td><td>7.3%</td></tr>
    <tr><td>3</td><td>Healthy eating</td><td>63,138</td><td>7.1%</td></tr>
    <tr><td>4</td><td>Technology</td><td>63,035</td><td>7.1%</td></tr>
    <tr><td>5</td><td>Food</td><td>61,598</td><td>6.9%</td></tr>
  </tbody>
</table>

<p>Those five hold <strong>36.0%</strong> of all score. Mean score per reaction is almost flat (~38–41), so the ranking is mostly volume. Same top 5 in pandas and SQLite.</p>

<p>Stack: pandas, SQLite, matplotlib, seaborn, python-pptx.</p>

<hr>

<h2>Cosmetics ingredient analysis</h2>

<p>MedTourEasy / DataCamp-style brief. <strong>1,472</strong> Sephora products. I turn the ingredient lists of <strong>190 dry-skin moisturizers</strong> into a 190 × 2,233 one-hot matrix (98.4% sparse, mean 35.1 ingredients), shrink it with t-SNE, and score neighbors with cosine.</p>

<p>Example pair: AmorePacific Color Control Cushion SPF 50+ vs Laneige BB Cushion Hydra Radiance — cosine <strong>0.535</strong>, 23 shared ingredients (Jaccard 0.365). Laneige is $22 cheaper and 0.3 stars higher. Next neighbor after that pair is only 0.333, so it is a real cluster, not a t-SNE smear.</p>

<p>t-SNE axes have no units. This is shared ingredients, not safety or a dermatology tool. 471 catalogue products have no skin-type flag.</p>

<p>Stack: pandas, scikit-learn (t-SNE), cosine / Jaccard, SQLite, Excel, matplotlib.</p>

<hr>

<h2>IMDb movie analysis</h2>

<p>Kaggle IMDb dump: 5,043 rows → <strong>4,916 unique titles</strong>. Five assigned questions in pandas, SQLite, and Excel. Short version: <strong>genre, runtime, and director</strong> move IMDb score; <strong>budget</strong> moves gross, not score.</p>

<ul>
  <li>Drama is the most common tag (2,532). Highest mean among genres with ≥50 tags: Documentary <strong>7.18</strong>. Horror <strong>5.80</strong>.</li>
  <li>Runtime vs IMDb: Pearson <strong>r = 0.265</strong>. Bins: <90 → 6.11, <strong>>150 → 7.44</strong>.</li>
  <li>English is 93% of the file (mean 6.39). Smaller languages look better because famous titles survive.</li>
  <li>Directors with ≥5 films: <strong>Christopher Nolan 8.425</strong> (8 films).</li>
  <li>Budget vs gross after dropping 10 local-currency miscodes above $400M: <strong>r = 0.627</strong>. Budget vs IMDb ≈ 0.04. Highest profit: Avatar $523.5M.</li>
</ul>

<p>Missing budget (492) and gross (884) stay missing. Scores are IMDb user averages, not studio P&L. Gross is mostly US theatrical.</p>

<p>Stack: pandas, SQLite, Excel (<code>=CORREL()</code>), matplotlib, python-pptx.</p>

<hr>

<h2>Ops analytics and the August drop</h2>

<p>Two cases from the same brief.</p>

<p><strong>Case 1</strong> — job-review throughput. Only <strong>8 jobs over 6 days</strong> (25–30 Nov 2020). Throughput 0.0417–0.0833 jobs/hour. Persian is 3/8 of the language share. One extra job doubles a daily rate, so I do not treat the 7-day rolling number as a capacity SLA.</p>

<p><strong>Case 2</strong> — engagement, 1 May – 31 Aug 2014. 19,066 accounts (9,381 activated, 49.2%), 340,832 events, 90,389 email rows. Peak engaged users <strong>1,443</strong> (week of 28 Jul). Then 1,266 on 4 Aug (<strong>−12.3%</strong>) and 1,194 on 25 Aug (<strong>−17.3%</strong> vs peak). Phone −25%, tablet −35%, computer −9%. Email open rate holds (~33–35%); CTR falls 16.1% → 10.8% the week of 4 Aug. Signup-cohort week-0 retention is 50.4% — inflated because only activated accounts engage while the denominator is all signups.</p>

<p>Descriptive only. I do not claim a cause (mobile bug vs broken CTA vs content).</p>

<p>Stack: pandas, SQLite, matplotlib, seaborn, python-pptx.</p>

<hr>

<h2>Play Store — 14 SQL questions</h2>

<p>Kaggle Play Store dump. Cleaned apps: <strong>9,648</strong> (dropped the <code>Category = 1.9</code> row and duplicate names). Reviews: 29,692 unique (from 37,427). 1,458 apps have no rating; I <strong>did not impute</strong>. Among rated apps: median 4.3, mean 4.173.</p>

<p>Headline answers: highest rating 5.0 on <strong>271</strong> apps (most have almost no reviews). Most reviews: <strong>Facebook</strong> 78,158,306. Paid “revenue” <code>price × install floor</code> = <strong>$291,097,458</strong> (Minecraft $69.9M). Category installs: <strong>GAME 13,878,924,415</strong>. Genre with most apps: Tools 824. Free / paid: 8,895 / 753 (92.2% / 7.8%). Android string <code>4.0.3 and up</code> exact match: 1,395.</p>

<p>Installs are bucket floors. That “revenue” is not Google’s take.</p>

<p>Stack: pandas, SQLite, matplotlib, python-pptx. Sentiment labels are already in the Kaggle file.</p>

<hr>

<h2>Tech stack across all five</h2>

<table>
  <thead>
    <tr><th>Layer</th><th>Tools</th></tr>
  </thead>
  <tbody>
    <tr><td>Language</td><td>Python 3</td></tr>
    <tr><td>Data</td><td>pandas, NumPy</td></tr>
    <tr><td>SQL</td><td>SQLite (<code>sqlite3</code>) — same numbers as pandas</td></tr>
    <tr><td>Spreadsheet</td><td>Excel (IMDb correlation, cosmetics aggregates)</td></tr>
    <tr><td>Similarity (cosmetics)</td><td>scikit-learn t-SNE, cosine, Jaccard</td></tr>
    <tr><td>Visualization</td><td>matplotlib, seaborn</td></tr>
    <tr><td>Deck</td><td>python-pptx</td></tr>
    <tr><td>Notebook</td><td>Jupyter</td></tr>
  </tbody>
</table>

<hr>

<h2>Layout</h2>

<pre><code>README.md                                              this file
Accenture_Data_analytics_and_Visualization/            Social Buzz top 5
Cosmetics_Ingredient_Analysis/                         ingredient cosine + t-SNE
IMDB_Movie_Analysis/                                   five IMDb questions
Operations_Analytics_And_Investigating_Metric_Spike/   ops + August drop
Playstore Apps Analysis & Visualization/               14 Play Store queries</code></pre>

<p>Open a folder and use that README to run it. This file is only the index.</p>

<hr>

<h2>License</h2>

<p>Code is MIT unless a child README says otherwise. Data: Forage / Accenture sample, Sephora catalogue (MedTourEasy / DataCamp brief), Kaggle IMDb dump, ops CSVs from the brief, Kaggle Play Store dump — see each <code>data/README.md</code>.</p>
