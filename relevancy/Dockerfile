FROM continuumio/anaconda

MAINTAINER John Beieler <jbeieler1@jhu.edu>

RUN apt-get install -y unzip netcat

ADD . /src

RUN cd /src; pip install -r requirements.txt

RUN chmod -x /src/launch.sh
CMD sh /src/launch.sh
