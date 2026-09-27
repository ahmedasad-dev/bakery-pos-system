.PHONY: up down logs migrate test lint

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

migrate:
	docker compose exec backend python manage.py migrate

test:
	docker compose exec backend pytest
	docker compose exec frontend npm test

lint:
	docker compose exec backend ruff check .
	docker compose exec frontend npm run lint

