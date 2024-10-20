#!/usr/bin/env python3

import argparse
import requests
import os
from dotenv import dotenv_values

env_config = dotenv_values(".local_env")

DEFAULT_CONFIG = {
    "FAST_API_HOST": env_config.get("FAST_API_HOST", "localhost"),
    "FAST_API_PORT": env_config.get("FAST_API_PORT", "8000"),
}

DEFAULT_BASE_URL = f"http://{DEFAULT_CONFIG['FAST_API_HOST']}:{DEFAULT_CONFIG['FAST_API_PORT']}"

def send_text(base_url, prompt, with_medusa, dyn_batching):
    url = f"{base_url}/send_text"
    payload = {"text": prompt, "with_medusa": with_medusa, "dyn_batch": dyn_batching}
    response = requests.post(url, json=payload)
    print_response(response)

def generate(base_url, prompt, with_medusa, dyn_batching):
    url = f"{base_url}/generate"
    payload = {"text": prompt, "with_medusa": with_medusa, "dyn_batch": dyn_batching}
    response = requests.post(url, json=payload)
    print_response(response)

def health_check(base_url):
    url = f"{base_url}/health_check"
    response = requests.get(url)
    print_response(response)

def get_task_status(base_url, task_id):
    url = f"{base_url}/get_task_status/{task_id}"
    response = requests.get(url)
    print_response(response)

def print_response(response):
    if response.status_code == 200:
        print(f"Success:\n{response.json()}")
    else:
        print(f"Error {response.status_code}:\n{response.text}")

def main():
    parser = argparse.ArgumentParser(description="Simple Tester for FastAPI Medusa Service")

    # Common arguments for all commands
    parser.add_argument("--url", default=DEFAULT_BASE_URL, help="Base URL of the FastAPI service")

    subparsers = parser.add_subparsers(dest="command", required=True)
    
    send_text_parser = subparsers.add_parser("send-text", help="Send text prompt")
    send_text_parser.add_argument("--prompt", required=True, help="Prompt to generate from")
    send_text_parser.add_argument("--with-medusa", action="store_true", help="Enable Medusa")
    send_text_parser.add_argument("--dyn-batching", action="store_true", help="Enable dynamic batching")

    generate_parser = subparsers.add_parser("generate", help="Generate text with options")
    generate_parser.add_argument("--prompt", required=True, help="Prompt to generate from")
    generate_parser.add_argument("--with-medusa", action="store_true", help="Enable Medusa")
    generate_parser.add_argument("--dyn-batching", action="store_true", help="Enable dynamic batching")

    health_check_parser = subparsers.add_parser("health-check", help="Perform health check")

    status_parser = subparsers.add_parser("get-task-status", help="Get task status by ID")
    status_parser.add_argument("--task-id", required=True, help="Task ID to check")

    args = parser.parse_args()

    if args.command == "send-text":
        send_text(args.url, args.prompt, args.with_medusa, args.dyn_batching)
    elif args.command == "generate":
        generate(args.url, args.prompt, args.with_medusa, args.dyn_batching)
    elif args.command == "health-check":
        health_check(args.url)
    elif args.command == "get-task-status":
        get_task_status(args.url, args.task_id)
    else:
        parser.print_help()
        return
    
if __name__ == "__main__":
    main()
