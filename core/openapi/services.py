import ast
import json
import logging

import openai

from core.openapi.constants import (
    FEELINGS_FORMAT,
    GPT_MODEL,
    REPORT_FORMAT,
    SUMMARIZE_FORMAT,
    TOPICS_FORMAT,
)
from core.openapi.exceptions import ChatGPTServiceException, ChatGPTWrongJson
from settings import OPENAI_KEY

logger = logging.getLogger("services.chatgpt")

openai.api_key = OPENAI_KEY


def format_message(message: str, role: str) -> list:
    return [
        {"role": "system", "content": role},
        {"role": "user", "content": message},
    ]


def format_response_to_json(raw_questionnaire: str) -> list[dict]:

    try:
        return json.loads(raw_questionnaire)
    except json.JSONDecodeError as e:
        logger.error("Cannot convert into json. Trying evaluation")
        logger.error(e)
    try:
        return ast.literal_eval(raw_questionnaire)
    except Exception as e:
        logger.error("Raising exception")
        logger.error(e)
        raise ChatGPTWrongJson()


async def get_channel_summary(messages: list[str]) -> list[dict]:
    try:
        logger.info(
            f"Starting chatgpt summarize request {len(messages)} messages in total"
        )
        completion = await openai.ChatCompletion.acreate(
            model=GPT_MODEL,
            messages=format_message(
                message=f"""
                Based on the following list of messages {messages} where each message is represented like: "<User>:Message"
                You will identify the language from messages and responde with that language.
                If you can't recognize the language, assume it's English.
                You are going to summarize the conversation.
                You are going to use following format {SUMMARIZE_FORMAT}
                - Replace (topic) for a topic of the conversation
                - Replace (summarize) for the summarize of that topic in particular
                Only respond with the format supplied with a valid json and nothing else.
                Do no add or create or add any topic/idea that is not int he conversation
                """,
                role="You are a very talent team manager who wants to summary the main topics",
            ),
        )
        response = completion.choices[0].message.content

        if "(topic)" in response:
            return await get_channel_summary(messages)

        return format_response_to_json(f"[{response}]")
    except openai.error.RateLimitError:
        logger.error(f"Max rate limit:  {len(messages)} amount of messages")

    raise ChatGPTServiceException()


async def get_channel_messages_feelings(messages: list[str]) -> list[dict]:
    try:
        logger.info(
            f"Starting chatgpt request feelings {len(messages)} messages in total"
        )
        completion = await openai.ChatCompletion.acreate(
            model=GPT_MODEL,
            messages=format_message(
                message=f"""
                Based on the following list of messages {messages} where each message is represented like: "<User>:Message"
                You will identify the language from messages and responde with that language.
                If you can't recognize the language, assume it's English.
                You are going to identify the feelings in the conversation based on topics.
                You are going to use following format {FEELINGS_FORMAT}
                Do no add or create or add any topic/idea that is not int he conversation
                - Replace (topic) for a topic of the conversation
                - Replace (feeling) for the general feeling of that topic in particular
                Only respond with the format supplied with a valid json and nothing else.
                """,
                role="You are a very talent team manager who wants to identify how your team is feeling about the work",
            ),
        )
        response = completion.choices[0].message.content

        if "(topic)" in response:
            return await get_channel_messages_feelings(messages)

        return format_response_to_json(f"[{response}]")
    except openai.error.RateLimitError:
        logger.error(f"Max rate limit:  {len(messages)} amount of messages")

    raise ChatGPTServiceException()


async def get_channel_main_topics(messages: list[str]) -> list[str]:
    try:
        logger.info(
            f"Starting chatgpt request  topics {len(messages)} messages in total"
        )
        completion = await openai.ChatCompletion.acreate(
            model=GPT_MODEL,
            messages=format_message(
                message=f"""
                Based on the following list of messages {messages} where each message is represented like: "<User>:Message"
                You will identify the language from messages and responde with that language.
                If you can't recognize the language, assume it's English.
                You are going to summarize the main topics of the conversation.
                You are going to use following format {TOPICS_FORMAT}
                - Replace topic for the 5 most importants topics of the conversation.
                If you cant find 5 main topics, just write as you can.
                Do no add or create or add any topic/idea that is not int he conversation
                Only respond with the format supplied with a valid json and nothing else.
                """,
                role="You are a very talent team manager who wants to summary the main topics",
            ),
        )
        response = completion.choices[0].message.content
        if "(topic)" in response:
            return await get_channel_summary(messages)

        return format_response_to_json(response)
    except openai.error.RateLimitError:
        logger.error(f"Max rate limit:  {len(messages)} amount of messages")

    raise ChatGPTServiceException()


async def get_channel_report(messages: list[str]) -> list[dict]:
    try:
        logger.info(
            f"Starting chatgpt request report {len(messages)} messages in total"
        )

        topics = await get_channel_main_topics(messages)
        topics = ",".join(topics)

        completion = await openai.ChatCompletion.acreate(
            model=GPT_MODEL,
            messages=format_message(
                message=f"""
                Based on the following list of messages {messages} where each message is represented like: "<User>:Message"
                You will identify the language from messages and responde with that language.
                If you can't recognize the language, assume it's English.

                You are going to identify the feelings in the conversation for the following topics {topics} for each user.
                You are going to use following format {REPORT_FORMAT}
                - Replace (topic) for each topic suplied
                - Replace (user) for the user
                - Replace (feeling) for the user feeling in that specific topic.
                - Replace (confort) for the confort about that feeling, where 100 is very confort and 0 is disconfort
                Only respond with the format supplied and nothing else.

                If a user doesnt talk or know about the topic, use "neutral" as feeling and 50% as confort
                Do no add or create or add any topic/idea that is not int he conversation
                """,
                role="You are a very talent team manager who wants to create a report of your team status",
            ),
        )
        response = completion.choices[0].message.content

        if "(topic)" in response:
            return await get_channel_summary(messages)

        return format_response_to_json(f"[{response}]")
    except openai.error.RateLimitError:
        logger.error(f"Max rate limit:  {len(messages)} amount of messages")
    raise ChatGPTServiceException()
