import httpx

from enviroment import OPENAI_TOKEN


#TODO: Refactor to handler with config
async def send_request(message):

    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://api.openai.com/v1/engine/<engine-id>/completions',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {OPENAI_TOKEN}',
            },
            json={
                'prompt': message,
                'max_tokens': 50,
                'temperature': 0.5,
                'n': 1,
                'stop': '.\n',
            },
        )

        response.raise_for_status()

        response_json = response.json()

        return response_json['choices'][0]['text']
