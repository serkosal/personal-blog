FROM ghcr.io/astral-sh/uv:alpine

RUN apk add --no-cache tzdata

WORKDIR /usr/src/site

COPY . /usr/src/site/
RUN uv sync