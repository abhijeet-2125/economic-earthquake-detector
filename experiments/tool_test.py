from langchain.tools import tool

@tool
def square_number(number: int) -> int:
    """
    Returns square of a number.
    """
    return number * number
print(square_number.invoke({"number": 5}))