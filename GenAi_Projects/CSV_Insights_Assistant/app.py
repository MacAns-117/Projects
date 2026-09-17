"""Streamlit UI. Upload any CSV; hotel_bookings.csv is the default sample."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

from src.config import DEFAULT_CSV, LLM_MODEL, MAX_ROWS, MAX_UPLOAD_MB
from src.data_loader import load_csv_buffer, load_default
from src.memory import ConversationMemory
from src.orchestrator import create_orchestrator, empty_state
from src.schema import schema_card


st.set_page_config(page_title="CSV Insights Assistant", layout="wide")


def _init():
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationMemory()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "df" not in st.session_state:
        st.session_state.df = None
    if "source_name" not in st.session_state:
        st.session_state.source_name = None
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = None
    if "orch_key" not in st.session_state:
        st.session_state.orch_key = None


def _load_default():
    df = load_default()
    st.session_state.df = df
    st.session_state.source_name = df.attrs.get("source_name", DEFAULT_CSV.name)
    st.session_state.orchestrator = None
    st.session_state.orch_key = None


def _ensure_orchestrator():
    key = (st.session_state.source_name, len(st.session_state.df), tuple(st.session_state.df.columns))
    if st.session_state.orchestrator is None or st.session_state.orch_key != key:
        st.session_state.orchestrator = create_orchestrator(st.session_state.df)
        st.session_state.orch_key = key


_init()

with st.sidebar:
    st.header("Table")
    uploaded = st.file_uploader(
        f"CSV (max {MAX_UPLOAD_MB} MB, {MAX_ROWS:,} rows)",
        type=["csv"],
    )
    if uploaded is not None:
        token = (uploaded.name, uploaded.size)
        if st.session_state.get("upload_token") != token:
            try:
                df = load_csv_buffer(uploaded, filename=uploaded.name)
                st.session_state.df = df
                st.session_state.source_name = uploaded.name
                st.session_state.upload_token = token
                st.session_state.orchestrator = None
                st.session_state.chat_history = []
                st.session_state.memory.clear()
            except Exception as exc:
                st.error(str(exc))
    elif st.session_state.df is None:
        try:
            _load_default()
        except Exception as exc:
            st.error(str(exc))
            st.stop()

    if st.button("Use hotel sample"):
        _load_default()
        st.session_state.chat_history = []
        st.session_state.memory.clear()
        st.session_state.upload_token = None
        st.rerun()

    df = st.session_state.df
    if df is not None:
        st.metric("Rows", f"{len(df):,}")
        st.metric("Columns", len(df.columns))
        st.caption(f"Source: {st.session_state.source_name}")
        st.caption(f"Model: {LLM_MODEL}")
        with st.expander("Schema"):
            st.text(schema_card(df))

    if st.button("Clear conversation"):
        st.session_state.memory.clear()
        st.session_state.chat_history = []
        st.rerun()


st.title("CSV Insights Assistant")
st.markdown(
    "Ask questions about the loaded table. Default sample is the "
    "Antonio et al. hotel bookings file (arrivals July 2015 – August 2017). "
    "Upload another CSV to swap the table."
)

if st.session_state.df is None:
    st.stop()

try:
    _ensure_orchestrator()
except Exception as exc:
    st.error(f"Could not start the agents: {exc}")
    st.info("Put GROQ_API_KEY in .env")
    st.stop()

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("chart") is not None:
            st.plotly_chart(msg["chart"], use_container_width=True)

question = st.chat_input("Ask about the current table…")
if question:
    st.session_state.chat_history.append({"role": "user", "content": question})
    st.session_state.memory.add_message("user", question)

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Working…"):
            memory_context = st.session_state.memory.get_context_string()
            full_input = question
            if memory_context:
                full_input = (
                    f"Previous conversation:\n{memory_context}\n\nNew question: {question}"
                )
            try:
                result = st.session_state.orchestrator.invoke(empty_state(full_input))
                answer = result.get("final_answer") or "No answer."
                chart = result.get("chart_fig")
                st.write(answer)
                if chart is not None:
                    st.plotly_chart(chart, use_container_width=True)
            except Exception as exc:
                answer = f"Error: {exc}"
                chart = None
                st.error(answer)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer, "chart": chart}
    )
    st.session_state.memory.add_message("assistant", answer)
