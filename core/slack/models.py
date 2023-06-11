import logging
import re
from datetime import datetime

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
