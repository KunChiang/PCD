FROM python:3.9

LABEL "Maintainer"="ichiangkun@gmail.com"
LABEL "Version"="1"

# RUN pip install --upgrade pip
# RUN pip install pqi
# RUN pqi use douban

ADD . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "main.py"]