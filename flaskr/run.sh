#!/bin/sh
cd /srv
pip install --upgrade virtualenv
virtualenv -p python3 venv
python3 -m venv venv
chmod 700 venv
source venv/bin/activate
export FLASK_APP=flaskr
export FLASK_ENV=development
python3 -m flask --app flaskr init-db
python3 -m flask --app flaskr --debug run