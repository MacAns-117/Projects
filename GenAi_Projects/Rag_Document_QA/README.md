<h1>Multi-Doc RAG Q&amp;A with Citations</h1>

<p>A Retrieval-Augmented Generation system that lets users ask natural-language questions across multiple PDF documents and get answers with citations back to the source documents and page numbers.</p>

<h2>What it does</h2>

<ul>
  <li>User uploads 2-5 PDFs via the Streamlit UI</li>
  <li>System chunks and embeds them into a local Chroma vector database</li>
  <li>User asks a question in natural language</li>
  <li>System retrieves the most relevant chunks, sends them to an LLM (Groq Llama 3.1)</li>
  <li>Returns an answer with inline citations like <code>[doc1.pdf, p.3]</code></li>
  <li>Clicking a citation shows the source passage</li>
</ul>

<h2>Why this project</h2>

<p>After my Software Engineer role ended in October 2024, I made a deliberate decision to invest in GenAI/LLM skills. This project is the first of two GenAI applications I'm building to demonstrate production-quality RAG capability — the #1 in-demand GenAI skill in 2025-2026 job postings.</p>

<h2>Tech stack</h2>

<table>
  <thead>
    <tr><th>Layer</th><th>Tools</th></tr>
  </thead>
  <tbody>
    <tr><td>Language</td><td>Python 3.11</td></tr>
    <tr><td>Orchestration</td><td>LangChain 0.3.7</td></tr>
    <tr><td>Vector DB</td><td>Chroma 0.5.20 (local, persistent)</td></tr>
    <tr><td>Embeddings</td><td>HuggingFace all-MiniLM-L6-v2 (local, free)</td></tr>
    <tr><td>LLM</td><td>Groq Llama 3.1 8B (free tier)</td></tr>
    <tr><td>PDF parsing</td><td>pdfplumber 0.11.4</td></tr>
    <tr><td>UI</td><td>Streamlit 1.40.1</td></tr>
    <tr><td>Deployment</td><td>Hugging Face Spaces (planned)</td></tr>
  </tbody>
</table>

<h2>How to run</h2>

<pre><code># Clone the Projects repo
git clone https://github.com/MacAns-117/Projects.git
cd "Projects/GenAi_Projects/Rag_Document_QA"

# Create venv (Python 3.11)
conda create -n rag-qa python=3.11 -y
conda activate rag-qa

# Install deps
pip install -r requirements.txt

# Add your Groq API key
cp .env.example .env
# Edit .env and paste your GROQ_API_KEY (get one free at console.groq.com)

# Run the app
streamlit run app.py</code></pre>

<h2>Repo layout</h2>

<pre><code>Rag_Document_QA/
├── app.py                          # Streamlit UI
├── src/
│   ├── pdf_loader.py               # PDF loading + parsing
│   ├── chunker.py                  # Text splitting
│   ├── embeddings.py               # HuggingFace embeddings
│   ├── vectorstore.py              # Chroma setup + persistence
│   ├── retriever.py                # Retrieval logic
│   ├── llm.py                      # Groq LLM wrapper
│   └── chain.py                    # LangChain RAG chain
├── data/
│   ├── sample_pdfs/                # Add your test PDFs here
│   └── README.md
├── notebooks/
│   └── exploration.ipynb           # Dev notebook
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md</code></pre>

<h2>Status</h2>

<p>🚧 In development — scaffolding complete, building core RAG pipeline next.</p>

<h2>License</h2>

<p>MIT</p>