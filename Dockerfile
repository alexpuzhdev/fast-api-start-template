FROM python:3.12-slim

ENV POETRY_VERSION=2.1.4 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential postgresql-client \
    && pip install "poetry==${POETRY_VERSION}" \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root

COPY app ./app
COPY docker/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
