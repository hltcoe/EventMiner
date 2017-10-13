FROM continuumio/anaconda

MAINTAINER John Beieler <jbeieler1@jhu.edu>

#RUN sed -i "s/httpredir.debian.org/`curl -s -D -http://httpredir.debian.org/demo/debian/ | awk '/^Link:/ { print $2 }' | sed -e 's@<http://\(.*\)/debian/>;@\1@g'`/" /etc/apt/sources.list
RUN apt-get clean && apt-get update
RUN apt-get install -y build-essential python-dev netcat

ADD . /src
RUN cd /src; pip install -r requirements.txt

RUN chmod -x /src/launch.sh
CMD sh /src/launch.sh
