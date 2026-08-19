from pydantic import BaseModel, Field


class ResearchAnalysis(BaseModel):

    key_findings: list[str] = Field(
        description="The most important findings discovered from the research."
    )

    comparisons: list[str] = Field(
        description="Important comparisons between the researched subjects."
    )

    recommendation: str = Field(
        description="The final recommendation based on the research evidence."
    )

    reasoning: str = Field(
        description="Explain the reasoning behind the recommendation."
    )