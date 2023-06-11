import logging
import re
from datetime import datetime
from typing import Optional

from dateutil.parser import parse

logger = logging.getLogger()


def validate_date(parameters: list[str]) -> datetime:
    for parameter in parameters:
        try:
            return parse(parameter)
        except ValueError:
            logger.error(f"Invalid date {parameter}")


def validate_user(parameters: list[str]) -> list[str]:
    regex = r"<@([A-Z0-9]+)>"
    parameters = " ".join(parameters)
    return re.findall(regex, parameters)


class ExtraArguments:
    def __init__(self, parameters: list) -> None:
        self.date = validate_date(parameters)
        self.user = validate_user(parameters)
        self._raw_parameters = parameters

    def __str__(self) -> str:
        return f"{self.date} {self.user}"


class Message:
    def __init__(
        self,
        user: str,
        time_stamp: str,
        blocks: list[dict],
        team: str,
        thread_messages: list,
        raw_text: str,
    ) -> None:
        self.user = user
        self.time_stamp = time_stamp
        self.blocks = blocks
        self.team = team
        self.raw_text = raw_text
        self.thread_messages = thread_messages

    def get_message_data(self) -> dict:
        return {
            "user": self.user,
            "message": self.raw_text,
            "extra_messages": self._parse_thread_messages(),
        }

    def _parse_thread_messages(self) -> list[dict]:
        parsed_thread = []
        for message in self.thread_messages[1:]:
            parsed_thread.append({"user": message.user, "message": message.raw_text})
        return parsed_thread

    def is_valid(self, users_id: Optional[list[str]] = None) -> bool:
        if not users_id:
            return True

        return True if self.user in users_id else False
