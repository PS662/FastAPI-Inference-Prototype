import os
from celery import Celery
from .model_utils import infer

# Initialize Celery
celery = Celery(__name__)
celery.conf.broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

@celery.task(bind=True)
def do_infer(self, text: str, model_name: str, dyn_batch: int, speculative_decoding: bool) -> str:
    """Perform inference using the specified model."""
    try:
        result = infer(text, model_name, speculative_decoding, dyn_batch)
        return result
    except Exception as e:
        print(f"Error during inference: {str(e)}")
        return "Inference failed."
