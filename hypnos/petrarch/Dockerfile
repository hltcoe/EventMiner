FROM python:2.7-alpine

MAINTAINER John Beieler <jbeieler1@jhu.edu>

RUN apk add --no-cache git

RUN pip install git+https://github.com/openeventdata/petrarch2.git

ADD . /src

RUN cd /src; pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "/src/petrarch_app.py"]
