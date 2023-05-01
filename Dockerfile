FROM python:3.10.11-slim-buster

# RUN apt update
# RUN apt install python3 -y

ARG ENVIROMENT, TELEGRAM_TOKEN, OPENAI_TOKEN
# COPY ./ ./

# ENV PYTHONFAULTHANDLER=1 \
#   PYTHONUNBUFFERED=1 \
#   PYTHONHASHSEED=random \
#   PIP_NO_CACHE_DIR=off \
#   PIP_DISABLE_PIP_VERSION_CHECK=on \
#   PIP_DEFAULT_TIMEOUT=100 \
#   POETRY_VERSION=1.0.0

ENV CONNECT_TIMEOUT=30 \
  READ_TIMEOUT=30 \
  WRITE_TIMEOUT=30 \
  API_CLIENT_TIMEOUT=45 \
  TELEGRAM_TOKEN=$TELEGRAM_TOKEN \
  OPENAI_TOKEN=$OPENAI_TOKEN \
  ENVIROMENT=$ENVIROMENT \
  POETRY_HOME="/opt/poetry"

ENV PATH="$POETRY_HOME/bin:$PATH"


# # System deps:
# RUN pip install "poetry"

# Install Poetry
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN apt-get remove -y --purge curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
# RUN curl -sSL https://install.python-poetry.org | python3 - && \
#   chmod +x $HOME/.poetry/bin/poetry && \
#   $HOME/.poetry/bin/poetry config virtualenvs.create false

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$ENVIROMENT" == production && echo "--no-dev") --no-interaction --no-ansi

COPY . /app
RUN poetry shell
CMD ["poetry", "run", "python", "-m", "chatgpt_telegram_bot.main"]
