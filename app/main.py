from fastapi import FastAPI, HTTPException, Request as FastAPIRequest
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
from app.worker import do_infer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import redis
import os
from pydantic import BaseModel

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_db = int(os.getenv("REDIS_DB", 0))

redis_conn = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Close Redis connection on shutdown
@app.on_event("shutdown")
def shutdown_event():
    redis_conn.close()

class InferenceRequest(BaseModel):
    text: str
    with_medusa: bool = True
    dyn_batch: bool = True

@app.get("/")
async def read_root(request: FastAPIRequest):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health_check")
async def health_check():
    result = do_infer.apply_async(args=["hello"], kwargs={"with_medusa": False})
    response = result.get(timeout=5)
    if response:
        return JSONResponse(status_code=200, content={"message": "Model healthy"})
    raise HTTPException(status_code=404, detail="Model not responding")

@app.get("/test_redis")
async def test_redis():
    try:
        redis_conn.ping()  # Test Redis connection
        return {"status": "Redis connected"}
    except redis.ConnectionError as e:
        raise HTTPException(status_code=500, detail=f"Redis connection failed: {str(e)}")

@app.post("/send_text")
async def send_text(request: InferenceRequest):
    task = do_infer.apply_async(
        args=[request.text], 
        kwargs={"with_medusa": request.with_medusa, "dyn_batch": request.dyn_batch}
    )
    return {"task_id": task.id}

@app.get("/get_task_status/{req_id}")
async def get_task_status(req_id: str):
    task = AsyncResult(req_id)
    if task.state == "PENDING":
        return {"status": "processing"}
    elif task.state == "SUCCESS":
        return {"status": "finished", "result": task.result}
    else:
        return {"status": "failed"}

@app.get("/tasks/")
async def get_all_tasks():
    keys = redis_conn.keys()
    task_ids = [key.decode("utf-8") for key in keys]
    return {"tasks": task_ids}

@app.post("/generate")
async def generate(request: InferenceRequest):
    task = do_infer.apply_async(
        args=[request.text], 
        kwargs={
            "with_medusa": request.with_medusa, 
            "dyn_batch": request.dyn_batch
        }
    )

    try:
        result = task.get(timeout=10)  # Block until task finishes
        return {"status": "finished", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task failed: {str(e)}")
