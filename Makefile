ENV_FILE ?= local.env

-include $(ENV_FILE)
export

run-worker:
	celery -A app.worker worker --loglevel=info

run-app:
	uvicorn app.main:app --reload --host ${FAST_API_HOST} --port ${FAST_API_PORT}

run-tests:
	python -m unittest discover -s tests -p "test_*.py"

start-inference-service:
	docker compose up --build -d

stop-inference-service:
	docker compose down

test-inference-service:
	docker compose run --rm tests
