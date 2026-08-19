from tavily import TavilyClient
from dotenv import load_dotenv
import os


load_dotenv()


tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def web_search(query: str) -> dict:
    """
    Search the web for current information.

    Returns both:
    - formatted research content
    - structured source information
    """

    response = tavily_client.search(
        query=query,
        max_results=5
    )

    results = []

    sources = []

    for result in response.get("results", []):

        title = result.get(
            "title",
            ""
        )

        url = result.get(
            "url",
            ""
        )

        content = result.get(
            "content",
            ""
        )

        # Content for the LLM
        results.append(
            f"""
Title: {title}

URL: {url}

Content:
{content}
"""
        )

        # Structured source
        sources.append(
            {
                "title": title,
                "url": url
            }
        )

    return {
        "content": "\n---\n".join(results),
        "sources": sources
    }