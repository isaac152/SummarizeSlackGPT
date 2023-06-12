import logging

from slack_bolt.async_app import AsyncApp
from slack_bolt.context.say.async_say import AsyncSay

import settings
from commands import command_handler
from core.slack import ExtraArguments, SlackHelper
from core.slack.constants import GENERIC_CONNECTION_ERROR, MISSING_COMMAND_ERROR

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = AsyncApp(
    token=settings.SLACK_BOT_TOKEN, signing_secret=settings.SLACK_SIGNING_SECRET
)


@app.event("app_mention")
async def get_command(event: dict, say: AsyncSay) -> None:
    event_text = event.get("text", "").split()
    if not event_text or len(event_text) < 2:
        error_message = (
            GENERIC_CONNECTION_ERROR if not event_text else MISSING_COMMAND_ERROR
        )
        return await say(error_message)

    bot_data = await app.client.auth_test()
    bot_id = bot_data.get("user_id", "")

    command = event_text[1].lower().strip()
    extra_args = ExtraArguments(event_text[2:])

    slack_helper = SlackHelper(app.client, say, bot_id)

    return await command_handler(command, slack_helper, extra_args)
