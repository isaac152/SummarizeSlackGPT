import logging
import time
from typing import Optional

from slack_bolt.context.say.async_say import AsyncSay
from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_client import AsyncWebClient

from core.slack.models import ExtraArguments, Message

logger = logging.getLogger()


class SlackHelper:
    def __init__(self, client: AsyncWebClient, say: AsyncSay, bot_id: str) -> None:
        self._client = client
        self.say = say
        self._bot_id = bot_id

    async def _parse_messages(
        self, messages: list[dict], parse_thread: Optional[bool] = False
    ) -> list[Message]:
        parsed_messages = []

        for message in messages:
            raw_text = message.get("text")
            thread_id = message.get("thread_ts")
            thread_messages = []
            if not message.get("client_msg_id") or self._bot_id in raw_text:
                continue

            if thread_id and not parse_thread:
                channel = self.say.channel
                thread_response = await self._client.conversations_replies(
                    channel=channel, ts=thread_id, limit=200
                )
                thread_messages = await self._parse_messages(
                    thread_response.get("messages"), True
                )

            parsed_message = Message(
                user=message.get("user"),
                time_stamp=message.get("ts"),
                blocks=message.get("blocks", []),
                team=message.get("team"),
                raw_text=raw_text,
                thread_messages=thread_messages,
            )
            parsed_messages.append(parsed_message)
        return parsed_messages

    async def get_conversation_history(
        self, channel: Optional[str] = "", arguments: Optional[ExtraArguments] = None
    ) -> list[Message]:
        channel = channel or self.say.channel
        date_timestamp = (
            time.mktime(arguments.date.timetuple()) if arguments.date else None
        )
        logger.info(date_timestamp)

        try:
            result = await self._client.conversations_history(
                limite=200,
                channel=channel,
                include_all_metadata=True,
                oldest=date_timestamp,
            )

            raw_messages = result.get("messages")
            if not raw_messages:
                raise Exception("Custom exception")

            messages = await self._parse_messages(raw_messages)
            messages = [
                message.get_message_data() for message in messages if message.is_valid()
            ]
            return
        except SlackApiError as e:
            logger.error(f"Slack error: {e}")

        raise Exception("same custom exception")
