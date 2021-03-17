FROM python:3.8.6-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install --no-cache-dir -r requirements.txt && \
 apk --purge del .build-deps
 
COPY . .

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "--workers", "2", "tinytwitter.wsgi" ]