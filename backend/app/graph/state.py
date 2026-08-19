from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class ResearchState(TypedDict):

    messages: Annotated[
        list[AnyMessage],
        add_messages
    ]

    question: str

    research_plan: list[str]

    research_results: list[dict]

    sources: list[dict]

    analysis: dict

    report: dict