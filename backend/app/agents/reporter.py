from app.llm import llm
from app.schemas.report import ResearchReport


reporter_llm = llm.with_structured_output(
    ResearchReport
)


def generate_report(
    question: str,
    analysis: dict,
    sources: list[dict]
) -> ResearchReport:

    # ========================================================
    # FORMAT ANALYSIS
    # ========================================================

    key_findings = "\n".join(
        f"- {item}"
        for item in analysis.get(
            "key_findings",
            []
        )
    )

    comparisons = "\n".join(
        f"- {item}"
        for item in analysis.get(
            "comparisons",
            []
        )
    )

    recommendation = analysis.get(
        "recommendation",
        ""
    )

    reasoning = analysis.get(
        "reasoning",
        ""
    )

    # ========================================================
    # FORMAT SOURCES
    # ========================================================

    source_text = "\n".join(
        f"[{index + 1}] {source.get('title', '')} - "
        f"{source.get('url', '')}"
        for index, source in enumerate(sources)
    )

    # ========================================================
    # REPORT PROMPT
    # ========================================================

    prompt = f"""
You are an expert research report writer.

Create a professional research report answering:

{question}

Use ONLY the analysis and sources provided below.

============================================================
KEY FINDINGS
============================================================

{key_findings}


============================================================
COMPARISONS
============================================================

{comparisons}


============================================================
RECOMMENDATION
============================================================

{recommendation}


============================================================
REASONING
============================================================

{reasoning}


============================================================
SOURCES
============================================================

{source_text}


============================================================
REPORT REQUIREMENTS
============================================================

1. Create a clear and professional title.

2. Write an executive summary.

3. Present the most important findings.

4. Explain the detailed analysis clearly.

5. Include the recommendation.

6. Use source citations such as [1], [2], [3].

7. Only cite sources that actually support the claim.

8. Do not invent facts.

9. Do not invent citations.

10. Keep the report professional and easy to read.

11. Do not mention the internal AI agents.

12. Do not mention the internal workflow.

Return the structured research report.
"""

    return reporter_llm.invoke(
        prompt
    )