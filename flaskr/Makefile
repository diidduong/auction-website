VERSION=v1
DOCKERUSER=diidduong

build:
	docker build -f Dockerfile -t flaskr-rest .

push:
	docker tag flaskr-rest $(DOCKERUSER)/flaskr-rest:$(VERSION)
	docker push $(DOCKERUSER)/flaskr-rest:$(VERSION)
	docker tag flaskr-rest $(DOCKERUSER)/flaskr-rest:latest
	docker push $(DOCKERUSER)/flaskr-rest:latest

deploy:
	kubectl apply -f flaskr-deployment.yaml
