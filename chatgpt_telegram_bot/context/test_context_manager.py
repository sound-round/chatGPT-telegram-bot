from .context_manager import ContextManager, MAX_CONTEXT_TOKENS
from ..models import Message


def test_context_manager():
    message = "This is an user prompt."
    FIRST_USER_ID = 1
    SECOND_USER_ID = 2
    # message = Message(role="system", content=prompt)

    # assert message
    # assert message.role == "system"
    # assert message.content == prompt
    # assert message.tokens
    # assert message.tokens == 6

    cm = ContextManager()

    assert cm

    assert cm.context == {}

    cm.add_message(role="user", text=message, user_id=FIRST_USER_ID)

    assert cm.max_context_tokens == MAX_CONTEXT_TOKENS
    assert cm.context == {
        1: {
            "messages": [
                Message(
                    role="system", content="You are a helpful assistant.", tokens=6
                ),
                Message(role="user", content="This is an user prompt.", tokens=5),
            ],
            "tokens": 11,
        }
    }
    # assert cm.context[USER_ID]["tokens"] == 11

    cm.max_context_tokens = 13
    # message2 = "This is the second user prompt."

    # messages = cm.add_message(role="user", text=message2)
    # assert cm.tokens == 11
    # assert cm.context == [message, Message(role="user", content=message2)]
    # assert messages == [
    #     {"role": "system", "content": "This is a system prompt."},
    #     {"role": "user", "content": "This is an user prompt."},
    # ]

    assistant_message = "This is an assistant message."

    messages = cm.add_message(
        role="assistant", text=assistant_message, user_id=FIRST_USER_ID
    )
    # assert cm.tokens == 12
    assert cm.context == {
        1: {
            "messages": [
                Message(
                    role="system", content="You are a helpful assistant.", tokens=6
                ),
                Message(
                    role="assistant", content="This is an assistant message.", tokens=6
                ),
            ],
            "tokens": 12,
        }
    }

    # add message from second user
    second_user_message = "Hello! I'm a second user!"
    cm.add_message(role="user", text=message, user_id=SECOND_USER_ID)

    assert cm.context == {
        1: {
            "messages": [
                Message(
                    role="system", content="You are a helpful assistant.", tokens=6
                ),
                Message(
                    role="assistant", content="This is an assistant message.", tokens=6
                ),
            ],
            "tokens": 12,
        },
        2: {
            "messages": [
                Message(
                    role="system", content="You are a helpful assistant.", tokens=6
                ),
                Message(role="user", content="This is an user prompt.", tokens=5),
            ],
            "tokens": 11,
        },
    }

    custom_system_prompt = "You are Batman"
    cm.set_custom_prompt(custom_system_prompt, user_id=FIRST_USER_ID)

    assert cm.context[FIRST_USER_ID]["messages"][0].content == custom_system_prompt

    cm.reset_dialog(user_id=FIRST_USER_ID)

    assert cm.context == {
        1: {
            "messages": [Message(role="system", content="You are Batman", tokens=3)],
            "tokens": 3,
        },
        2: {
            "messages": [
                Message(
                    role="system", content="You are a helpful assistant.", tokens=6
                ),
                Message(role="user", content="This is an user prompt.", tokens=5),
            ],
            "tokens": 11,
        },
    }

    cm.reset_system_prompt(user_id=FIRST_USER_ID)

    assert (
        cm.context[FIRST_USER_ID]["messages"][0].content
        == "You are a helpful assistant."
    )
