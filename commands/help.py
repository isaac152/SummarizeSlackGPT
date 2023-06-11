from core.slack import ExtraArguments, SlackHelper


async def command_help(
    helper: SlackHelper, extra_arguments: ExtraArguments, *args, **kwargs
) -> None:
    await helper.say(str(extra_arguments))
