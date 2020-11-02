FROM python:3.8.6

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate