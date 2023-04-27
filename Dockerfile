FROM python:3.9

LABEL "Maintainer"="ichiangkun@gmail.com"
LABEL "Version"="1"

RUN sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list
RUN cat /etc/apt/sources.list
RUN rm -Rf /var/lib/apt/lists/*
RUN apt-get update
RUN apt-get -y install git vim nginx
RUN pip install flask pyyaml python-magic Pillow art gunicorn

ADD . /app
WORKDIR /app

COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir /app/logs/

# RUN pip install --upgrade pip
# RUN pip install pqi
# RUN pqi use douban
# RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
# ENTRYPOINT [ "./gunicorn_start.sh" ]
