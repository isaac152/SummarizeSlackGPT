from core.slack import ExtraArguments, SlackHelper


async def command_report(
    helper: SlackHelper, extra_arguments: ExtraArguments, *args, **kwargs
) -> None:
    await helper.get_conversation_history(arguments=extra_arguments)
