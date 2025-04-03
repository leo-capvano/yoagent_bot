from langgraph.constants import START, END
from langgraph.graph import StateGraph

from .agent import agent_node
from .state import State

main_graph_builder = StateGraph(State)

# nodes
main_graph_builder.add_node("agent_node", agent_node)

# edges
main_graph_builder.add_edge(START, "agent_node")
main_graph_builder.add_edge("agent_node", END)

main_graph = main_graph_builder.compile()
