runserver:
	python3 project/manage.py runserver 0.0.0.0:8000

migrate:
	python3 project/manage.py makemigrations
	python3 project/manage.py migrate

migrate-clean:
	rm -rf */*/migrations/[0-9]*_*.py

load-users:
	python3 project/manage.py loaddata project/user_data.json

docker-build:
	docker build . -t finansfatura:latest

docker-migrate:
	docker-compose exec backend python3 manage.py makemigrations
	docker-compose exec backend python3 manage.py migrate

docker-run:
	docker-compose down
	docker-compose up -d

docker-createsuperuser:
	docker-compose exec backend python3 manage.py createsuperuser --email=admin --noinput