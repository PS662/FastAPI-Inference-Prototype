from fastapi import FastAPI, HTTPException, Request as FastAPIRequest
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
from app.worker import do_infer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import redis
import os
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

# Redis Configuration
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_db = int(os.getenv("REDIS_DB", 0))
redis_conn = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

# Initialize FastAPI
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("shutdown")
def shutdown_event():
    redis_conn.close()

class InferenceRequest(BaseModel):
    text: str
    model_name: str 
    dyn_batch: int = 1  
    speculative_decoding: bool = True  # Enable/disable speculative decoding

@app.post("/send_text")
async def send_text(request: InferenceRequest):
    """Submit an inference request."""
    task = do_infer.apply_async(
        args=[request.text, request.model_name, request.dyn_batch, request.speculative_decoding]
    )
    return {"task_id": task.id}

@app.post("/generate")
async def generate(request: InferenceRequest):
    """Generate text using the specified model."""
    task = do_infer.apply_async(
        args=[request.text, request.model_name, request.dyn_batch, request.speculative_decoding]
    )

    try:
        result = task.get(timeout=50)  # Block until task finishes
        return {"status": "finished", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task failed: {str(e)}")

@app.get("/health_check")
async def health_check():
    """Check the health of the model service."""
    task = do_infer.apply_async(
        args=["hello", "vicuna_q2", 1, False]
    )
    try:
        response = task.get(timeout=5)
        if response:
            return JSONResponse(status_code=200, content={"message": "Model healthy"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

    raise HTTPException(status_code=404, detail="Model not responding")

@app.get("/get_task_status/{req_id}")
async def get_task_status(req_id: str):
    """Retrieve the status of a task."""
    task = AsyncResult(req_id)
    if task.state == "PENDING":
        return {"status": "processing"}
    elif task.state == "SUCCESS":
        return {"status": "finished", "result": task.result}
    else:
        return {"status": "failed"}

@app.get("/tasks/")
async def get_all_tasks():
    """List all tasks."""
    keys = redis_conn.keys()
    task_ids = [key.decode("utf-8") for key in keys]
    return {"tasks": task_ids}

@app.get("/openapi.json")
async def get_open_api_endpoint():
    return get_openapi(
        title="FastAPI Inference Service",
        version="1.0.0",
        description="This is the API for the inference service with dynamic batching and speculative decoding.",
        routes=app.routes,
    )

@app.get("/")
async def read_root(request: FastAPIRequest):
    """Render the home page."""
    return templates.TemplateResponse("index.html", {"request": request})
