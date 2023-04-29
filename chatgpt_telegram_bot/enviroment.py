import os

from dotenv import load_dotenv


load_dotenv()

TELEGRAM_TOKEN = str(os.getenv("TELEGRAM_TOKEN"))
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")

# Telegram ApplicationBuilder
CONNECT_TIMEOUT = float(os.getenv("CONNECT_TIMEOUT"))  # type: ignore[arg-type]
READ_TIMEOUT = float(os.getenv("READ_TIMEOUT"))  # type: ignore[arg-type]
WRITE_TIMEOUT = float(os.getenv("WRITE_TIMEOUT"))  # type: ignore[arg-type]

# OpenAI client
API_CLIENT_TIMEOUT = int(os.getenv("API_CLIENT_TIMEOUT"))  # type: ignore[arg-type]
