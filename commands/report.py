from core.openapi.services import get_channel_report
from core.slack import ExtraArguments, SlackHelper

USERS = {}


async def command_report(
    helper: SlackHelper, extra_arguments: ExtraArguments, *args, **kwargs
) -> None:
    messages = await helper.get_conversation_history(arguments=extra_arguments)
    response = await get_channel_report(messages)

    initial_text = "This is a report of the channel topic an feelings"

    users = {}
    for report_data in response:
        user_data = report_data.get("users_data", [{}])
        users_id = [user.get("user") for user in user_data]

        for user_id in users_id:
            if user_id in users:
                continue
            username = await helper.get_username(user_id)
            users[user_id] = username

    blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": initial_text}}]

    for report_data in response:
        users_data = report_data.get("users_data")
        user_data_text_parsed = []
        for user in users_data:
            username = users[user.get("user")]
            user_text = f"- *User*: {username} *Feeling*:{user.get('feeling')} *Confort*:{user.get('confort')}"
            user_data_text_parsed.append(user_text)

        user_block_text = "\n\n".join(user_data_text_parsed)
        block_text = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{report_data.get('topic')}*\n\n {user_block_text} ",
            },
        }

        blocks.append(block_text)

        blocks.append({"type": "divider"})

    await helper.say(text=initial_text, blocks=blocks)
