"""
request_handler.py

A small HTTP client module. It demonstrates how to issue GET and POST requests from Python,
inspect responses, and report request latency in a consistent, readable format.

Key capabilities
---------------
- Dispatches requests based on an HTTP method string (GET/POST).
- Prints a structured JSON summary of each response including:
  - method, url
  - HTTP status code
  - response Content-Type
  - response body (JSON when possible; otherwise a truncated text preview)
  - request latency (ms)
- Uses timeouts to avoid hanging network calls.
- Validates “success” using the HTTP 2xx range and delegates non-2xx handling
  to `response_error_handler`.

Payload handling (POST)
-----------------------
- If `data` is provided, it is expected to be a JSON string; it is decoded to a
  Python object via `json.loads()` before being passed to `requests.post(..., json=...)`.
- If `data_file` is provided, it is expected to point to a file containing a JSON
  payload; the file is read via `pathlib.Path.read_text()` and decoded via
  `json.loads()` before the request is sent.

Public API
----------
- process_request(url: str, method: str, data: str | None, data_file: str | None) -> None
- request_get(url: str) -> None
- request_post(url: str, data: str | None, data_file: str | None) -> None
- print_output(method: str, URL: str, status_code: int, header_content_type: str,
              response_body: object, latency: float) -> None

Notes
-----
- This module focuses on REST exploration rather than production-grade features
  (e.g., retries/backoff, structured logging, and typed response models).
- For best results when experimenting, use endpoints that return JSON
  (e.g., https://httpbin.org/get and https://httpbin.org/post).
"""


import requests # to perform GET and POST requests
import json # to use json.dumps() (convert dict or list to JSON), and json.loads() (convert JSON to dict)
import time # to calculate request latency
from pathlib import Path # to open and read a file
from app.services.error_handler import response_error_handler

# process the input request
def process_request(url: str , method: str, data: str, data_file: str):
    if method.lower() == "get":
        request_get(url)
    elif method.lower() == "post":
        request_post(url, data, data_file)


def print_output(method: str, URL: str, status_code: str, header_content_type: str, response_body: str, latency: int):
    # In Python, a string defined with a single set of quotes must begin and end on the same line. 
    # To allow the string to span multiple lines and handle the internal quotes correctly, use triple double-quotes (""")
    # output = f"""{
    #         "method": {method},
    #         "url": {URL},
    #         "status_code": {status_code},
    #         "response_content_type": {header_content_type},
    #         "response_body": {response_body},
    #         }"""

    # I will not use the above representation as the curly braces {} will confuse the string and may be treated as a expression/format placeholder
    # so it may try to interpret parts of the string as (format specifier)
    # Solution: Don’t manually craft JSON using an f-string. Build a Python dict and print it with json.dumps()
    output = {
        "method": method,
        "url": URL,
        "status_code": status_code,
        "response_content_type": header_content_type,
        "response_body": response_body,
    }
    # convert dict to JSON
    output = json.dumps(output, indent=4)
    print(output)
    print(f"\n Total request time taken: {latency} ms")





def request_get (url: str):
    # start latency measurement
    start = time.perf_counter()
    # perform the GET request with timeout = 10 seconds
    response_get = requests.get(url, timeout=10)
    # calculate latency
    latency_ms = (time.perf_counter() - start) * 1000
    status_code = response_get.status_code
    if 200 <= status_code < 300:
        response_content_type = response_get.headers['content-type']
        try:
            # Try to parse the response body as JSON
            response_body = response_get.json()
        except ValueError:
            # If the response body can't be parsed as JSON, parse it as text, get the first 500 characters
            response_body = response_get.text[:500]
        print_output("GET", url, status_code, response_content_type, response_body, latency_ms)
    elif status_code >= 300 or status_code < 200:
        response_error_handler(status_code)

def request_post (url: str, data, data_file):
    start = time.perf_counter()
    # the --data has nargs = "?"
    # which means that if the user doesn't specify it,
    # it will become None (which is not an empty string ...
    # so the check: "if data != "" " is not a valid check")
    if data is not None:
        # convert the JSON to dict before sending it to the POST request
        payload = json.loads(data)
        response_post = requests.post(url, json=payload, timeout=10)
    elif data_file is not None:
        # Read the file and then convert it from JSON to dict before sending it to the POST request
        payload = json.loads(Path(data_file).read_text(encoding="utf-8"))
        response_post = requests.post(url, json=payload)
    latency_ms = (time.perf_counter() - start) * 1000
    status_code = response_post.status_code
    if status_code >= 200 and status_code < 300:
        response_content_type = response_post.headers['content-type']
        response_body = response_post.json()
        print_output("POST", url, status_code, response_content_type, response_body, latency_ms)
    elif status_code >= 300 or status_code < 200:
        response_error_handler(status_code)
