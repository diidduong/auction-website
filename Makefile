install:
	pip install -e .

init-db:
	flask --app flaskr init-db

run:
	flask --app flaskr --debug run


