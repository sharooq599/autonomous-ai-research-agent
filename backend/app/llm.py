from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

from app.tools.registry import tools

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)



llm_with_tools = llm.bind_tools(tools)