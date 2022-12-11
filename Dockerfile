FROM ubuntu:20.04
LABEL MAINTAINER="diidduong@gmail.com"

WORKDIR /srv
COPY flaskr /srv/flaskr
COPY requirements.txt /srv/requirements.txt
COPY Makefile /srv/Makefile
COPY setup.cfg /srv/setup.cfg
COPY setup.py /srv/setup.py

ENV FLASK_APP=flaskr
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt
RUN make install
RUN make init-db

CMD ["make", "run"]