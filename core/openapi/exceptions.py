from core.exceptions import BaseServiceException


class ChatGPTServiceException(BaseServiceException):
    def __init__(self, msg="ChatGPT exception", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class ChatGPTWrongJson(ChatGPTServiceException):
    def __init__(self, *args, **kwargs):
        super().__init__("Wrong json format", *args, **kwargs)
