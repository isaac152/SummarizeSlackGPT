from slack_bolt.context.say.async_say import AsyncSay


async def command_feelings(say: AsyncSay, *args, **kwargs) -> None:
    await say(str(*args))
