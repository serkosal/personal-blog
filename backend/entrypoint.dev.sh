#!/bin/sh

set -e  # stop if any error

source .venv/bin/activate 

cd ./src

echo "Running migrations..."
python manage.py migrate

echo "Compiling translations..."
python manage.py compilemessages

echo "Starting app..."
exec "$@"