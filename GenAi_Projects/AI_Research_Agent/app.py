"""
Streamlit web app for the AI Research Agent.

Users type a research question, the app runs the full multi-agent
pipeline (Planner → Searcher → Synthesizer → Report Writer) and
displays the final research report with citations.

Prior conversation turns are passed into the orchestrator as `context`
so follow-up questions can resolve references.

Run with:
    streamlit run app.py
"""

from __future__ import annotations
import sys
from pathlib import Path

import streamlit as st

# Ensure src/ is importable
sys.path.insert(0, str(Path(__file__).parent))

from src.config import validate_config, LLM_MODEL
from src.orchestrator import create_orchestrator
from src.memory import ConversationMemory


# --- Page Config ---
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- Session State ---
def init_state():
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = None
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationMemory()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "last_sources" not in st.session_state:
        st.session_state.last_sources = []


init_state()


# --- Load Orchestrator (cached) ---
@st.cache_resource(show_spinner="Initializing AI Research Agent...")
def load_orchestrator():
    """Create orchestrator. Cached so it only runs once."""
    validate_config()
    orchestrator = create_orchestrator()
    return orchestrator


try:
    orchestrator = load_orchestrator()
except Exception as e:
    st.error(f"Failed to initialize: {e}")
    st.info("Make sure GROQ_API_KEY and TAVILY_API_KEY are set in .env")
    st.stop()


# --- Sidebar ---
with st.sidebar:
    st.header("🔬 AI Research Agent")

    st.subheader("How it works")
    st.caption("1. **Planner** decomposes your question into search queries")
    st.caption("2. **Searcher** runs web searches, extracts & summarizes pages")
    st.caption("3. **Synthesizer** cross-references findings")
    st.caption("4. **Report Writer** generates a structured report with citations")

    st.divider()

    st.subheader("Tech Stack")
    st.caption(f"• LLM: {LLM_MODEL}")
    st.caption("• LangGraph multi-agent orchestration")
    st.caption("• Tavily web search API")
    st.caption("• 4 agents: Planner, Searcher, Synthesizer, Report Writer")

    st.divider()

    # Show sources from the last research query
    if st.session_state.last_sources:
        st.subheader("📚 Last Sources")
        for i, s in enumerate(st.session_state.last_sources, 1):
            st.caption(f"[{i}] [{s.title}]({s.url})")

    st.divider()

    if st.button("🗑️ Clear Conversation"):
        st.session_state.memory.clear()
        st.session_state.chat_history = []
        st.session_state.last_sources = []
        st.rerun()


# --- Main Panel ---
st.title("🔬 AI Research Agent")
st.markdown(
    "Ask a research question. The agent will search the web, read multiple sources, "
    "cross-reference findings, and generate a structured report with citations."
)

st.divider()

# --- Chat Interface ---
st.subheader("💬 Ask a research question")

# Display chat history
for msg in st.session_state.chat_history:
    role = msg["role"]
    with st.chat_message(role):
        if msg.get("is_report"):
            st.markdown(msg["content"])
        else:
            st.write(msg["content"])

# Input box
question = st.chat_input("e.g., 'What are the latest advances in RAG evaluation?'")

if question:
    # Capture prior turns BEFORE adding the current question
    prior_context = st.session_state.memory.get_context_string()

    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": question})
    st.session_state.memory.add_message("user", question)

    # Display user message
    with st.chat_message("user"):
        st.write(question)

    # Generate research report
    with st.chat_message("assistant"):
        with st.spinner("🔬 Researching... This takes 2-4 minutes."):
            try:
                result = orchestrator.invoke({
                    "question": question,
                    "context": prior_context,
                    "search_queries": [],
                    "sources": [],
                    "sources_text": "",
                    "synthesis": "",
                    "final_report": "",
                })

                report = result.get("final_report", "Error: Could not generate report.")
                sources = result.get("sources", [])

                st.markdown(report)

                # Store sources for sidebar
                st.session_state.last_sources = sources

            except Exception as e:
                report = f"Sorry, I encountered an error: {str(e)}"
                st.error(report)

    # Add assistant message to history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": report,
        "is_report": True,
    })
    st.session_state.memory.add_message("assistant", report)
