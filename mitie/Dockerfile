FROM python:2.7-alpine

MAINTAINER John Beieler <jbeiele1@jhu.edu>

RUN apk add --no-cache git build-base curl

RUN mkdir /src
ADD . /src

WORKDIR /src 

RUN curl -LO https://github.com/mit-nlp/MITIE/releases/download/v0.4/MITIE-models-v0.2.tar.bz2
RUN tar -xzjf MITIE-models-v0.2.tar.bz2; rm -rf MITIE-models-v0.2.tar.bz2

RUN pip install -r requirements.txt

EXPOSE 6000

CMD ["/src/wait-for", "rabbitmq:5672", "--", "python", "/src/app.py"]
