from app.llm import llm
from app.schemas.planner import ResearchPlan


# Create an LLM that returns structured ResearchPlan output
planner_llm = llm.with_structured_output(
    ResearchPlan
)


def create_research_plan(question: str) -> ResearchPlan:

    prompt = f"""
You are an expert AI research planner.

Break the user's research question into
3 to 6 focused research questions.

Rules:

1. Each sub-question must investigate a different aspect.
2. Avoid duplicate questions.
3. Focus only on information necessary to answer
   the original question.
4. Do not answer the questions.
5. Return only the research plan.

User question:

{question}
"""

    return planner_llm.invoke(prompt)
