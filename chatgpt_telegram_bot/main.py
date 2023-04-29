import logging
import telegram
import httpx

from telegram import Update
from telegram.error import NetworkError
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from .enviroment import TELEGRAM_TOKEN, CONNECT_TIMEOUT, READ_TIMEOUT, WRITE_TIMEOUT
from .openai_client import OpenAIClient
from .context.context_manager import ContextManager


TYPING = 1


API_client = OpenAIClient()
context_manager = ContextManager()


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        response = await handle_request_to_API(text)
    except httpx.ConnectTimeout:
        print("\033[91m ERROR: connection timed out \033[0m")
        response = "exception: connection timed out"
    except NetworkError as exc:
        print("\033[91m Telegream network exception: \033[0m", exc.message)
        response = f"Telegream network exception: {exc.message}"
    except httpx.TimeoutException as exc:
        print("\033[91m API_client Timeout exception: \033[0m", exc)
        response = f"API_client Timeout exception:: {exc}"
    except httpx.HTTPError as exc:
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


async def reset_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="The context of this dialog has been reset.",
    )
    context_manager.reset_dialog()


async def set_default_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context_manager.reset_system_prompt()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="The system prompt has been set to default:\n"
        f"{context_manager.system_prompt}",
    )


async def start_setting_custom_system_prompt(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Please, enter your system prompt."
    )
    return TYPING


async def finish_setting_custom_system_prompt(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    prompt = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"The system prompt has been set to:\n{prompt}",
    )
    context_manager.set_custom_prompt(prompt)
    return ConversationHandler.END


async def show_current_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"The system prompt is:\n{context_manager.system_prompt}",
    )


if __name__ == "__main__":
    try:
        reset_handler = CommandHandler("reset", reset_dialog)
        reset_prompt_handler = CommandHandler("set_default_prompt", set_default_prompt)
        show_prompt_handler = CommandHandler("show_current_prompt", show_current_prompt)
        message_handler = MessageHandler(
            filters.TEXT & ~filters.COMMAND, handle_message
        )

        custom_prompt_handler = ConversationHandler(
            entry_points=[
                CommandHandler(
                    "set_custom_system_prompt", start_setting_custom_system_prompt
                )
            ],
            states={TYPING: []},
            fallbacks=[
                MessageHandler(filters.ALL, finish_setting_custom_system_prompt)
            ],
        )

        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        application = (
            ApplicationBuilder()
            .token(TELEGRAM_TOKEN)
            .connect_timeout(CONNECT_TIMEOUT)
            .read_timeout(READ_TIMEOUT)
            .write_timeout(WRITE_TIMEOUT)
            .build()
        )
        application.add_handlers(
            [
                custom_prompt_handler,
                reset_handler,
                reset_prompt_handler,
                show_prompt_handler,
                message_handler,
            ]
        )
        application.run_polling()
    except Exception as exc:
        print("\033[91m MAIN EXCEPTION: \033[0m", exc)


# TODO:

# resolve problem on running:
# 'api.telegram.org' does not appear to be an IPv4 or IPv6 address
# (maybe set telegram.error.TimedOut)

# context to json
# inline mode
