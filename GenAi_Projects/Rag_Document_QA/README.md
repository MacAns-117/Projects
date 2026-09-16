<h1>Multi-Doc RAG Q&amp;A with Citations</h1>

<p>
  <img src="https://img.shields.io/badge/projects-1-blue?style=flat-square" alt="1 project">
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/langchain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" alt="LangChain">
  <img src="https://img.shields.io/badge/chromadb-FF6F00?style=flat-square&logo=chroma&logoColor=white" alt="ChromaDB">
  <img src="https://img.shields.io/badge/groq-F55036?style=flat-square&logo=groq&logoColor=white" alt="Groq">
  <img src="https://img.shields.io/badge/streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Live Demo">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

<p>A Retrieval-Augmented Generation system that lets users ask natural-language questions across multiple PDF documents and get answers with citations back to the source documents and page numbers. Includes OCR fallback for scanned PDFs.</p>

<h2>Live Demo</h2>

<p>🔗 <strong><a href="https://projects-wktkeuxu6u3nqmz9vdyith.streamlit.app/">projects-wktkeuxu6u3nqmz9vdyith.streamlit.app</a></strong></p>

<p>Try it now — upload any PDF (text-based or scanned) and ask questions. No login required.</p>

<h2>What it does</h2>

<ul>
  <li>User uploads 1-10 PDFs via the Streamlit UI</li>
  <li>System chunks and embeds them into a persistent Chroma vector database</li>
  <li>OCR fallback (Tesseract) automatically handles scanned/image-based PDFs</li>
  <li>User asks a question in natural language via chat interface</li>
  <li>System retrieves the top-K most relevant chunks via cosine similarity</li>
  <li>LLM generates an answer grounded in retrieved context, with inline citations like <code>[doc1.pdf, p.3]</code></li>
  <li>Anti-hallucination: honestly says "I don't know" when context doesn't contain the answer</li>
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
    <tr><td>Vector DB</td><td>Chroma 0.5.20 (persistent)</td></tr>
    <tr><td>Embeddings</td><td>HuggingFace all-MiniLM-L6-v2 (384-dim, local, free)</td></tr>
    <tr><td>LLM</td><td>Groq openai/gpt-oss-120b (free tier)</td></tr>
    <tr><td>PDF parsing</td><td>pdfplumber 0.11.4</td></tr>
    <tr><td>OCR fallback</td><td>Tesseract + pytesseract + pdf2image</td></tr>
    <tr><td>UI</td><td>Streamlit 1.40.1</td></tr>
    <tr><td>Deployment</td><td>Streamlit Community Cloud (free)</td></tr>
  </tbody>
</table>

<h2>Tested end-to-end</h2>

<p>Tested on the live deployment with a real resume PDF. Sample Q&amp;A:</p>

<table>
  <thead>
    <tr><th>Question</th><th>Answer (abbreviated)</th><th>Citations</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>What is this document about?</td>
      <td>The document is a professional portfolio/resume for Maqsood Ansari that outlines his data-analytics and machine-learning projects, software-development work, certifications...</td>
      <td>[1][2][4]</td>
    </tr>
    <tr>
      <td>What is his latest experience?</td>
      <td>His most recent role is as a Software Engineer at Aptsol Global Tech Pvt, working from 02/2024 to 10/2024 in Hyderabad, India.</td>
      <td>[1][3]</td>
    </tr>
    <tr>
      <td>List his work</td>
      <td>Software Engineer at Aptsol + 5 projects (Request Management System, Instagram User Analytics, Playstore Apps Analysis, House Price Prediction, Task Manager Application) with full descriptions.</td>
      <td>[1][2][3][4]</td>
    </tr>
  </tbody>
</table>

<h2>How to run locally</h2>

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
├── app.py                          # Streamlit UI (multi-PDF upload + chat)
├── src/
│   ├── pdf_loader.py               # PDF loading + parsing (with OCR fallback)
│   ├── chunker.py                  # RecursiveCharacterTextSplitter (1000-char, 200-overlap)
│   ├── embeddings.py               # HuggingFace all-MiniLM-L6-v2 (cached)
│   ├── vectorstore.py              # Persistent Chroma DB with citation metadata
│   ├── retriever.py                # Similarity search with RetrievedChunk objects
│   ├── llm.py                      # Groq openai/gpt-oss-120b wrapper (cached)
│   └── chain.py                    # End-to-end RAG with 6-rule citation prompt
├── data/
│   ├── sample_pdfs/                # Add your test PDFs here
│   └── README.md
├── notebooks/
│   └── exploration.ipynb           # Interactive end-to-end test
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md</code></pre>

<h2>Status</h2>

<p>✅ <strong>Live</strong> — deployed on Streamlit Community Cloud.</p>

<p>The RAG pipeline is fully functional — PDF upload, OCR fallback for scanned docs, semantic retrieval (top-8), LLM answer generation with citations, and a Streamlit chat UI. Auto-redeploys on every push to the main branch.</p>

<h2>License</h2>

<p>MIT</p>
