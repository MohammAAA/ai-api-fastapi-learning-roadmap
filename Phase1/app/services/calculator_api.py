import time
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from app.schemas.operations import operations


calculation_history: list[dict] = [] # Create an empty list to store the the 10 most recent calculations history
app = FastAPI()

# A FastAPI middleware is code that runs for every HTTP request before it reaches our endpoint function,
# and then runs again on the way back after the endpoint returns a response.
# This is the complete pipeline (middleware → router (maybe another middleware) → endpoint → response → middleware.)
# Note: the parameter "call_next" is not a pointer to the endpoint function, it is actually a pointer to whatever function that is coming next in the pipeline,
# which may be the endpoint function and may be another next-handler function
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request) # get to the next step
    latency_ms = (time.perf_counter() - start) * 1000 # calculate the whole process response time (i.e.: middleware → router → endpoint → response)

    request_time = datetime.now(timezone.utc).isoformat() # Get the current time
    path = request.url.path # Get the request path
    status = response.status_code # Get the response status code

    print(f"{request_time} {request.method} {path} -> {status} ({latency_ms:.2f} ms)")
    return response # The response must be returned, otherwise, the client never receives a response

@app.get("/health")
def get_health():
    return {"status": "ok"}


@app.post ("/calculate/{operation}/{operand_a}/{operand_b}")
def perform_calculation(operation: operations, operand_a: float, operand_b: float):
    if operation is operations.add:
        result = operand_a + operand_b
        output = {
        "result": result,
        "operation": operation
        }
    elif operation is operations.subtract:
        result = operand_a - operand_b
        output = {
        "result": result,
        "operation": operation
        }
    elif operation is operations.multiply:
        result = operand_a * operand_b
        output = {
        "result": result,
        "operation": operation
        }
    else:
        output = {
            "error": "operation is not valid",
            "valid_options": "add | subtract | multiply"
        }
        add_request_logging(output)
        return output
    add_request_logging(output)
    return output

def add_request_logging(result: dict):
    # Only log the 10 most recent elements
    if len(calculation_history) >= 10:
        calculation_history.pop(0)
    calculation_history.append(result)
    

@app.get ("/history")
def print_history():
    # print(f"Last 10 calculations are: \n {calculation_history}") # this is printing to the uvicorn console, not to the browser. We have to return the output
    return {
        "message": "Last 10 caclulations are:",
        "calculation_history": calculation_history
    }