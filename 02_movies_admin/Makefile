.PHONY: run web-service
run:
	python3 manage.py runserver

.PHONY: run database
run-db:
	docker run -d \
		--name postgres \
		-p 5432:5432 \
		-v ${HOME}/Documents/postgresql_data:/var/lib/postgresql/data \
		-e POSTGRES_PASSWORD=123qwe \
		-e POSTGRES_USER=app \
		-e POSTGRES_DB=movies_database  \
		postgres:13 

.PHONY: tearn down database
stop-db:
	docker stop postgres && docker rm postgres && docker system prune -f 

.PHONY: connect to PostgreSQL
connect-db:
	psql -U app -h 127.0.0.1 -d movies_database

.PHONY: create schema into PostgreSQL
init-schema-db:
	psql -U app -h 127.0.0.1 -d movies_database -f ../01_schema_design/movies_database.ddl

.PHONY: clean pyc-files
clean-pyc:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
