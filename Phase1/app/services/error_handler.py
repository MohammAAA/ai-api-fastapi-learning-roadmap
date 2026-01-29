"""
error_handler.py

Centralized validation and error utilities for the REST exploration CLI.

This module provides:
- A custom exception type (`invalidData`) used to report invalid CLI inputs and
  HTTP error outcomes in a consistent way.
- Input validation rules that enforce the intended CLI contract:
  - GET requests must not include a request body.
  - POST requests must provide exactly one body source (`--data` or `--data_file`).
- A helper that turns non-success HTTP status codes into a raised exception so
  callers can fail fast and surface meaningful errors.

Public API
----------
- invalidData:
    Custom exception raised when CLI arguments are invalid or when an HTTP request
    returns an unexpected status code.

- input_error_handler(input_args) -> None:
    Validates parsed CLI arguments. Raises `invalidData` if the inputs violate
    the expected contract (e.g., POST without payload, GET with payload, or both
    payload sources provided).

- response_error_handler(error_code: int) -> None:
    Raises `invalidData` with a message that includes the HTTP status code when a
    request fails (non-2xx, depending on caller logic).

Expected `input_args` fields
----------------------------
`input_args` is expected to be an argparse Namespace (or compatible object) with:
- method: str
- data: str | None
- data_file: str | None

Notes
-----
- This module intentionally raises exceptions rather than printing errors so that
  the CLI entrypoint can decide how to display or handle failures.
- For a more production-like approach, consider mapping HTTP status codes to
  typed exceptions and including response body/context in the error message.
"""



class invalidData(ValueError):
    """Exception raised for invalid data"""
    pass

def input_error_handler(input_args):
    if input_args.method == "":
        raise invalidData("The input --method must be existing")
    if input_args.data is None and input_args.data_file is None and input_args.method == "post":
        raise invalidData("either --data or --data_file must be entered")
    elif input_args.data is not None and input_args.data_file is not None:
        raise invalidData("Only one input (--data or --data_file) must be entered")
    # elif (input_args.data != "" or input_args.data_file != "") and (input_args.method == "get" or input_args.method == "GET"):
    elif (input_args.data or input_args.data_file) and input_args.method.lower() == "get":
    # an empty string is evaluated to FALSE, so if any string is not empty the first parenthesis will evaluate to TRUE
    # input_args.method.lower() handles variations like "Get" or "gET" or "GET"
        raise invalidData("No data shall be sent in a GET request")
    
def response_error_handler (error_code):
    raise invalidData(f"request returned with status code: {error_code}")