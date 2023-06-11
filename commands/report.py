from slack_bolt.context.say.async_say import AsyncSay


async def command_report(say: AsyncSay, *args, **kwargs) -> None:
    await say(str(*args))
