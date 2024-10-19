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

ENV GOOGLE_CLOUD_PROJECT blockhouse-439114
ENV USE_CLOUD_SQL_AUTH_PROXY false

EXPOSE 8000

CMD python /app/server/manage.py runserver
