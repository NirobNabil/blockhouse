# Use an official Python runtime as a parent image
FROM python:3.12.5

# Set the working directory
WORKDIR /app

# Install dependencies
COPY server/requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . /app/

WORKDIR /app/server

EXPOSE $PORT

RUN echo '#!/bin/bash \
python manage.py process_tasks & \
exec gunicorn server.wsgi:application --bind localhost:$PORT' > ./start.sh && chmod +x /start.sh

CMD python /app/server/manage.py runserver $PORT