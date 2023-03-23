import logging
import telegram

from fastapi import FastAPI

from telegram.error import NetworkError
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from pydantic import BaseModel

from enviroment import TELEGRAM_TOKEN
from utils import send_request


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

bot = telegram.Bot(token=TELEGRAM_TOKEN)
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()


async def handle_message(update, context):
    print("\033[91m HERE \033[0m")
    message = update.message.text
    # try:
    #     response = await send_request(message)
    # except NetworkError as exc:
    #     print("\033[91m ERROR: \033[0m", exc)

    response = "Hello, I'm your bot"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)


if __name__ == '__main__':

    application.add_handler(handler)
    application.run_polling()


# TODO: Add inline mode
