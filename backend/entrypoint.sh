#!/bin/sh

set -e  # stop if any error

source .venv/bin/activate 

cd ./src

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput
RUN rm -rf static

echo "Starting app..."
exec "$@"