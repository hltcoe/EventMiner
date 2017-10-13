FROM python:2.7-alpine

MAINTAINER John Beieler <jbeieler1@jhu.edu>

RUN apk add --no-cache git wget unzip

ADD . /src

RUN cd /src; pip install -r requirements.txt

CMD ["/src/wait-for", "ccnlp:5000", "-t", "60", "--", "python", "/src/app.py"]
