import logging
import telegram
import httpx

# from fastapi import FastAPI
from telegram import Update
from telegram.error import NetworkError
from telegram.ext import ApplicationBuilder, MessageHandler, filters

from .enviroment import TELEGRAM_TOKEN
from .openai_client import OpenAIClient
from .context.context_manager import ContextManager
from .models import Message


SYSTEM_PROMPT = "You are a helpful assistant. Your name is Alfred." 


start_prompt = Message(role="system", content=SYSTEM_PROMPT)

API_client = OpenAIClient()
context_manager = ContextManager(start_prompt)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def handle_message(update: Update, context):
    text = update.message.text
    try:
        response = await handle_request_to_API(text)
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

async def handle_request_to_API(text):
    messages = context_manager.add_message(role="user", text=text)

    print("\033[91m messages \033[0m", messages)

    response = await API_client.send_request(messages)
    context_manager.add_message(role="assistant", text=response)
    return response



if __name__ == '__main__':
    handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(handler)
    application.run_polling()


# TODO:
# resolve problem on running: 'api.telegram.org' does not appear to be an IPv4 or IPv6 address (maybe set telegram.error.TimedOut)
# context
# commands
# inline mode
