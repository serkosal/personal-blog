FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /app

RUN apk add --no-cache tzdata

COPY pyproject.toml uv.lock .python-version /app/
RUN uv sync

COPY django-entrypoint.sh /app/
RUN chmod +x /app/django-entrypoint.sh 

COPY src /app/