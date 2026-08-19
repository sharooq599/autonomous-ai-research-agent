from app.llm import llm_with_tools
from app.tools.registry import tools_by_name


def research_question(question: str):

    messages = [
        {
            "role": "user",
            "content": f"""
Research the following question carefully:

{question}

Use the available web search tool when
current or factual information is required.

Use the search results to produce an
accurate research answer.
"""
        }
    ]

    sources = []

    # ============================================================
    # FIRST LLM CALL
    # ============================================================

    response = llm_with_tools.invoke(
        messages
    )

    messages.append(
        response
    )

    # ============================================================
    # EXECUTE TOOL CALLS
    # ============================================================

    for tool_call in response.tool_calls:

        tool_name = tool_call["name"]

        tool_args = tool_call["args"]

        tool = tools_by_name.get(
            tool_name
        )

        if tool is None:
            continue

        result = tool(
            **tool_args
        )

        # --------------------------------------------------------
        # Extract sources
        # --------------------------------------------------------

        if isinstance(result, dict):

            content = result.get(
                "content",
                ""
            )

            tool_sources = result.get(
                "sources",
                []
            )

            sources.extend(
                tool_sources
            )

        else:

            content = str(result)

        # --------------------------------------------------------
        # Add tool result to conversation
        # --------------------------------------------------------

        messages.append(
            {
                "role": "tool",
                "content": content,
                "tool_call_id": tool_call["id"]
            }
        )

    # ============================================================
    # FINAL LLM CALL
    # ============================================================

    final_response = llm_with_tools.invoke(
        messages
    )

    return {
        "question": question,

        "answer": final_response.content,

        "sources": sources
    }

if __name__ == "__main__":

    result = research_question(
        "What is LangGraph and how is it used for production AI agents?"
    )

    print("\n============================")
    print("RESEARCH RESULT")
    print("============================")

    print(result)