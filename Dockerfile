# Use an official Python runtime as a parent image
FROM ubuntu:22.04

RUN apt-get update

RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory
WORKDIR /app

# Install dependencies
COPY server/requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . /app/

WORKDIR /app/server

EXPOSE $PORT

RUN chmod +x /app/server/start.sh

CMD ["python -m gunicorn server.wsgi:application --bind 0.0.0.0:$PORT"]

# ENTRYPOINT ["python /app/server/manage.py process_tasks & gunicorn server.wsgi:application --bind 0.0.0.0:$PORT"]