FROM python:3.12-slim

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    apt-get update && apt-get install -y --no-install-recommends make build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ARG POETRY_VERSION=1.8.2

RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade pip \
    && pip install poetry==${POETRY_VERSION}

COPY .env pyproject.toml poetry.lock Makefile ./
COPY bot bot

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# CMD ["/bin/bash", "-c", "poetry run python bot/main.py"]
CMD ["make", "run"]
