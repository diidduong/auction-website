VERSION=v1
DOCKERUSER=diidduong

install:
	pip install -e .
	pip install Flask-APScheduler

init-db:
	flask --app flaskr init-db

run:
	flask --app flaskr --debug run

generate-dependencies:
	pip freeze > requirements.txt

build:
	docker build -f Dockerfile -t flaskr-rest .

push:
	docker tag flaskr-rest $(DOCKERUSER)/flaskr-rest:$(VERSION)
	docker push $(DOCKERUSER)/flaskr-rest:$(VERSION)
	docker tag flaskr-rest $(DOCKERUSER)/flaskr-rest:latest
	docker push $(DOCKERUSER)/flaskr-rest:latest

