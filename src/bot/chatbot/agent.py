from llm_svc import invoke_model
from .state import State


def agent_node(state: State):
    print(f"Invoking agent with prompt: {state.prompt}")
    response = invoke_model(state.prompt)
    print(f"Agent response: {response}")
    state.response = response
    return state
