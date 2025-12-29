FROM ghcr.io/astral-sh/uv:alpine

RUN apk add --no-cache tzdata

WORKDIR /usr/src/site

COPY . /usr/src/site/

RUN uv sync
RUN .venv/bin/python manage.py collectstatic
RUN .venv/bin/python manage.py makemigrations
RUN .venv/bin/python manage.py migrate