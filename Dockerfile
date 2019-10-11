# Base image
FROM python:3.7.4-slim-buster

# Update and install required build dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc libc6-dev

# Upgrade pip
RUN pip install --upgrade pip

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install project dependencies
COPY requirements.txt /
RUN pip install -r requirements.txt

# Copy code
COPY . /code/

# Set work directory
WORKDIR /code

# Run lint checks
RUN pylint --load-plugins pylint_django apps/**/ --disable=missing-docstring --disable=unused-variable --disable=unused-argument --max-line-length=120

# Run tests
RUN python manage.py test

# listen on this port
EXPOSE 8000

# Start server in dev mode
CMD python manage.py runserver 0.0.0.0:8000
