ENV_FILE ?= config/local.env

-include $(ENV_FILE)
export

# Default model path and output type if not provided
MODEL_PATH ?= ../FastAPI-Inference-Prototype/models/medusa-vicuna-7b/
OUT_TYPE ?= q8_0

# you need to git clone llama.cpp to use this tool
convert:
	python convert_hf_to_gguf.py $(MODEL_PATH) --outtype $(OUT_TYPE)

# run locally
run-worker:
	celery -A app.worker worker --loglevel=info

run-app:
	uvicorn app.main:app --reload --host ${FAST_API_HOST} --port ${FAST_API_PORT}

run-tests:
	python -m unittest discover -s tests -p "test_*.py"

# Following commands are for docker compose
start-inference-service:
	docker compose up --build -d

stop-inference-service:
	docker compose down

test-inference-service:
	docker compose run --rm tests
