from core.slack import ExtraArguments, SlackHelper


async def command_help(
    helper: SlackHelper, extra_arguments: ExtraArguments, *args, **kwargs
) -> None:
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Nice to meet you, i am the SummaryGPT. My dutty is summary and reports the conversations in a public channel :grin:",
            },
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "These are the commands you can use"},
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "• *summary*: Get a channel conversation summary  \n Optional arguments: Date | User mentions \n\n *Examples*:  \n\n  - @SummaryGPT summary 11/06/2023   \n\n  - @SummaryGPT summary  @JustPepe \n\n  - @SummaryGPT summary 11/06/2023 @Pepethefrog @Someone",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "• *topics*: Get the main topics of a channel conversation \n Optional arguments: Date \n\n *Examples*:  \n\n  - @summary topics 11/05/2023  \n\n",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "• *feelings*: Get the general feeling of a conversation \n Optional arguments: Date | User mentions \n\n *Examples*:  \n\n  - @SummaryGPT feelings 11/06/2023   \n\n  - @SummaryGPT feelings  @JustSadPepe \n\n  - @SummaryGPT feelings 11/06/2023 @Pepethefrog @Someone",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "• *report*: Get a simple report of a channel conversation \n Optional arguments: Date \n\n *Examples*:  \n\n  - @summary report 11/05/2023  \n\n ",
            },
        },
    ]
    await helper.say(text="You need some help? Take a look", blocks=blocks)
