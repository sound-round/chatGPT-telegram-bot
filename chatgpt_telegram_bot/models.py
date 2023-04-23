from pydantic import BaseModel, root_validator

from .tokenizer import tokenize


class Message(BaseModel):
    role: str
    content: str
    tokens: int | None

    @root_validator()
    def count_tokens(cls, values):
        # TODO: add role to context: role = values.get("role")?
        content = values.get("content")
        tokens = tokenize(content)
        values["tokens"] = tokens
        return values
