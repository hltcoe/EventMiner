FROM python:2.7-alpine

MAINTAINER John Beieler <jbeieler1@jhu.edu>

RUN apk add --no-cache git wget unzip

RUN mkdir /src

RUN mkdir -p /src/nltk_data/tokenizers
RUN wget https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/tokenizers/punkt.zip -O /src/nltk_data/tokenizers/punkt.zip
RUN unzip /src/nltk_data/tokenizers/punkt.zip; rm -rf /src/nltk_data/tokenizers/punkt.zip
RUN mv punkt /src/nltk_data/tokenizers
ENV NLTK_DATA=/src/nltk_data

ADD . /src

RUN cd /src; pip install -r requirements.txt

EXPOSE 6000

CMD ["/src/wait-for", "rabbitmq:5672", "-t", "90", "--", "python", "/src/app.py"]
