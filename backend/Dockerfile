FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /app

RUN apk add --no-cache tzdata

COPY pyproject.toml uv.lock .python-version /app/
RUN uv sync

COPY src /app/
RUN .venv/bin/python manage.py makemigrations
RUN .venv/bin/python manage.py migrate