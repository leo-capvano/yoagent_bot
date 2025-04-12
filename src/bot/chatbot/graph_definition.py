from langgraph.constants import START, END
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

from .agent import agent_node, agent_tools, should_continue

main_graph_builder = StateGraph(MessagesState)

# nodes
main_graph_builder.add_node("agent_node", agent_node)
main_graph_builder.add_node("tools", ToolNode(tools=agent_tools))

# edges
main_graph_builder.add_edge(START, "agent_node")
main_graph_builder.add_edge("agent_node", END)
main_graph_builder.add_conditional_edges("agent_node", should_continue, {
    "tools": "tools",
    "end": END
})
main_graph_builder.add_edge("tools", "agent_node")

main_graph = main_graph_builder.compile()
