from slack_bolt.async_app import AsyncApp
from slack_bolt.context.say.async_say import AsyncSay

import settings
from commands import command_handler

app = AsyncApp(
    token=settings.SLACK_BOT_TOKEN, signing_secret=settings.SLACK_SIGNING_SECRET
)

GENERIC_CONNECTION_ERROR = "There was a problem, try again"
MISSING_COMMAND_ERROR = "Please retry using a valid command"


@app.event("app_mention")
async def get_command(event: dict, say: AsyncSay) -> None:

    event_text = event.get("text", "").split()
    if not event_text:
        await say(GENERIC_CONNECTION_ERROR)
        return

    if len(event_text) < 2:
        await say(MISSING_COMMAND_ERROR)
        return

    command = event_text[1].lower().strip()
    extra_args = event_text[2:]

    await command_handler(command, say, extra_args)


if __name__ == "__main__":
    app.start(3000)
