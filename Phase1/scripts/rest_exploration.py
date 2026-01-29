"""
rest_exploration.py

CLI entrypoint for exploring HTTP request/response behavior. This script parses command-line arguments,
validates them against the intended contract (method/body rules), and delegates
execution to the request layer.

Workflow
--------
1) Parse CLI inputs (method, url, optional payload source).
2) Validate inputs:
   - GET must not include payload.
   - POST must provide exactly one payload source (inline JSON or JSON file).
3) Execute the HTTP request and print a structured response summary.

Command-line arguments
----------------------
--method   Required. HTTP method to use (expected: get|post).
--url      Required. Target URL to call.
--data     Optional. JSON string payload for POST requests.
--data_file Optional. Path to a file containing a JSON payload for POST requests.

Examples
--------
GET:
    python -m scripts.rest_exploration --method get --url https://httpbin.org/get

POST with inline JSON:
    python -m scripts.rest_exploration --method post --url https://httpbin.org/post --data '{"a": 1}'

POST with JSON file:
    python -m scripts.rest_exploration --method post --url https://httpbin.org/post --data_file payload.json

Modules used
------------
- app.services.error_handler: input validation for method/payload rules.
- app.services.request_handler: request dispatching and response printing.
"""


import argparse
from app.services.error_handler import input_error_handler
from app.services.request_handler import process_request


def parse_args():
    parser = argparse.ArgumentParser(
        description="Explore http methods and their responses"
    )
    parser.add_argument("--method", required=True, type=str, help="http method (get - post)")
    parser.add_argument(
        "--url",
        required=True,
        type=str,
        help="URL to apply the method on",
    )
    parser.add_argument(
        "--data",
        nargs='?',
        type=str,
        help="JSON data to be sent in case of POST method",
    )
    parser.add_argument(
        "--data_file",
        nargs='?',
        type=str,
        help="Relative file path in which the data exists, use in case of POST method",
    )
    return parser.parse_args()

def main():
    input_args = parse_args()
    input_error_handler(input_args)
    process_request(input_args.url, input_args.method, input_args.data, input_args.data_file)

if __name__ == "__main__":
    main()