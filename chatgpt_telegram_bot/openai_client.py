import httpx

from .enviroment import OPENAI_TOKEN


CONFIG = {
    "model": "gpt-3.5-turbo",
    "max_tokens": 500,
    "temperature": 0.5,
    "n": 1,
    # 'stop': '.\n',
}
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_TOKEN}",
}
ROLE = "user"
TIMEOUT = 30
URL = "https://api.openai.com/v1/chat/completions"


class OpenAIClient:
    def __init__(
        self,
        url: str = URL,
        headers: dict[str, str] = HEADERS,
        timeout: int = TIMEOUT,
        config=CONFIG,
    ):
        self.url = url
        self.headers = headers
        self.timeout = timeout
        self.config = config

    async def send_request(self, messages: dict[str, str]):
        # system_prompt = {'role': "system", 'content': SYSTEM_PROMPT}
        # user_message = {'role': "user", 'content': text}
        # messages = [system_prompt, user_message]
        request_params = dict(messages=messages, **self.config)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.url,
                headers=self.headers,
                json=request_params,
                timeout=self.timeout,
            )

            response.raise_for_status()
            response_json = response.json()
            return response_json["choices"][0]["message"]["content"]
