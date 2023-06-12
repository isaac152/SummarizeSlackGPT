import os

from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET", "")

PORT = os.environ.get("PORT", 3000)

OPENAI_KEY = os.environ.get("OPENAI_KEY")
