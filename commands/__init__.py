from slack_bolt.context.say.async_say import AsyncSay

from commands.feelings import command_feelings
from commands.help import command_help
from commands.report import command_report
from commands.resume import command_resume
from commands.topics import command_topics


async def command_handler(command_name: str, say: AsyncSay, *args, **kwargs) -> None:
    commands = {
        "resume": command_resume,
        "topics": command_topics,
        "feelings": command_feelings,
        "report": command_report,
        "help": command_help,
    }
    return await commands.get(command_name, command_help)(say, *args, **kwargs)
