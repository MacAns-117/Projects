<h1>Projects</h1>

<p>Fourteen projects across four areas: GenAI, ML, analytics, and web. Each folder has its own README with numbers, plots, and how to run it. The three GenAI apps are deployed on Streamlit Community Cloud.</p>

<h2>GenAI Projects</h2>

<p>Three LLM apps: RAG over PDFs, a LangGraph CSV analyst, and a web research agent. All three have a Streamlit UI, a FastAPI wrapper, and tests that run in CI without API keys.</p>

<table>
  <thead>
    <tr><th>Project</th><th>What it is</th><th>Headline</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="./GenAi_Projects/Rag_Document_QA/"><strong>RAG Document Q&amp;A</strong></a></td>
      <td>Q&amp;A over uploaded PDFs with file + page citations. Hybrid BM25 + vector retrieval, cross-encoder rerank, OCR fallback</td>
      <td>Hit@8 77.3% (17/22), MRR 0.524 on a 24-question gold set · 62 tests · <a href="https://projects-wktkeuxu6u3nqmz9vdyith.streamlit.app/">Live demo</a></td>
    </tr>
    <tr>
      <td><a href="./GenAi_Projects/CSV_Insights_Assistant/"><strong>CSV Insights Assistant</strong></a></td>
      <td>LangGraph multi-agent: data analyst + viz + report writer on any CSV</td>
      <td>19/19 pandas gold checks · 88 tests · DuckDB SQL · Plotly charts · <a href="https://portfolio-wtvyr5raavdyaknbh4jml6.streamlit.app/">Live demo</a></td>
    </tr>
    <tr>
      <td><a href="./GenAi_Projects/AI_Research_Agent/"><strong>AI Research Agent</strong></a></td>
      <td>LangGraph pipeline: plans searches, reads pages (Tavily + trafilatura), writes a report citing [1], [2]</td>
      <td>70 tests · live web eval not run · <a href="https://projects-4vtuq5ybps6g3rgyzg84ry.streamlit.app/">Live demo</a></td>
    </tr>
  </tbody>
</table>

<h2>Data Science / ML Projects</h2>

<p>Three projects: classification, regression, and a voice assistant.</p>

<table>
  <thead>
    <tr><th>Project</th><th>What it is</th><th>Headline</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="./Data_Science(ML)_projects/Hotel_churn_rate/"><strong>Hotel Booking Cancellation</strong></a></td>
      <td>Binary classification on 87K hotel bookings, temporal split (train 2015–16, test 2017)</td>
      <td>Random forest ROC-AUC 0.815 on 2017 holdout · 10 plots (EDA + model)</td>
    </tr>
    <tr>
      <td><a href="./Data_Science(ML)_projects/Predicting_HP_Using_ADV_Ensamble_Techniques/"><strong>Indian House Price Prediction</strong></a></td>
      <td>Regression on 28.7K Indian listings; gradient boosting on log price, with ridge and random forest baselines</td>
      <td>R² 0.71 · median abs. error ₹12.1 lakh · local Streamlit form · started as MTech final-year project</td>
    </tr>
    <tr>
      <td><a href="./Data_Science(ML)_projects/Stella_Bot/"><strong>Stella Bot</strong></a></td>
      <td>Rule-based voice assistant in Python</td>
      <td>Speech-to-text + pyttsx3 · Wikipedia + browser + jokes</td>
    </tr>
  </tbody>
</table>

<h2>Data Analytics Projects</h2>

<p>Five analytics projects: content scoring, cosmetics similarity, IMDb analysis, an engagement drop investigation, and 14 Play Store queries. Same approach in each: pandas, then the same numbers again in SQLite.</p>

