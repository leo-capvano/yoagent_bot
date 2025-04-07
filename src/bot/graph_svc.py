from chatbot.graph_definition import main_graph


def invoke_graph(user_prompt: str) -> str:
    graph_result = main_graph.invoke({"prompt": user_prompt})
    return graph_result["response"]
