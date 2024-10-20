
# FastAPI Inference Prototype

This prototype provides a FastAPI-based inference service with dynamic batching, speculative decoding, 
and model switching using Celery and Redis.

## Project Structure

```
.
├── app/                   # Main application logic
├── config/                # Configuration files
├── models/                # Model directory
├── static/                # Static assets
├── templates/             # HTML templates
├── tests/                 # Unit tests
├── examples/              # Example scripts
├── Dockerfile             # Docker image configuration
└── Makefile               # Automation commands
```

## Makefile Commands

| Command                        | Description                                  |
|--------------------------------|----------------------------------------------|
| `make convert`                 | Convert HF models to GGUF format.            |
| `make run-worker`              | Start the Celery worker.                     |
| `make run-app`                 | Run the FastAPI app locally.                 |
| `make run-tests`               | Run unit tests.                              |
| `make start-inference-service` | Start the service with Docker Compose.       |
| `make stop-inference-service`  | Stop the running services.                   |
| `make test-inference-service`  | Test the inference service using Docker.     |

## API Endpoints

| Endpoint                | Method | Description                                |
|-------------------------|--------|--------------------------------------------|
| `/`                     | GET    | Home page.                                 |
| `/health_check`         | GET    | Check the health of the service.           |
| `/send_text`            | POST   | Submit a text prompt for inference.        |
| `/generate`             | POST   | Generate text from a prompt.               |
| `/get_task_status/{id}` | GET    | Get the status of a specific task by ID.   |
| `/tasks/`               | GET    | List all tasks.                            |

## Example Usage

### Using `simple_tester.py`:

**Send a text prompt:**
```bash
python examples/simple_tester.py --url http://localhost:8000 send-text     --prompt "Hello, how are you?" --model-name vicuna_q2
```

**Generate text:**
```bash
python examples/simple_tester.py --url http://localhost:8000 generate     --prompt "Hello, how are you?" --model-name vicuna_q2
```

**Health Check:**
```bash
python examples/simple_tester.py --url http://localhost:8000 health-check
```

**List all tasks:**
```bash
python examples/simple_tester.py --url http://localhost:8000 tasks
```

**Get task status:**
```bash
python examples/simple_tester.py --url http://localhost:8000 get-task-status     --task-id <TASK_ID>
```

## Configuration

- **Environment Variables:** Stored in `config/local.env`.
- **Model Configuration:** Defined in `config/model_config.json`.

## Conclusion

This project serves LLM models with dynamic batching and speculative decoding. Use the provided 
Makefile commands and API to interact with the service.