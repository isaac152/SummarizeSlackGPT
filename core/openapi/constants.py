GPT_MODEL = "gpt-3.5-turbo"

SUMMARIZE_FORMAT = """
    {
        "topic":(topic),
        "summarize":(summarize)
    },
"""
FEELINGS_FORMAT = """
    {
        "topic":(topic),
        "feeling":(feeling)
    },
"""

TOPICS_FORMAT = """
    ["topic","topic","topic","topic"]
"""
REPORT_FORMAT = """
    {
        "topic":(topic),
        "users_data":{
            [
                "user":(user),
                "feeling":(feeling),
                "confort":"(confort)%",
            ],
        },
    },
"""
