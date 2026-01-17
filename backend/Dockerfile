FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /app/backend

RUN apk add --no-cache tzdata

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --no-dev

COPY src ./src

COPY entrypoint.dev.sh entrypoint.sh ./
RUN chmod +x entrypoint.dev.sh entrypoint.sh