"""LangGraph: router → analyst and/or viz → report writer."""

from __future__ import annotations

from typing import Optional, TypedDict

import pandas as pd
import plotly.graph_objects as go
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph

from src.agents.data_analyst import create_data_analyst
from src.agents.report_writer import write_report
from src.agents.viz_agent import create_viz_agent
from src.chart_buffer import ChartBuffer
from src.llm import get_llm
from src.routing import classify_intent, route_after_data_analyst, route_after_router

ROUTER_PROMPT = """Classify the user question for a tabular analytics assistant.

Reply with ONLY one word:
data — numbers, stats, counts, comparisons, filters, SQL-like asks
viz — they want a chart / plot / graph and not a numeric write-up
both — analysis AND a chart
general — greeting, capabilities, or off-topic

Question: {question}

Category:"""


class AgentState(TypedDict):
    question: str
    intent: str
    data_findings: str
    chart_fig: Optional[go.Figure]
    chart_description: str
    final_answer: str


def create_orchestrator(df: pd.DataFrame, llm=None, chart_buffer: ChartBuffer | None = None):
    if llm is None:
        llm = get_llm()
    buffer = chart_buffer or ChartBuffer()

    router_chain = ChatPromptTemplate.from_template(ROUTER_PROMPT) | llm
    analyst = create_data_analyst(df, llm)
    viz = create_viz_agent(df, buffer, llm)

    def router_node(state: AgentState) -> dict:
        response = router_chain.invoke({"question": state["question"]})
        return {"intent": classify_intent(response.content)}

    def data_analyst_node(state: AgentState) -> dict:
        result = analyst.invoke({"input": state["question"]})
        return {"data_findings": result.get("output", "")}

    def viz_agent_node(state: AgentState) -> dict:
        context = state["question"]
        if state.get("data_findings"):
            context += f"\n\nData findings so far:\n{state['data_findings']}"
        result = viz.invoke({"input": context})
        fig, caption = buffer.snapshot()
        desc = caption or result.get("output", "")
        return {"chart_description": desc, "chart_fig": fig}

    def report_writer_node(state: AgentState) -> dict:
        if state.get("intent") == "general" and not state.get("data_findings"):
            findings = (
                "This assistant answers questions about the currently loaded CSV "
                "using pandas tools and optional SQL (table name `data`). "
                "It can filter, aggregate, correlate, and draw charts. "
                "It only knows this table."
            )
        else:
            findings = state.get("data_findings") or "No data analysis was run."
        summary = write_report(
            question=state["question"],
            data_findings=findings,
            chart_description=state.get("chart_description") or "",
            llm=llm,
        )
        return {"final_answer": summary}

    workflow = StateGraph(AgentState)
    workflow.add_node("router", router_node)
    workflow.add_node("data_analyst", data_analyst_node)
    workflow.add_node("viz_agent", viz_agent_node)
    workflow.add_node("report_writer", report_writer_node)
    workflow.set_entry_point("router")
    workflow.add_conditional_edges(
        "router",
        route_after_router,
        {
            "data_analyst": "data_analyst",
            "viz_agent": "viz_agent",
            "report_writer": "report_writer",
        },
    )
    workflow.add_conditional_edges(
        "data_analyst",
        route_after_data_analyst,
        {"viz_agent": "viz_agent", "report_writer": "report_writer"},
    )
    workflow.add_edge("viz_agent", "report_writer")
    workflow.add_edge("report_writer", END)
    return workflow.compile()


def empty_state(question: str) -> AgentState:
    return {
        "question": question,
        "intent": "",
        "data_findings": "",
        "chart_fig": None,
        "chart_description": "",
        "final_answer": "",
    }
