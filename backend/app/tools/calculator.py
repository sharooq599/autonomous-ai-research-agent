def calculator(expression: str) -> str:

    """
    Calculate a mathematical expression.
    """

    try:

        resut = eval(expression, {"__builtins__": {}}, {})

        return str(resut)

    except Exception as e:
        return f"Calculation error: {str(e)}"