from core.openapi.services import get_channel_main_topics
from core.slack import ExtraArguments, SlackHelper


async def command_topics(
    helper: SlackHelper, extra_arguments: ExtraArguments, *args, **kwargs
) -> None:
    messages = await helper.get_conversation_history(arguments=extra_arguments)
    response = await get_channel_main_topics(messages)
    initial_text = "The main topics in the chat are: "

    topic_text = [f"• *{topic}*\n\n" for topic in response]

    blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": initial_text},
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": topic_text,
            },
        },
    ]

    await helper.say(text=initial_text, blocks=blocks)
