#!bin/bash
kubectl apply -f ./flaskr/flaskr-deployment.yaml
kubectl apply -f flaskr/flaskr-ingress.yaml
kubectl apply -f flaskr/flaskr-service.yaml