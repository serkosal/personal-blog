#!/bin/sh

set -e  # stop if any error

source .venv/bin/activate 

cd ./src

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput
rm -rf ./static/*

echo "Compiling translations..."
python manage.py compilemessages

echo "Updating model translations..."
python manage.py update_translation_fields


echo "Starting app..."
exec "$@"