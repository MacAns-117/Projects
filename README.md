<h1>Projects</h1>

<p>Thirteen projects across four domains — analytics, ML, GenAI, and web. Each folder has its own README with numbers, plots, and how to run it. Two GenAI projects are deployed live.</p>

<h2>GenAI Projects</h2>

<p>Two production-style LLM applications — one RAG, one multi-agent. Both deployed on Streamlit Community Cloud.</p>

<table>
  <thead>
    <tr><th>Project</th><th>What it is</th><th>Headline</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="./GenAi_Projects/Rag_Document_QA/"><strong>RAG Document Q&amp;A</strong></a></td>
      <td>Multi-doc RAG with citations, OCR fallback, hybrid retrieval</td>
      <td>77.3% Hit@8 on 24-question gold set · <a href="https://projects-wktkeuxu6u3nqmz9vdyith.streamlit.app/">Live demo</a></td>
    </tr>
    <tr>
      <td><a href="./GenAi_Projects/Hotel_Insights_Assistant/"><strong>CSV Insights Assistant</strong></a></td>
      <td>LangGraph multi-agent: data analyst + viz + report writer on any CSV</td>
      <td>42 tests · 19/19 pandas eval · DuckDB SQL · Plotly charts</td>
    </tr>
  </tbody>
</table>

<h2>Data Science / ML Projects</h2>

<p>Three ML projects — classification, regression, and a voice assistant.</p>

<table>
  <thead>
    <tr><th>Project</th><th>What it is</th><th>Headline</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="https://github.com/MacAns-117/hotel-churn-prediction"><strong>Hotel Booking Cancellation</strong></a></td>
      <td>Binary classification on 87K hotel bookings, temporal split</td>
      <td>Random forest ROC-AUC 0.815 · 10 EDA plots · standalone repo</td>
    </tr>
    <tr>
      <td><a href="./Data_Science(ML)_projects/Predicting_HP_Using_ADV_Ensamble_Techniques/"><strong>Indian House Price Prediction</strong></a></td>
      <td>Regression with stacking, blending, bagging ensembles</td>
      <td>R² 0.71 · MAE ₹12.1 lakh · Streamlit app · MTech final-year project</td>
    </tr>
    <tr>
      <td><a href="./Data_Science(ML)_projects/Stella_Bot/"><strong>Stella Bot</strong></a></td>
      <td>Rule-based voice assistant in Python</td>
      <td>Speech-to-text + pyttsx3 · Wikipedia + browser + jokes</td>
    </tr>
  </tbody>
</table>

<h2>Data Analytics Projects</h2>

<p>Five analytics projects — content scoring, cosmetics similarity, IMDb analysis, an engagement drop investigation, and 14 Play Store queries. Same stack: pandas, then the same numbers in SQLite.</p>

<table>
  <thead>
    <tr><th>Project</th><th>What it is</th><th>Headline</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="./Data_Analytics_Projects/Accenture_Data_analytics_and_Visualization/"><strong>Accenture / Social Buzz</strong></a></td>
      <td>Top 5 content categories by reaction score</td>
      <td>Animals 68,624 — pandas and SQL agree</td>
    </tr>
    <tr>
      <td><a href="./Data_Analytics_Projects/Cosmetics_Ingredient_Analysis/"><strong>Cosmetics Ingredient Analysis</strong></a></td>
      <td>Similar formulas among dry-skin moisturizers</td>
      <td>190 × 2,233 one-hot · example cosine 0.535</td>
    </tr>
    <tr>
      <td><a href="./Data_Analytics_Projects/IMDB_Movie_Analysis/"><strong>IMDb Movie Analysis</strong></a></td>
      <td>What moves an IMDb score?</td>
      <td>4,916 titles · budget vs gross r = 0.627</td>
    </tr>
    <tr>
      <td><a href="./Data_Analytics_Projects/Operations_Analytics_And_Investigating_Metric_Spike/"><strong>Ops Analytics &amp; Metric Spike</strong></a></td>
      <td>Job-review ops + August engagement drop investigation</td>
      <td>Peak 1,443 engaged · −17.3% by 25 Aug</td>
    </tr>
    <tr>
      <td><a href="./Data_Analytics_Projects/Playstore_Apps_Analysis_%26_Visualization/"><strong>Playstore Apps Analysis</strong></a></td>
      <td>14 assigned SQL questions on 9,648 apps</td>
      <td>GAME installs 13.9B (bucket floors) · revenue $291M</td>
    </tr>
  </tbody>
</table>

<h2>Django Projects</h2>

<p>Three Django apps — login and CRUD on SQLite, Bootstrap 5 on every page, console mail on the request app so SMTP is optional. Each has tests.</p>

<table>
  <thead>
    <tr><th>Project</th><th>What it is</th><th>Headline</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="./Django_Projects/todo/"><strong>Task Manager</strong></a></td>
      <td>Task list per user, Bootstrap modals, status toggle</td>
      <td>6 tests · login_required on every page</td>
    </tr>
    <tr>
      <td><a href="./Django_Projects/smtp1/"><strong>Request Management System</strong></a></td>
      <td>Request form + staff approve/reject + SMTP email</td>
      <td>5 tests · status workflow (pending → approved / rejected)</td>
    </tr>
    <tr>
      <td><a href="./Django_Projects/HMS/"><strong>Hospital Management System</strong></a></td>
      <td>Patients and nurses in one app, shared dashboard</td>
      <td>2 models · 6 tests · one dashboard for both</td>
    </tr>
  </tbody>
</table>

<h2>Stack</h2>

<table>
  <thead>
    <tr><th>Layer</th><th>Tools</th></tr>
  </thead>
  <tbody>
    <tr><td>GenAI</td><td>LangChain · LangGraph · Chroma · DuckDB · Groq (gpt-oss-120b) · HuggingFace MiniLM · Tesseract OCR</td></tr>
    <tr><td>ML</td><td>scikit-learn · PyCaret · pandas · NumPy · Seaborn · Streamlit</td></tr>
    <tr><td>Analytics</td><td>pandas · SQLite · Power BI · SQL · Excel · matplotlib</td></tr>
    <tr><td>Web</td><td>Django · Bootstrap 5 · HTML/CSS · SQLite</td></tr>
    <tr><td>Testing</td><td>pytest (54 tests across GenAI + Django)</td></tr>
    <tr><td>Deployment</td><td>Streamlit Community Cloud · GitHub Pages</td></tr>
  </tbody>
</table>

<h2>Layout</h2>

<pre><code>Projects/
├── GenAi_Projects/
│   ├── Rag_Document_QA/              # RAG: hybrid retrieval, citations, OCR, FastAPI
│   └── Hotel_Insights_Assistant/      # Agents: LangGraph, DuckDB, Plotly, CSV upload
├── Data_Science(ML)_projects/
│   ├── Hotel_churn_rate/             # Link to standalone repo
│   ├── Predicting_HP_Using_ADV_Ensamble_Techniques/
│   └── Stella_Bot/
├── Data_Analytics_Projects/
│   ├── Accenture_Data_analytics_and_Visualization/
│   ├── Cosmetics_Ingredient_Analysis/
│   ├── IMDB_Movie_Analysis/
│   ├── Operations_Analytics_And_Investigating_Metric_Spike/
│   └── Playstore_Apps_Analysis_&_Visualization/
├── Django_Projects/
│   ├── todo/                          # Task Manager
│   ├── smtp1/                         # Request Management System
│   └── HMS/                           # Hospital Management System
└── README.md                          # this file</code></pre>

<h2>License</h2>

<p>MIT unless a child README says otherwise.</p>
