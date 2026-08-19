from app.llm import llm
from app.schemas.analysis import ResearchAnalysis


# LLM configured for structured analysis
analyzer_llm = llm.with_structured_output(
    ResearchAnalysis
)


def analyze_research(
    question: str,
    research_results: list[dict]
) -> ResearchAnalysis:

    research_text = "\n\n".join(
        f"""
Research Question:
{item["question"]}

Research Answer:
{item["answer"]}
"""
        for item in research_results
    )

    prompt = f"""
You are an expert research analyst.

The user asked:

{question}

Below are the research results collected by
the research agent:

{research_text}

Analyze the research carefully.

Your tasks:

1. Identify the most important findings.
2. Compare the relevant subjects.
3. Identify strengths and weaknesses.
4. Determine the best option when appropriate.
5. Base your recommendation only on the research.
6. Explain your reasoning clearly.
7. Do not invent information.

Return a structured research analysis.
"""

    return analyzer_llm.invoke(prompt)