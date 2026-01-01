Below are professional, clear requirements for the Phase 1 task “Write Python script that makes GET, POST requests,” aligned with the roadmap’s goal of seeing headers/status codes in action.[^1]

## Script requirements (Phase 1: REST practice)

### Objective

Build a small Python CLI script that sends at least one HTTP **GET** request and one HTTP **POST** request to a real API endpoint and prints the most important parts of the request/response cycle (status code, headers, and JSON body).[^1]

### Functional requirements

- The script **shall** support running from the command line and must execute at least:
    - One GET request to retrieve data.[^1]
    - One POST request to create/send data.[^1]
- The script **shall** print, for each request:
    - Request method + full URL.[^1]
    - Response HTTP status code.[^1]
    - Response headers (at minimum `Content-Type`, plus any other key headers you find useful).[^1]
    - Response body:
        - If JSON: pretty-print JSON.
        - If not JSON: print raw text (or first N characters).[^1]
- The script **shall** include basic error handling:
    - Catch network/connection errors.
    - Handle non-2xx responses without crashing (print status + body).[^1]
- The script **shall** set a timeout for every request to avoid hanging.[^1]


### Input/CLI requirements

- The script **shall** accept configuration via CLI arguments (minimum):
    - `--base-url` (default allowed) or direct `--url`.
    - `--method` optional (or run both GET and POST by default).[^1]
- For POST, the script **shall** accept a JSON payload:
    - Either inline via `--data '{"key":"value"}'` or by reading from a file path `--data-file payload.json`.[^1]


### Data/API requirements (choose one approach)

- The script **should** use a safe public test API (recommended) such as `https://httpbin.org` for GET/POST experimentation, or any public API you choose.[^1]
- The script **shall** demonstrate sending JSON for POST with `Content-Type: application/json`.[^1]


### Output requirements

- Output must be human-readable and grouped per request (GET section, POST section).[^1]
- Include a short summary line at the end:
    - GET status, POST status, and total time taken (optional but useful).[^1]


### Quality requirements

- Code must be readable (clear function names, minimal duplication).[^1]
- Organize logic into functions, e.g. `send_get()`, `send_post()`, `print_response()`.[^1]


### Deliverables

- A single Python file, e.g. `src/rest_client.py`, committed to the repo.[^1]
- A short note added to `docs/rest_concepts.md` explaining what was observed about:
    - status codes,
    - headers,
    - request body vs response body.[^1]

If you tell which API you want to test against (httpbin vs a real public users API), a concrete CLI + code skeleton that meets these requirements can be provided.
<span style="display:none">[^2][^3][^4]</span>

<div align="center">⁂</div>

[^1]: AI_API_Learning_Roadmap.md

[^2]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/86423868/00de22ac-cc2d-43ec-91bc-292d1395b1bc/AI_API_Learning_Roadmap.md

[^3]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/86423868/40f0520d-b857-498d-8004-5f46765ffbbc/AI_API_Learning_Roadmap.md

[^4]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/86423868/f672760e-1795-42de-a708-f027cccf50c3/AI_API_Learning_Roadmap.md

