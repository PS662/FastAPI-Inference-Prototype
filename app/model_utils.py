import os
import json
import redis
from llama_cpp import Llama
from llama_cpp.llama_speculative import LlamaPromptLookupDecoding

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_conn = redis.Redis(host=redis_host, port=redis_port)

CONFIG_PATH = os.getenv("MODEL_CONFIG_PATH", "./config/model_config.json")
with open(CONFIG_PATH, "r") as f:
    model_config = json.load(f)

active_models = {}

MOCK = bool(os.getenv("MOCK_INFERENCE", "False").lower() in ["true", "1", "yes"])

def get_model_key(model_name: str, speculative: bool) -> str:
    """Generate a unique key for the model."""
    return f"{model_name}_speculative_{speculative}"

def load_model(model_name: str, speculative: bool) -> Llama:
    """Lazy load the model using the JSON config."""
    if model_name not in model_config:
        raise ValueError(f"Model '{model_name}' not found in config. Check your model_config.json.")

    model_info = model_config[model_name]
    model_path = model_info["path"]
    model_key = get_model_key(model_name, speculative)

    # Check if the model is already loaded
    if model_key in active_models:
        return active_models[model_key]

    with redis_conn.lock(f"model_lock_{model_key}", timeout=30):
        if model_key in active_models:
            return active_models[model_key]

        if speculative:
            decoder = LlamaPromptLookupDecoding(num_pred_tokens=10)
            model = Llama(model_path=model_path, draft_model=decoder, n_threads=8, chat_format="llama-2")
        else:
            model = Llama(model_path=model_path, n_threads=8, chat_format="llama-2")

        active_models[model_key] = model
        return model

def batch_infer(model, texts):
    """Perform batch inference and extract results."""
    results = []
    for text in texts:
        response = model(
            text, 
            max_tokens=32, 
            stop=["Q:", "\n"], 
            echo=True
        )
        if "choices" in response and response["choices"]:
            results.append(response["choices"][0]["text"])
        else:
            results.append("Inference failed: No valid response.") 
    return results

def infer(text: str, model_name: str, speculative: bool, dyn_batch: int) -> str:
    """Unified inference function."""
    print(f"Mock is {MOCK}")
    if MOCK:
        return f"Mock inference result for: {model_name}"

    model = load_model(model_name, speculative)

    prompt = f"Q: {text.strip()} Please respond in English. A: "

    if dyn_batch > 1:
        redis_conn.rpush("batch_queue", prompt)
        batch_size = redis_conn.llen("batch_queue")

        if batch_size >= dyn_batch:
            texts = [redis_conn.lpop("batch_queue").decode() for _ in range(batch_size)]
            results = batch_infer(model, texts)
            return results[0] 
        else:
            return "Request added to batch, waiting for more requests."
    elif dyn_batch == 1:
        response = model(
            prompt,
            max_tokens=32, 
            stop=["Q:", "\n", "A:"], 
            echo=False
        )

        print(f"Model response: {response}")  # Debugging

        if "choices" in response and response["choices"]:
            generated_text = response["choices"][0]["text"].strip()
            return generated_text
        else:
            return "Inference failed: No valid response."
    else:
        raise ValueError("Invalid batch size.")



