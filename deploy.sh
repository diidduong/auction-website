#!bin/bash
kubectl apply -f ./flaskr/flaskr-deployment.yaml
kubectl apply -f flaskr/flaskr-ingress.yaml
kubectl apply -f flaskr/flaskr-service.yaml

kubectl port-forward --address 0.0.0.0 service/flaskr-service 5000:5000