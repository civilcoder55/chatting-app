#!/bin/bash
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
gunicorn simpleio.wsgi:application --bind 0.0.0.0:8000