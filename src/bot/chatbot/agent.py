import os

from langchain_community.tools import BraveSearch
from langgraph.graph import MessagesState

from llm_svc import invoke_model


def should_continue(state: MessagesState):
    if len(state["messages"]) > 0 and state["messages"][-1].tool_calls:
        return "tools"
    return "end"


def agent_node(state: MessagesState):
    print(f"Invoking agent with messages: {state["messages"]}")
    response_message = invoke_model(state["messages"], agent_tools)
    print(f"Agent response: {response_message}")
    state["messages"] += [response_message]
    return state


agent_tools = []

if brave_api_key := os.getenv("BRAVE_API_KEY", default=None):
    brave_search_tool = BraveSearch.from_api_key(api_key=brave_api_key, search_kwargs={"count": 3})
    agent_tools.append(brave_search_tool)
