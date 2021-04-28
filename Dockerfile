FROM python:3.9-alpine

LABEL "Maintainer"="ichiangkun@gmail.com"
LABEL "Version"="1"
# USER root

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg libmagic\
    && pip install Pillow \
    && apk del build-deps

# RUN pip install --upgrade pip
# RUN pip install pqi
# RUN pqi use douban

ADD . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "main.py"]