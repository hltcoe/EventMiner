FROM python:2.7-alpine

MAINTAINER John Beieler <jbeieler1@jhu.edu>

RUN apk add --no-cache git wget unzip

RUN mkdir -p /src/data

ADD . /src

RUN cd /src; pip install -r requirements.txt

CMD ["/src/wait-for", "rabbitmq:5672", "--", "python", "/src/app.py"]
