#!/bin/sh

set -e  # stop if any error

source .venv/bin/activate 

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting app..."
exec "$@"