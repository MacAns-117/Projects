"""Report writer — LLM only. Prompt fields are passed as a dict (no Passthrough bug)."""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate

from src.llm import get_llm

REPORT_WRITER_PROMPT = """You write a short answer from tool output. You do not have the table.

Rules:
1. Lead with the answer to the question.
2. Use only numbers that appear in the data findings. Do not invent any.
3. If a chart was generated, mention it in one clause (title / axes).
4. If findings say the table cannot answer, say that.
5. Keep it under 6 sentences.

Data findings:
{data_findings}

Chart:
{chart_description}

Question:
{question}

Summary:"""


def write_report(
    question: str,
    data_findings: str,
    chart_description: str = "",
    llm=None,
) -> str:
    if llm is None:
        llm = get_llm()
    prompt = ChatPromptTemplate.from_template(REPORT_WRITER_PROMPT)
    message = (prompt | llm).invoke(
        {
            "question": question,
            "data_findings": data_findings or "No data analysis was run.",
            "chart_description": chart_description or "No chart generated.",
        }
    )
    return message.content
