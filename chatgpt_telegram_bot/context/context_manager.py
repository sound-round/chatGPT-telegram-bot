from ..models import Message


MAX_CONTEXT_TOKENS: int = 3400


class ContextManager:
    max_context_tokens: int = MAX_CONTEXT_TOKENS
    context: "list[Message]" = []
    tokens: int = 0

    def __init__(self, system_prompt: str):
        start_prompt = Message(role="system", content=system_prompt)
        self.context.append(start_prompt)
        self.tokens += start_prompt.tokens

    def add_message(self, role: str, text: str):
        message = Message(role=role, content=text)
        context = [*self.context, message]
        tokens = self.tokens + message.tokens
        self.context = context
        self.tokens = tokens

        while tokens > self.max_context_tokens:
            context, tokens = self._delete_message()
            self.context = context
            self.tokens = tokens

        return self._proccess_context(self.context)

    def _delete_message(self):
        tokens = self.tokens - self.context[1].tokens
        context = [self.context[0], *self.context[2:]]

        self.context = context
        self.tokens = tokens
        return self.context, self.tokens

    def _proccess_context(self, context: "list[Message]"):
        return list(map(lambda message: {"role": message.role, "content": message.content}, context))
    
    def reset(self, system_prompt: Message):
        self.context = []
        self.tokens = 0

        start_prompt = Message(role="system", content=system_prompt)

        self.context.append(start_prompt)
        self.tokens += start_prompt.tokens