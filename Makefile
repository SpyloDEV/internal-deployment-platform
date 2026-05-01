.PHONY: dev test lint migrate worker frontend backend

dev:
	docker compose up --build

backend:
	cd backend && uvicorn app.main:app --reload

frontend:
	cd frontend && npm run dev

worker:
	cd backend && celery -A app.workers.celery_app.celery_app worker --loglevel=INFO

test:
	cd backend && pytest

lint:
	cd backend && ruff check . && black --check .
	cd frontend && npm run lint && npm run typecheck

migrate:
	cd backend && alembic upgrade head
