from typing import List

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from secrets_manager_svc import get_secret

GPT_O3_MINI = "o3-mini-2025-01-31"
GPT_3_5_TURBO = "gpt-3.5-turbo-0125"


def invoke_model(messages: List[BaseMessage], tools: list) -> BaseMessage:
    llm_api_key = get_secret("llm_api_key")
    llm = ChatOpenAI(model=GPT_3_5_TURBO, api_key=llm_api_key)
    if tools:
        llm = llm.bind_tools(tools)
    response = llm.invoke(messages)
    return response
