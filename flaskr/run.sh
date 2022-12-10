#!/bin/bash
echo $WORKDIR
cd $WORKDIR
export FLASK_APP=flaskr
export FLASK_ENV=development
flask init-db
flask run