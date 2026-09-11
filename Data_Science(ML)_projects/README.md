<h1>Data Science / ML Projects</h1>

<p>
  <img src="https://img.shields.io/badge/projects-3-blue?style=flat-square" alt="3 projects">
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<blockquote><em>Three self-directed ML and Python projects — classification, regression, and a rule-based voice assistant. Each folder has its own README with numbers, plots, and how to run it.</em></blockquote>

<hr>

<h2>What's in here</h2>

<p>Three small projects I keep in one place:</p>

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
      <td><a href="hotel-churn-prediction/"><code>hotel-churn-prediction/</code></a></td>
      <td>Will this hotel booking cancel?</td>
      <td>Random forest, holdout <strong>ROC-AUC 0.815</strong></td>
    </tr>
    <tr>
      <td><a href="indian-house-price-prediction/"><code>indian-house-price-prediction/</code></a></td>
      <td>Asking price of an Indian listing</td>
      <td>Gradient boosting, typical error <strong>₹12.1 lakh</strong></td>
    </tr>
    <tr>
      <td><a href="stella-bot/"><code>stella-bot/</code></a></td>
      <td>Voice assistant (not ML)</td>
      <td>Keyword commands + Wikipedia / jokes / sites</td>
    </tr>
  </tbody>
</table>

<p>Each folder has its own README with numbers, plots, and how to run it.</p>

<hr>

<h2>Hotel booking cancellation</h2>

<p>Binary classification on hotel bookings (<code>is_canceled</code>). Cleaned table is 28k+ rows after dropping duplicates and junk. Train on 2015–2016, test on 2017 so the cancel rate shift (about 25% → 32%) is in the score.</p>

<p>Main model is a random forest. Logistic regression is the baseline. I do <strong>not</strong> use <code>reservation_status</code> — that column is the outcome.</p>

<p><strong>Holdout:</strong> accuracy 0.76, ROC-AUC <strong>0.815</strong>, precision / recall about 0.62 on the cancel class.</p>

<p>Stack: pandas, scikit-learn, seaborn, matplotlib.</p>

<hr>

<h2>Indian house prices</h2>

<p>Regression on the Kaggle <a href="https://www.kaggle.com/datasets/anmolkumar/house-price-prediction-challenge">House Price Prediction Challenge</a> train split (29,451 listings). Kaggle's test file has no prices, so I score a 20% holdout from train.</p>

<p>Fit on <code>log1p(price)</code> and report rupees. Features are size, BHK, city, who posted it, RERA, resale, under construction. <strong>₹/sqft is not a feature</strong> — that number <em>is</em> the price.</p>

<p>After cleaning (28,711 rows, median asking price ₹61 lakh):</p>

<table>
  <thead>
    <tr>
      <th>Model</th>
      <th>MAE (₹ lakh)</th>
      <th>Median AE</th>
      <th>R²</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Median dummy</td>
      <td>57.6</td>
      <td>28.6</td>
      <td>—</td>
    </tr>
    <tr>
      <td>Ridge</td>
      <td>30.8</td>
      <td>13.6</td>
      <td>0.65</td>
    </tr>
    <tr>
      <td>Random forest</td>
      <td>29.3</td>
      <td>11.7</td>
      <td>0.67</td>
    </tr>
    <tr>
      <td><strong>Gradient boosting</strong></td>
      <td><strong>28.5</strong></td>
      <td><strong>12.1</strong></td>
      <td><strong>0.71</strong></td>
    </tr>
  </tbody>
</table>

<p>Optional Streamlit form: <code>streamlit run app.py</code> in that folder.</p>

<p>Stack: pandas, scikit-learn, seaborn, matplotlib, streamlit.</p>

<hr>

<h2>Stella Bot</h2>

<p>A rule-based voice script. Google speech-to-text in, <code>pyttsx3</code> out. It opens a handful of sites, reads two Wikipedia sentences, tells a joke from a list, speaks the time, or launches VS Code if the path in <code>Stella.py</code> is right.</p>

<p>This is <strong>not</strong> a model. It matches keywords. I keep it here because it lives next to the other two in my GitHub.</p>

<pre><code>python -m pip install -r requirements.txt
python Stella.py</code></pre>

<p>Needs a microphone and internet for recognition.</p>

<hr>

<h2>Tech stack across all three</h2>

<table>
  <thead>
    <tr><th>Layer</th><th>Tools</th></tr>
  </thead>
  <tbody>
    <tr><td>Language</td><td>Python 3</td></tr>
    <tr><td>Data</td><td>pandas, NumPy</td></tr>
    <tr><td>Modeling</td><td>scikit-learn (LogisticRegression, RandomForest, GradientBoosting, Ridge)</td></tr>
    <tr><td>Visualization</td><td>matplotlib, seaborn</td></tr>
    <tr><td>App framework</td><td>Streamlit (house price predictor)</td></tr>
    <tr><td>Voice (Stella Bot)</td><td>speech_recognition, pyttsx3, wikipedia</td></tr>
    <tr><td>Notebook</td><td>Jupyter</td></tr>
    <tr><td>Persistence</td><td>joblib</td></tr>
  </tbody>
</table>

<hr>

<h2>Layout</h2>

<pre><code>README.md                              this file
hotel-churn-prediction/                cancellation classifier
indian-house-price-prediction/         house price regressor + Streamlit
stella-bot/                            voice assistant</code></pre>

<p>Drop each child repo into the matching folder (or leave them as separate GitHub repos and treat this file as an index).</p>

<hr>

<h2>License</h2>

<p>Code is MIT unless a child README says otherwise. Hotel and house data come from their public extracts (see each <code>data/README.md</code>).</p>
