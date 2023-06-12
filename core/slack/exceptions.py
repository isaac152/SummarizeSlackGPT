from core.exceptions import BaseServiceException


class SlackServiceException(BaseServiceException):
    def __init__(self, msg="Slack Connection exception", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
