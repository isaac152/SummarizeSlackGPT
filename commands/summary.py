from core.openapi.services import get_channel_summary
from core.slack import ExtraArguments, SlackHelper


async def command_summary(
    helper: SlackHelper, extra_arguments: ExtraArguments, *args, **kwargs
) -> None:
    messages = await helper.get_conversation_history(arguments=extra_arguments)
    response = await get_channel_summary(messages)

    initial_text = "Sure, this is the summary of the lastest messages"

    summary_block = []
    for summary_data in response:
        summary_text = f"• *Topic*: {summary_data.get('topic')}: {summary_data.get('summarize')} \n\n "

        summary_block.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": summary_text,
                },
            }
        )

    blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": initial_text},
        },
        *summary_block,
    ]

    await helper.say(text=initial_text, blocks=blocks)
