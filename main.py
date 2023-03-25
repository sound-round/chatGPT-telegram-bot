import logging
import telegram
import httpx

# from fastapi import FastAPI

from telegram.error import NetworkError
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from pydantic import BaseModel

from enviroment import TELEGRAM_TOKEN
from openai_client import OpenAIClient


API_client = OpenAIClient()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

bot = telegram.Bot(token=TELEGRAM_TOKEN)
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()


async def handle_message(update, context):
    message = update.message.text
    try:
        response = await API_client.send_request(message)
    except httpx.ConnectTimeout as exc:
        print("\033[91m ERROR: connection timed out \033[0m")
        response = f"exception: connection timed out"
    except (NetworkError, httpx.HTTPError) as exc:
        print("\033[91m ERROR: \033[0m", exc)
        response = f"exception: {exc}"
    except Exception as exc:
        print("\033[91m COMMON EXCEPTION: \033[0m", exc)
        response = f"exception: {exc}"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)


if __name__ == '__main__':
    application.add_handler(handler)
    application.run_polling()


# TODO:
# resolve problem on running
# context
# commands
# inline mode
