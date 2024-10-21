
# FastAPI Inference Prototype

This prototype provides a FastAPI-based inference service with dynamic batching, speculative decoding, 
and model switching using Celery and Redis.

I chose llama.cpp as the compilation library because it supports quantization, allowing models to be compressed into formats like Q2, Q4, and Q8. This compression improves inference speed while keeping memory usage low. Another reason I went with llama.cpp is its vendor-neutral design, which prevents getting locked into specific hardware ecosystems like OpenVINO or TensorRT, which are optimized for Intel and NVIDIA hardware. This makes the setup portable across both CPUs and GPUs, enabling efficient deployments on servers or edge devices. It reduces infrastructure costs and avoids vendor lock-in, ensuring flexibility as needs evolve.

Speculative decoding is implemented by using a smaller, faster draft model to predict future tokens, with the main model verifying those predictions. If the predictions align, the system skips redundant calculations, improving speed. This approach balances the trade-off between compute and latency, delivering faster responses without sacrificing much accuracy. It’s particularly useful for real-time applications where low latency is essential. By minimizing the workload on the main model, speculative decoding also increases overall throughput.

For dynamic batching, I’ve used Redis as a simple way to hack batching without over-complicating things. Incoming requests are pushed to a Redis queue, and once enough requests come in to fill the batch size, they are processed together. If the queue isn’t full right away, requests wait until enough accumulate. This approach ensures that resources are used efficiently, improving throughput and handling sudden traffic spikes by reducing redundant processing. Using Redis keeps things simple and fast while providing a way to manage batching dynamically.

The current system relies on FastAPI to serve models, with Celery managing asynchronous tasks and Redis acting as a broker and a lightweight queue for batching. Models are loaded lazily, which optimizes memory usage by keeping only the needed models in memory. Configurations are handled through environment variables and a JSON file that maps model names to paths, making the system easy to maintain and extend. Everything is containerized using Docker and managed with Docker Compose, this can be scaled by adding more workers or replicas of the API.

In the future, I will package the setup into a Python package for easier distribution and split the system into microservices by separating the API, Celery workers, and model services. Adding a load balancer would help manage traffic effectively, while caching frequently used results could reduce the system’s workload. I also plan to explore dynamic model loading, either by monitoring the configuration file for changes or by tying it to available system resources. There’s potential to integrate the Medusa head for further performance improvements and implement a more sophisticated dynamic batching strategy. Redis has worked well for now, but a more robust batching solution might be needed as the system grows.


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

## UI Overview

This prototype includes a simple web-based interface to interact with the inference service.

### Usage

1. **Launch the Service:**  
   Ensure the FastAPI app and Celery workers are running. You can start the services with:

   ```bash
   make start-inference-service
   ```

2. **Access the Web Interface:**  
   Open your browser and go to:  
   [http://localhost:8000](http://localhost:8000)

3. **Send a Text Prompt:**  
   - Enter your text in the input field.
   - Click the **"Send Message"** button to submit the prompt.
   - The response will be displayed on the same page when it becomes available.

4. **API Polling:**  
   - The UI automatically polls the `/poll_task_status` endpoint to update the result once ready.

## Makefile Commands

Use the provided ```Makefile``` commands and API to interact with the service.

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



### UI Files

- **HTML:** Located at `templates/index.html`
- **CSS:** Located at `static/main.css`
- **JavaScript:** Located at `static/main.js`

## Documentation

To view generated docs, go:

```
http://localhost:8000/docs
http://localhost:8000/redoc

```

If you need to view/save json:

```
http://localhost:8000/openapi.json
```

## Configuration

- **Environment Variables:** Stored in `config/local.env`.
- **Model Configuration:** Defined in `config/model_config.json`.