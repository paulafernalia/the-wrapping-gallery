# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# copy project
COPY . /code/

# RUN mkdir /code/staticfiles
RUN mkdir -p /vol/web/static
RUN mkdir -p /vol/web/media

RUN useradd -ms /bin/bash user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user

# Run Django management commands and start the application
ENTRYPOINT ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --no-input --clear && gunicorn wrapping.wsgi:application --bind 0.0.0.0:8000"]
