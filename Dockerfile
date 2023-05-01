FROM python:3.10.11-slim-buster

ARG ENVIROMENT \
  TELEGRAM_TOKEN \
  OPENAI_TOKEN \
  CONNECT_TIMEOUT \
  READ_TIMEOUT \
  WRITE_TIMEOUT \
  API_CLIENT_TIMEOUT

ENV TELEGRAM_TOKEN $TELEGRAM_TOKEN \
  OPENAI_TOKEN $OPENAI_TOKEN \
  ENVIROMENT $ENVIROMENT \
  READ_TIMEOUT $READ_TIMEOUT \
  WRITE_TIMEOUT $WRITE_TIMEOUT \
  CONNECT_TIMEOUT $CONNECT_TIMEOUT \
  API_CLIENT_TIMEOUT $API_CLIENT_TIMEOUT

# ENV CONNECT_TIMEOUT=30 \
#   READ_TIMEOUT=30 \
#   WRITE_TIMEOUT=30 \
#   API_CLIENT_TIMEOUT=45 \
  # TELEGRAM_TOKEN=$TELEGRAM_TOKEN \
  # OPENAI_TOKEN=$OPENAI_TOKEN \
  # ENVIROMENT=$ENVIROMENT \
ENV POETRY_HOME="/opt/poetry"

ENV PATH="$POETRY_HOME/bin:$PATH"

# Install Poetry
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN apt-get remove -y --purge curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install --only main --no-interaction --no-ansi --no-root

COPY . /app
# RUN poetry shell
CMD ["poetry", "run", "python", "-m", "chatgpt_telegram_bot.main"]
