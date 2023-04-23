import pytest

from .context_manager import ContextManager, MAX_CONTEXT_TOKENS
from ..models import Message


def test_context_manager():
    prompt = "This is a system prompt."
    message = Message(role="system", content=prompt)

    assert message
    assert message.role == "system"
    assert message.content == prompt
    assert message.tokens
    assert message.tokens == 6

    # notice that the prompt itself has been passed to ContextManager
    cm = ContextManager(prompt)
    
    assert cm
    assert cm.max_context_tokens == MAX_CONTEXT_TOKENS
    assert cm.context == [message]
    assert cm.tokens == 6

    cm.max_context_tokens = 13
    message2 = "This is an user prompt."
    
    messages = cm.add_message(role="user", text=message2)
    assert cm.tokens == 11
    assert cm.context == [message, Message(role="user", content=message2)]
    assert messages == [
        {"role": "system", "content": "This is a system prompt."},
        {"role": "user", "content": "This is an user prompt."},
    ]

    message3 = "This is an assistant prompt."

    messages = cm.add_message(role="assistant", text=message3)
    assert cm.tokens == 12
    assert cm.context == [
        message,
        Message(role="assistant", content=message3),
    ]
    assert messages == [
        {"role": "system", "content": "This is a system prompt."},
        {"role": "assistant", "content": "This is an assistant prompt."},
    ]

    cm.reset(system_prompt="new system prompt")

    assert cm.tokens == 4
    assert cm.context[0].content == "new system prompt"
