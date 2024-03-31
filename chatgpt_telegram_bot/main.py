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
from .utils import get_chat_id, get_user_id


TYPING = 1
USER_ROLE = "user"
ASSISTANT_ROLE = "assistant"


API_client = OpenAIClient()
context_manager = ContextManager()


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message
    text = update.message.text

    user_id = get_user_id(update)
    try:
        response = await handle_request_to_API(text, user_id)
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
        print("\033[91m HTTP_ERROR: \033[0m", exc)
        response = f"exception: {exc}"
    except Exception as exc:
        print("\033[91m COMMON EXCEPTION: \033[0m", exc)
        response = f"exception: {exc}"

    await context.bot.send_message(chat_id=get_chat_id(update), text=response)
    return None


async def handle_request_to_API(text, user_id) -> str:
    messages = context_manager.add_message(role=USER_ROLE, text=text, user_id=user_id)
    response_text = await API_client.send_request(messages)
    context_manager.add_message(
        role=ASSISTANT_ROLE, text=response_text, user_id=user_id
    )
    return response_text


async def reset_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=get_chat_id(update),
        text="The context of this dialog has been reset.",
    )
    user_id = get_user_id(update)
    context_manager.reset_dialog(user_id)
    return None


async def set_default_prompt(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_id = get_user_id(update)
    context_manager.reset_system_prompt(user_id)
    await context.bot.send_message(
        chat_id=get_chat_id(update),
        text="The system prompt has been set to default:\n"
        f"{context_manager.context[user_id]['messages'][0].content}",
    )
    return None


async def start_setting_custom_system_prompt(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    await context.bot.send_message(
        chat_id=get_chat_id(update), text="Please, enter your system prompt."
    )
    return TYPING


async def finish_setting_custom_system_prompt(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    assert update.message
    prompt = update.message.text
    await context.bot.send_message(
        chat_id=get_chat_id(update),
        text=f"The system prompt has been set to:\n{prompt}",
    )
    context_manager.set_custom_prompt(prompt, user_id=get_user_id(update))
    return ConversationHandler.END


async def show_current_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = get_user_id(update)
    current_system_prompt = context_manager.context[user_id]["messages"][0].content
    await context.bot.send_message(
        chat_id=get_chat_id(update),
        text=f"The system prompt is:\n{current_system_prompt}",
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
# 1. add env vars on server properly

# context to json
# inline mode
