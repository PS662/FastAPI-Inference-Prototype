#!/usr/bin/env python3

import argparse
import requests
import os
import json
from dotenv import dotenv_values

# Load environment configuration
env_config = dotenv_values("config/local.env")

DEFAULT_CONFIG = {
    "FAST_API_HOST": env_config.get("FAST_API_HOST", "localhost"),
    "FAST_API_PORT": env_config.get("FAST_API_PORT", "8000"),
    "MODEL_CONFIG_PATH": env_config.get("MODEL_CONFIG_PATH", "config/model_config.json")
}

DEFAULT_BASE_URL = f"http://{DEFAULT_CONFIG['FAST_API_HOST']}:{DEFAULT_CONFIG['FAST_API_PORT']}"

def load_model_config(config_path):
    """Load the model configuration JSON."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")

    with open(config_path, "r") as f:
        return json.load(f)

def send_text(base_url, prompt, model_name, dyn_batching, speculative_decoding):
    """Send a text prompt for inference."""
    url = f"{base_url}/send_text"
    payload = {
        "text": prompt,
        "model_name": model_name,
        "dyn_batch": dyn_batching,
        "speculative_decoding": speculative_decoding
    }
    response = requests.post(url, json=payload)
    print_response(response)

def generate(base_url, prompt, model_name, dyn_batching, speculative_decoding):
    """Generate text with the specified model."""
    url = f"{base_url}/generate"
    payload = {
        "text": prompt,
        "model_name": model_name,
        "dyn_batch": dyn_batching,
        "speculative_decoding": speculative_decoding
    }
    response = requests.post(url, json=payload)
    print_response(response)

def health_check(base_url):
    """Perform a health check on the service."""
    url = f"{base_url}/health_check"
    response = requests.get(url)
    print_response(response)

def get_task_status(base_url, task_id):
    """Get the status of a specific task by ID."""
    url = f"{base_url}/get_task_status/{task_id}"
    response = requests.get(url)
    print_response(response)

def list_tasks(base_url):
    """List all tasks."""
    url = f"{base_url}/tasks/"
    response = requests.get(url)
    print_response(response)

def print_response(response):
    """Print the response from the API."""
    if response.status_code == 200:
        print(f"Success:\n{response.json()}")
    else:
        print(f"Error {response.status_code}:\n{response.text}")

def main():
    parser = argparse.ArgumentParser(description="Simple Tester for FastAPI Medusa Service")

    # Common arguments for all commands
    parser.add_argument("--url", default=DEFAULT_BASE_URL, help="Base URL of the FastAPI service")
    parser.add_argument("--config", default=DEFAULT_CONFIG["MODEL_CONFIG_PATH"], help="Path to the model configuration JSON")

    subparsers = parser.add_subparsers(dest="command", required=True)

    send_text_parser = subparsers.add_parser("send-text", help="Send text prompt")
    send_text_parser.add_argument("--prompt", required=True, help="Prompt to generate from")
    send_text_parser.add_argument("--model-name", required=True, help="Model name from the config")
    send_text_parser.add_argument("--dyn-batching", type=int, default=1, help="Batch size for dynamic batching")
    send_text_parser.add_argument("--speculative-decoding", action="store_true", help="Enable speculative decoding")

    generate_parser = subparsers.add_parser("generate", help="Generate text with options")
    generate_parser.add_argument("--prompt", required=True, help="Prompt to generate from")
    generate_parser.add_argument("--model-name", required=True, help="Model name from the config")
    generate_parser.add_argument("--dyn-batching", type=int, default=1, help="Batch size for dynamic batching")
    generate_parser.add_argument("--speculative-decoding", action="store_true", help="Enable speculative decoding")

    health_check_parser = subparsers.add_parser("health-check", help="Perform health check")

    status_parser = subparsers.add_parser("get-task-status", help="Get task status by ID")
    status_parser.add_argument("--task-id", required=True, help="Task ID to check")

    tasks_parser = subparsers.add_parser("tasks", help="List all tasks")

    args = parser.parse_args()

    model_config = load_model_config(args.config)

    if args.command == "send-text":
        send_text(args.url, args.prompt, args.model_name, args.dyn_batching, args.speculative_decoding)
    elif args.command == "generate":
        generate(args.url, args.prompt, args.model_name, args.dyn_batching, args.speculative_decoding)
    elif args.command == "health-check":
        health_check(args.url)
    elif args.command == "get-task-status":
        get_task_status(args.url, args.task_id)
    elif args.command == "tasks":
        list_tasks(args.url)
    else:
        parser.print_help()
        return

if __name__ == "__main__":
    main()
