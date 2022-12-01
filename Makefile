install:
	pip install -e .
	pip install Flask-Modals
	sudo pip uninstall jinja2
	sudo pip install jinja2==3.0

init-db:
	flask --app flaskr init-db

run:
	flask --app flaskr --debug run


