FROM python:3.10-alpine
LABEL MAINTAINER="diidduong@gmail.com"

WORKDIR /srv
COPY flaskr /srv/flaskr
COPY requirements.txt /srv/requirements.txt
COPY setup.cfg /srv/setup.cfg
COPY setup.py /srv/setup.py

RUN pip install flask Flask-APScheduler

ENV FLASK_APP=flaskr

CMD ["sh", "./flaskr/run.sh"]