from app.tools.web_search import web_search
from app.tools.calculator import calculator

# All available tools
tools = [
    web_search,
    calculator
]

# Map tool name -> actual Python function
tools_by_name = {
    "web_search": web_search,
    "calculator": calculator
}
