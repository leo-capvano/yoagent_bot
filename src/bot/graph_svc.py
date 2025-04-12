from langchain_core.messages import HumanMessage, SystemMessage

from chatbot.graph_definition import main_graph

system_message_pt = """
    You are an assistant that can use an online search tool to answer user questions. 
    You may choose to answer directly if you already know the answer.
    If you use the search tool, always include at least one link to the source in your response. 
    The link must be real and relevant.
    Be clear, concise, and accurate. If the topic is uncertain or evolving, let the user know.
    
    Format example:

    {response}
    Source: {link}
"""


def invoke_graph(user_prompt: str) -> str:
    graph_result = main_graph.invoke({"messages": [SystemMessage(content=system_message_pt),
                                                   HumanMessage(content=user_prompt)]})
    return graph_result["messages"][-1].content
