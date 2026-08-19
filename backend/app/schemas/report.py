from pydantic import BaseModel, Field


class ResearchReport(BaseModel):

    title: str = Field(
        description="A clear title for the research report."
    )

    executive_summary: str = Field(
        description="A concise summary of the most important conclusions."
    )

    key_findings: list[str] = Field(
        description="The most important findings from the research."
    )

    detailed_analysis: str = Field(
        description="A detailed explanation of the research and analysis."
    )

    recommendation: str = Field(
        description="The final recommendation based on the evidence."
    )

    sources: list[str] = Field(
        description="Citation references such as [1], [2], [3]."
    )
