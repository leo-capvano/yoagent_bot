class ChatNotPresentError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ChatIdNotPresentError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
