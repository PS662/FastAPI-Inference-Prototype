import os
import time
from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

def infer_vicuna_medusa(text: str) -> str:
    time.sleep(2)
    return f"Medusa inference result for: {text}"

def infer_vicuna_medusa_dyn_batch(text: str) -> str:
    time.sleep(2)
    return f"Dynamic batching Medusa inference result for: {text}"

def infer_vicuna_base(text: str) -> str:
    time.sleep(2)
    return f"Base Vicuna inference result for: {text}"

@celery.task(bind=True)
def do_infer(self, text: str, with_medusa: bool = True, dyn_batch: bool = True) -> str:
    if with_medusa:
        if dyn_batch:
            return infer_vicuna_medusa_dyn_batch(text)
        else:
            return infer_vicuna_medusa(text)
    else:
        return infer_vicuna_base(text)
