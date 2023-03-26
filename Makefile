t test:
	poetry run pytest -vv

make dev:
	poetry run python -m chatgpt_telegram_bot.main
