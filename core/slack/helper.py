from slack_bolt.context.say.async_say import AsyncSay
from slack_sdk.web.async_client import AsyncWebClient


class SlackHelper:
    def __init__(self, client: AsyncWebClient, say: AsyncSay) -> None:
        self.client = client
        self.say = say
