FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /app/backend

RUN apk add --no-cache tzdata

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync

COPY entrypoint.dev.sh entrypoint.sh ./
RUN chmod +x entrypoint.dev.sh entrypoint.sh

COPY src ./src