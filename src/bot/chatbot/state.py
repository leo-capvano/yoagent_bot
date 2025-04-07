from pydantic import BaseModel


class State(BaseModel):
    prompt: str
    response: str = ""
