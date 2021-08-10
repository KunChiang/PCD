FROM python:3.9

LABEL "Maintainer"="ichiangkun@gmail.com"
LABEL "Version"="1"

# RUN pip install --upgrade pip
# RUN pip install pqi
# RUN pqi use douban
RUN apt-get update
RUN apt-get -y install git vim nginx

ADD . /app
WORKDIR /app

COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir /app/logs/

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "./gunicorn_start.sh" ]