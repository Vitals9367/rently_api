#!/bin/bash
set -e

if [[ "$APPLY_MIGRATIONS" = "True" ]]; then
    echo "Applying database migrations..."
    ./manage.py migrate --noinput
fi

if [ "$1" = 'start_django_development_server' ]; then
    # Start server
    echo "Starting development server"
    ./manage.py runserver 0.0.0.0:8000
elif [ "$1" ]; then
    echo "Running command: $1"
    $1
else
    exec uwsgi --ini uwsgi.ini
fi