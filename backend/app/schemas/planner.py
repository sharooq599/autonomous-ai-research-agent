from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):
    sub_questions: list[str] = Field(
        description="3 to 6 focused research questions needed to answer the user's main question."
    )