from commands.feelings import command_feelings
from commands.help import command_help
from commands.report import command_report
from commands.summary import command_summary
from commands.topics import command_topics
from core.slack.helper import SlackHelper
from core.slack.models import ExtraArguments


async def command_handler(
    command_name: str,
    helper: SlackHelper,
    extra_arguments: ExtraArguments,
    *args,
    **kwargs
) -> None:
    commands = {
        "summary": command_summary,
        "topics": command_topics,
        "feelings": command_feelings,
        "report": command_report,
        "help": command_help,
    }
    return await commands.get(command_name, command_help)(
        helper, extra_arguments, *args, **kwargs
    )
