python manage.py process_tasks & \
exec gunicorn server.wsgi:application --bind 0.0.0.0:$PORT
