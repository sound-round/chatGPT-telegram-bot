from ..models import Message


MAX_CONTEXT_TOKENS: int = 3400
DEFAULT_PROMPT = "You are a helpful assistant."


class ContextManager:
    max_context_tokens: int = MAX_CONTEXT_TOKENS
    # TODO: implement context as a model
    context: dict = {}

    def start(self, user_id: int, system_prompt: str | None = None) -> None:
        start_prompt = Message(role="system", content=system_prompt or DEFAULT_PROMPT)
        self.context[user_id] = {}
        self.context[user_id]["messages"] = [start_prompt]
        self.context[user_id]["tokens"] = start_prompt.tokens
        return None

    def add_message(self, role: str, text: str, user_id: int) -> list[dict]:
        if not self.context.get(user_id):
            self.start(system_prompt=DEFAULT_PROMPT, user_id=user_id)
        message = Message(role=role, content=text)
        messages = [*self.context[user_id]["messages"], message]
        tokens = self.context[user_id]["tokens"] + message.tokens
        self.context[user_id]["messages"] = messages
        self.context[user_id]["tokens"] = tokens

        while self.context[user_id]["tokens"] > self.max_context_tokens:
            self._delete_message(user_id)

        return self._proccess_context(self.context[user_id]["messages"])

    def _delete_message(self, user_id: int) -> None:
        current_tokens = self.context[user_id]["tokens"]
        tokens_to_delete = self.context[user_id]["messages"][1].tokens
        tokens = current_tokens - tokens_to_delete
        messages = [
            self.context[user_id]["messages"][0],
            *self.context[user_id]["messages"][2:],
        ]

        self.context[user_id]["messages"] = messages
        self.context[user_id]["tokens"] = tokens
        return None

    def _proccess_context(self, context: "list[Message]"):
        return list(
            map(
                lambda message: {"role": message.role, "content": message.content},
                context,
            )
        )

    def reset_dialog(self, user_id: int):
        if not self.context or not self.context[user_id]["messages"]:
            return None
        start_prompt = self.context[user_id]["messages"][0]
        self.context[user_id]["messages"] = [start_prompt]
        self.context[user_id]["tokens"] = start_prompt.tokens
        return None

    def reset_system_prompt(self, user_id: int):
        current_system_prompt = self.context[user_id]["messages"][0]
        if current_system_prompt:
            default_system_prompt = Message(role="system", content=DEFAULT_PROMPT)
            self.context[user_id]["messages"][0] = default_system_prompt
            tokens_diff = default_system_prompt.tokens - current_system_prompt.tokens
            self.context[user_id]["tokens"] += tokens_diff
        return None

    def set_custom_prompt(self, prompt, user_id: int):
        current_system_prompt = self.context[user_id]["messages"][0]
        if current_system_prompt:
            custom_system_prompt = Message(role="system", content=prompt)
            self.context[user_id]["messages"][0] = custom_system_prompt
            tokens_diff = custom_system_prompt.tokens - current_system_prompt.tokens
            self.context[user_id]["tokens"] += tokens_diff
        return None
