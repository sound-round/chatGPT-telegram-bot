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

    cm = ContextManager(message)
    
    assert cm
    assert cm.max_context_tokens == MAX_CONTEXT_TOKENS
    assert cm.context == [message]
    assert cm.tokens == 6

    cm.max_context_tokens = 13
    message2 = Message(role="user", content="This is an user prompt.")
    assert message2.tokens == 5
    
    messages = cm.add_message(message2)
    assert cm.tokens == 11
    assert cm.context == [message, message2]
    assert messages == [
        {'role': 'system', 'content': 'This is a system prompt.'},
        {'role': 'user', 'content': 'This is an user prompt.'},
    ]

    message3 = Message(role="assistent", content="This is an assistent prompt.")
    assert message3.tokens == 6

    messages = cm.add_message(message3)
    assert cm.tokens == 12
    assert cm.context == [message, message3]
    assert messages == [
        {'role': 'system', 'content': 'This is a system prompt.'},
        {'role': 'assistent', 'content': 'This is an assistent prompt.'},
    ]
