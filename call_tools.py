"""Demonstrating a tool call with LangChain Ollama integration."""

from typing import List

from langchain.messages import AIMessage
from langchain.tools import tool
from langchain_ollama import ChatOllama


@tool
def validate_user(user_id: int, addresses: List[str]) -> bool:
    """Validate user using historical addresses.

    Args:
        user_id (int): the user ID.
        addresses (List[str]): Previous addresses as a list of strings.
    """
    return True


llm = ChatOllama(
    model="ministral-3:8b",
    validate_model_on_init=True,
    temperature=0,
).bind_tools([validate_user])

result = llm.invoke(
    "Could you validate user 123? They previously lived at "
    "123 Fake St in Boston MA and 234 Pretend Boulevard in "
    "Houston TX."
)

if isinstance(result, AIMessage) and result.tool_calls:
    for tool_call in result.tool_calls:
        print(tool_call)
        tool_result = validate_user.invoke(input=tool_call["args"])
        print(f"Tool Result: {tool_result}")
