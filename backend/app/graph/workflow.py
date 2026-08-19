from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from app.graph.state import ResearchState

from app.llm import llm_with_tools

from app.tools.registry import tools

from app.agents.planner import create_research_plan

from app.agents.researcher import research_question

from app.agents.analyzer import analyze_research

from app.agents.reporter import generate_report

from app.agents.source_manager import deduplicate_sources


# ============================================================
# PLANNER NODE
# ============================================================

def planner_node(state: ResearchState):

    question = state["question"]

    plan = create_research_plan(
        question
    )

    return {
        "research_plan": plan.sub_questions
    }


# ============================================================
# RESEARCHER NODE
# ============================================================

def research_node(state: ResearchState):

    research_plan = state["research_plan"]

    results = []

    sources = []

    for question in research_plan:

        result = research_question(
            question
        )

        results.append(
            result
        )

        sources.extend(
            result.get(
                "sources",
                []
            )
        )

    return {
        "research_results": results,
        "sources": sources
    }


# ============================================================
# SOURCE MANAGER NODE
# ============================================================

def source_manager_node(
    state: ResearchState
):

    sources = state.get(
        "sources",
        []
    )

    unique_sources = deduplicate_sources(
        sources
    )

    return {
        "sources": unique_sources
    }


# ============================================================
# ANALYZER NODE
# ============================================================

def analyzer_node(state: ResearchState):

    question = state["question"]

    research_results = state["research_results"]

    analysis = analyze_research(
        question,
        research_results
    )

    return {
        "analysis": analysis.model_dump()
    }


# ============================================================
# REPORTER NODE
# ============================================================

def reporter_node(state: ResearchState):

    question = state["question"]

    analysis = state["analysis"]

    sources = state["sources"]

    report = generate_report(
        question,
        analysis,
        sources
    )

    return {
        "report": report.model_dump()
    }


# ============================================================
# FINAL LLM NODE
# ============================================================

def call_llm(state: ResearchState):

    messages = state["messages"]

    report = state.get(
        "report",
        {}
    )

    if report:

        key_findings = "\n".join(
            f"- {item}"
            for item in report.get(
                "key_findings",
                []
            )
        )

        sources = "\n".join(
            f"[{source.get('id')}] "
            f"{source.get('title')} - "
            f"{source.get('url')}"
            for source in state.get(
                "sources",
                []
            )
        )

        report_text = f"""
Title:
{report.get("title", "")}


Executive Summary:
{report.get("executive_summary", "")}


Key Findings:

{key_findings}


Detailed Analysis:
{report.get("detailed_analysis", "")}


Recommendation:
{report.get("recommendation", "")}


Sources:

{sources}
"""

        messages = messages + [
            {
                "role": "system",
                "content": f"""
You are the final response generator.

The research system has completed:

- Planning
- Web research
- Source collection
- Source deduplication
- Analysis
- Report generation

Use the following report:

==================================================
RESEARCH REPORT
==================================================

{report_text}

==================================================

Citation rules:

1. Preserve citation numbers exactly.

2. Use citations like [1], [2], [3].

3. Only use a citation when it supports the claim.

4. Never invent citation numbers.

5. Never invent sources.

6. Do not mention internal agents.

7. Do not mention the internal workflow.

Return a professional final answer.
"""
            }
        ]

    response = llm_with_tools.invoke(
        messages
    )

    return {
        "messages": [response]
    }


# ============================================================
# TOOL NODE
# ============================================================

tool_node = ToolNode(
    tools
)


# ============================================================
# ROUTER
# ============================================================

def should_continue(
    state: ResearchState
):

    last_message = state["messages"][-1]

    if last_message.tool_calls:

        return "tools"

    return END


# ============================================================
# BUILD GRAPH
# ============================================================

builder = StateGraph(
    ResearchState
)


# ============================================================
# ADD NODES
# ============================================================

builder.add_node(
    "planner",
    planner_node
)

builder.add_node(
    "researcher",
    research_node
)

builder.add_node(
    "source_manager",
    source_manager_node
)

builder.add_node(
    "analyzer",
    analyzer_node
)

builder.add_node(
    "reporter",
    reporter_node
)

builder.add_node(
    "llm",
    call_llm
)

builder.add_node(
    "tools",
    tool_node
)


# ============================================================
# GRAPH EDGES
# ============================================================

builder.add_edge(
    START,
    "planner"
)

builder.add_edge(
    "planner",
    "researcher"
)

builder.add_edge(
    "researcher",
    "source_manager"
)

builder.add_edge(
    "source_manager",
    "analyzer"
)

builder.add_edge(
    "analyzer",
    "reporter"
)

builder.add_edge(
    "reporter",
    "llm"
)


# ============================================================
# LLM → TOOLS OR END
# ============================================================

builder.add_conditional_edges(
    "llm",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)


# ============================================================
# TOOLS → LLM
# ============================================================

builder.add_edge(
    "tools",
    "llm"
)


# ============================================================
# COMPILE GRAPH
# ============================================================

research_graph = builder.compile()