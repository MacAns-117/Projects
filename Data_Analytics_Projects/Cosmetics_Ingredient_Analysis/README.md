<h1>Analysis of Chemical Components</h1>

<p>
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="pandas">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/t--SNE-7B68EE?style=flat-square" alt="t-SNE">
  <img src="https://img.shields.io/badge/Excel-217346?style=flat-square&logo=microsoft-excel&logoColor=white" alt="Excel">
  <img src="https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=sqlite&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<blockquote><em>MedTourEasy traineeship project — turn the ingredient lists of 190 dry-skin moisturizers into a 190 × 2,233 one-hot matrix, shrink with t-SNE, and use cosine similarity as a "similar formula" score. Same brief as the DataCamp "Evaluating Cosmetics Ingredients" capstone.</em></blockquote>

<hr>

<h2>The question</h2>

<p>MedTourEasy traineeship project (same brief as DataCamp <em>Evaluating Cosmetics Ingredients</em>).</p>

<p><strong>1,472</strong> Sephora products. I turn the ingredient lists of <strong>190 dry-skin moisturizers</strong> into a 190 × 2,233 one-hot matrix, shrink it with t-SNE, and use cosine on that matrix as a cheap "similar formula" score.</p>

<p>This is a practice project, not a dermatology tool. t-SNE axes have no units. Close points share ingredients; they are not proven safer.</p>

<p>The original Bokeh hover plot is replaced with a static map plus a neighbor table. Same math, no extra UI.</p>

<hr>

<h2>What I ran</h2>

<table>
  <thead>
    <tr><th></th><th></th></tr>
  </thead>
  <tbody>
    <tr><td>Catalogue</td><td>298 moisturizers, 281 cleansers, 266 face masks, 248 treatments, 209 eye creams, 170 sun protect</td></tr>
    <tr><td>Brands</td><td>116. CLINIQUE 79, SEPHORA COLLECTION 66, SHISEIDO 63</td></tr>
    <tr><td>Price</td><td>mean <strong>$55.58</strong>, median $42.50. Treatments median $64.50, cleansers $28</td></tr>
    <tr><td>Rank</td><td>mean <strong>4.15</strong>. Eye cream is the weak category (3.81). 19 products have rank 0</td></tr>
    <tr><td>Skin flags</td><td>Combination 966, Normal 960, Dry 904, Oily 894, Sensitive 756. <strong>471</strong> have no flag at all</td></tr>
    <tr><td>Dry moisturizers</td><td><strong>190</strong>. Vocabulary <strong>2,233</strong>. Mean <strong>35.1</strong> ingredients / product. Matrix sparsity 98.4%</td></tr>
    <tr><td>Check token</td><td><code>decyl oleate</code> index <strong>25</strong></td></tr>
  </tbody>
</table>

<hr>

<h2>The example pair</h2>

<p>AmorePacific <strong>Color Control Cushion Compact Broad Spectrum SPF 50+</strong> ($60, rank 4.0) vs Laneige <strong>BB Cushion Hydra Radiance SPF 50</strong> ($38, rank 4.3).</p>

<ul>
  <li>Cosine on the ingredient vector: <strong>0.535</strong> (nearest other product)</li>
  <li>Shared ingredients: <strong>23</strong> (Jaccard 0.365)</li>
  <li>Laneige is <strong>$22 cheaper</strong> and 0.3 stars higher</li>
</ul>

<p>Next cosine neighbor after Laneige is only 0.333 (Supergoop CC cream). So this pair is a real cluster, not a t-SNE accident.</p>

<hr>

<h2>Tech stack</h2>

