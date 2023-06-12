from core.openapi.services import get_channel_messages_feelings
from core.slack import ExtraArguments, SlackHelper


async def command_feelings(
    helper: SlackHelper, extra_arguments: ExtraArguments, *args, **kwargs
) -> None:
    messages = await helper.get_conversation_history(arguments=extra_arguments)
    response = await get_channel_messages_feelings(messages)

    feelings_blocks = []

    for feelings_data in response:
        feeling_text = f"• *Topic*: {feelings_data.get('topic')}  \n\n  *General feeling*: {feelings_data.get('feeling')} \n\n "
        feelings_blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": feeling_text,
                },
            }
        )

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "I can notice the following feelings :eyes: ",
            },
        },
        *feelings_blocks,
    ]
    await helper.say(text="The feelings of the last messages are: ", blocks=blocks)
