run-server:
	poetry run python core/manage.py runserver

migrations:
	poetry run python core/manage.py makemigrations

migrate:
	poetry run python core/manage.py migrate

shell:
	poetry run python core/manage.py shell