<table>
  <thead>
    <tr><th>Project</th><th>What it is</th><th>Headline</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="./Data_Analytics_Projects/Accenture_Data_analytics_and_Visualization/"><strong>Accenture / Social Buzz</strong></a></td>
      <td>Top 5 content categories by reaction score</td>
      <td>Animals 68,624 · pandas and SQL agree</td>
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
      <td><a href="./Data_Analytics_Projects/Playstore%20Apps%20Analysis%20%26%20Visualization/"><strong>Playstore Apps Analysis</strong></a></td>
      <td>14 assigned SQL questions on 9,648 apps</td>
      <td>GAME installs 13.9B (bucket floors) · revenue $291M</td>
    </tr>
  </tbody>
</table>

<h2>Django Projects</h2>

<p>Three Django apps: login and CRUD on SQLite, Bootstrap 5 on every page, console mail on the request app so SMTP is optional. Each has tests (<code>python manage.py test</code>).</p>

<table>
  <thead>
    <tr><th>Project</th><th>What it is</th><th>Headline</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="./Django_Projects/todo-task-manager/todo/"><strong>Task Manager</strong></a></td>
      <td>Task list per user, Bootstrap modals, status toggle</td>
      <td>6 tests · login_required on every page</td>
    </tr>
    <tr>
      <td><a href="./Django_Projects/request-management-system/smtp1/"><strong>Request Management System</strong></a></td>
      <td>Request form + staff approve/reject + SMTP email</td>
      <td>5 tests · status workflow (pending → approved / rejected)</td>
    </tr>
    <tr>
      <td><a href="./Django_Projects/hospital-management/HMS/"><strong>Hospital Management System</strong></a></td>
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
    <tr><td>GenAI</td><td>LangChain · LangGraph · Chroma · rank-bm25 · cross-encoder rerank · DuckDB · Tavily · Groq (gpt-oss-120b) or a local OpenAI-compatible server · MiniLM embeddings · Tesseract OCR · FastAPI</td></tr>
    <tr><td>ML</td><td>scikit-learn · pandas · NumPy · seaborn · Streamlit · SpeechRecognition · pyttsx3</td></tr>
    <tr><td>Analytics</td><td>pandas · SQLite · SQL · Excel · matplotlib · seaborn · scikit-learn (t-SNE) · python-pptx</td></tr>
    <tr><td>Web</td><td>Django · Bootstrap 5 · HTML/CSS · SQLite</td></tr>
    <tr><td>Testing</td><td>pytest for the GenAI apps (62 + 88 + 70, run in <a href="https://github.com/MacAns-117/Projects/actions/workflows/genai-tests.yml">GitHub Actions</a>) · Django test runner (6 + 5 + 6)</td></tr>
    <tr><td>Deployment</td><td>Streamlit Community Cloud (GenAI apps)</td></tr>
  </tbody>
</table>

<h2>Layout</h2>

<pre><code>Projects/
├── GenAi_Projects/
│   ├── Rag_Document_QA/              # RAG: hybrid retrieval, rerank, citations, OCR, FastAPI
│   ├── CSV_Insights_Assistant/       # Agents: LangGraph, DuckDB, Plotly, CSV upload
│   └── AI_Research_Agent/            # Agents: LangGraph, Tavily, cited reports
├── Data_Science(ML)_projects/
│   ├── Hotel_churn_rate/
│   ├── Predicting_HP_Using_ADV_Ensamble_Techniques/
│   └── Stella_Bot/
├── Data_Analytics_Projects/
│   ├── Accenture_Data_analytics_and_Visualization/
│   ├── Cosmetics_Ingredient_Analysis/
│   ├── IMDB_Movie_Analysis/
│   ├── Operations_Analytics_And_Investigating_Metric_Spike/
│   └── Playstore Apps Analysis &amp; Visualization/
├── Django_Projects/
│   ├── todo-task-manager/todo/        # Task Manager
│   ├── request-management-system/smtp1/  # Request Management System
│   └── hospital-management/HMS/       # Hospital Management System
└── README.md                          # this file</code></pre>

<h2>License</h2>

<p>There is no repo-wide LICENSE file. Only some project folders include one (the three GenAI apps, Hotel_churn_rate, and Predicting_HP_Using_ADV_Ensamble_Techniques); check a project's folder before reusing its code. Datasets keep their original sources' terms.</p>
