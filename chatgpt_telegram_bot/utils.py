from telegram import Chat, Update, User


def get_user_id(update: Update) -> int:
    assert isinstance(update.effective_user, User)
    return update.effective_user.id


def get_chat_id(update: Update) -> int:
    assert isinstance(update.effective_chat, Chat)
    return update.effective_chat.id
