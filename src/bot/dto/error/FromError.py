class FromNotPresentError(Exception):
    def __init__(self, message: str, chat_id: str):
        self.__chat_id = chat_id
        self.__message = message
        super().__init__(message)

    def get_chat_id(self):
        return self.__chat_id

    def get_message(self):
        return self.__message


class FromIdNotPresentError(Exception):
    def __init__(self, message: str, chat_id: str):
        self.__chat_id = chat_id
        self.__message = message
        super().__init__(message)

    def get_chat_id(self):
        return self.__chat_id

    def get_message(self):
        return self.__message
