#!/bin/bash \
python manage.py process_tasks & \
exec gunicorn server.wsgi:application --bind localhost:$PORT
