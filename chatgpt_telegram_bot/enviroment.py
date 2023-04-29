import os

from dotenv import load_dotenv


load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")

# telegram ApplicationBuilder
CONNECT_TIMEOUT = float(os.getenv("CONNECT_TIMEOUT"))
READ_TIMEOUT = float(os.getenv("READ_TIMEOUT"))
WRITE_TIMEOUT = float(os.getenv("WRITE_TIMEOUT"))
