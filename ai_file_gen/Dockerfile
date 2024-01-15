# Starts from the Python 3.11.7 base image
FROM python:3.11.7

# Sets an environment variable with the directory
# where the app will be installed
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

# Creates the directory and instructs Docker to operate
# from there for the rest of the Dockerfile
RUN mkdir /app
WORKDIR /app

# Copies the requirements.txt to the container
COPY requirements.txt /app/

# Installs the Python dependencies
RUN pip install -r requirements.txt

# Copies the Django application to the container
COPY . /app/

# Exposes the port where Django App is running
EXPOSE 8000

# This is the command that will run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]