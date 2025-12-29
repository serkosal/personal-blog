FROM ghcr.io/astral-sh/uv:alpine

RUN apk add --no-cache tzdata

WORKDIR /usr/src/site

COPY pyproject.toml uv.lock .python-version /usr/src/site/
RUN uv sync
COPY blog main users manage.py /usr/src/site/