<table>
  <thead>
    <tr><th>Layer</th><th>Tools</th></tr>
  </thead>
  <tbody>
    <tr><td>Language</td><td>Python 3</td></tr>
    <tr><td>Data</td><td>pandas, NumPy</td></tr>
    <tr><td>Feature engineering</td><td>One-hot encoding of ingredient lists (190 × 2,233 matrix, 98.4% sparse)</td></tr>
    <tr><td>Dimensionality reduction</td><td><strong>t-SNE</strong> (scikit-learn)</td></tr>
    <tr><td>Similarity</td><td><strong>Cosine similarity</strong> + Jaccard index on ingredient sets</td></tr>
    <tr><td>Visualization</td><td>Static map (matplotlib / seaborn) + neighbor table</td></tr>
    <tr><td>SQL</td><td>SQLite (stdlib <code>sqlite3</code>) — catalogue queries only</td></tr>
    <tr><td>Spreadsheet</td><td>Excel — cross-check of catalogue aggregates</td></tr>
    <tr><td>Notebook</td><td>Jupyter</td></tr>
  </tbody>
</table>

<hr>

<h2>How to rerun</h2>

<pre><code>python -m pip install -r requirements.txt
jupyter notebook notebooks/cosmetics_analysis.ipynb</code></pre>

<p>SQL: <a href="sql/queries.sql"><code>sql/queries.sql</code></a> (catalogue only). Excel: <a href="excel/cosmetics_analysis.xlsx"><code>excel/cosmetics_analysis.xlsx</code></a>. Deck: <a href="reports/Cosmetics_Report.pptx"><code>reports/Cosmetics_Report.pptx</code></a>.</p>

<hr>

<h2>Layout</h2>

<pre><code>README.md
data/cosmetics.csv
sql/queries.sql
excel/cosmetics_analysis.xlsx
notebooks/cosmetics_analysis.ipynb
reports/Cosmetics_Report.pptx</code></pre>

<table>
  <thead>
    <tr><th>File you started with</th><th>Where it lives now</th></tr>
  </thead>
  <tbody>
    <tr><td><code>notebook.ipynb</code> (empty DataCamp starter)</td><td>replaced by <code>notebooks/cosmetics_analysis.ipynb</code></td></tr>
    <tr><td><code>MTE_Proj_1.ipynb</code> (filled DataCamp version)</td><td>replaced by <code>notebooks/cosmetics_analysis.ipynb</code></td></tr>
    <tr><td><code>README.md</code></td><td>this file</td></tr>
  </tbody>
</table>

<hr>

<h2>Limits</h2>

<ul>
  <li><strong>Not a dermatology tool.</strong> t-SNE axes have no units. Close points share ingredients; they are not proven safer or more effective. This is a similarity analysis, not a product recommendation engine.</li>
  <li><strong>Sephora catalogue is the universe.</strong> 1,472 products is a small slice of the global cosmetics market. Brands not carried by Sephora are invisible to this analysis.</li>
  <li><strong>Ingredient lists are messy.</strong> Sephora provides them as free-text strings; tokenisation handles most cases but complex chemical names can be split or merged incorrectly. The <code>decyl oleate</code> index 25 check is a sanity test, not a guarantee of clean tokenisation across all 2,233 vocabulary terms.</li>
  <li><strong>Matrix is 98.4% sparse.</strong> Most ingredients appear in only a handful of products. t-SNE on sparse one-hot matrices can produce misleading clusters; the cosine similarity score is the more reliable signal, with t-SNE as the visual aid.</li>
  <li><strong>Skin-type flags are vendor-supplied.</strong> 471 products have no skin-type flag at all. The "dry-skin moisturizers" subset (190) is filtered by vendor flag, not by ingredient analysis.</li>
  <li><strong>No price-quality model.</strong> The example pair shows Laneige is cheaper and higher-ranked than AmorePacific, but this is a single observation — not a generalisable claim about brand pricing.</li>
</ul>

<hr>

<h2>License</h2>

<p>Code is MIT. The Sephora catalogue is from the MedTourEasy traineeship brief / DataCamp <em>Evaluating Cosmetics Ingredients</em> dataset — see the original sources for data licensing.</p>