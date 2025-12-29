FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /usr/src/site

COPY . /usr/src/site/

RUN uv sync
RUN .venv/bin/python manage.py collectstatic

CMD [ "python", "-m gunicorn", "main.asgi:application", "-k uvicorn_worker.UvicornWorker" ]