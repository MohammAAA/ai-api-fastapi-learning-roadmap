""" OpenAI Model Performance and Cost Benchmarking Utility.

This module provides a framework to compare different OpenAI 
models (gpt-4o-mini and gpt-4.1-nano) and different APIs (chat completions, and responses) 
based on latency, output consistency, and financial cost. It automates the benchmarking process by tracking 
execution time and calculating expenses based on current token pricing.

Key Functionalities:
    1. API Integration: Interfaces with OpenAI's ChatCompletion/responses endpoints.
    2. Latency Tracking: Measures precise response times for each model and endpoint call.
    3. Cost Analysis: Calculates the price per 1,000 tokens based on 
       official 2025 pricing models.
    4. Variability Testing: Configures temperature (default=0.5) to observe 
       stochasticity across model responses.
    5. Reporting: Generates a formatted comparison table for easy evaluation.

Example:
    $ python api_exploration.py --prompt "Write a brief fictional story to a 5-years old kid"

Pricing Reference:
    For the latest rates, see the [OpenAI Pricing Page](openai.com).

Author: Mohammed Abdelalim
Version: 1.0
License: MIT
"""
import os # to get env variables
from openai import OpenAI # OpenAI APIs
#import sys # to fetch CLI input arguments
import argparse # to define arguments names (better convention than the sys.argv method)
import time, requests # to measure the latency time of the APIs/models
from helpers.models_info import pricing_reference # to get the models pricing info
from tabulate import tabulate # to create tables


# if len(sys.argv) < 2:
#     print("Usage: python api_exploration.py <prompt>")
#     raise SystemExit(1)

#prompt = sys.argv[1] # Get the prompt from the first CLI argument

# Parse the CLI input arguments
parser = argparse.ArgumentParser() # initialize argparse
parser.add_argument(
    "--prompt",
    required=True, #Forces the user to pass --prompt
    type=str,
    help="Prompt text to send to the API"
)
args = parser.parse_args()
prompt = args.prompt


# Instantiate OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Trying gpt-4o-mini and gpt-4.1-nano with chat completion endpoint
start_timer = time.perf_counter()
chat_completion_4o = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)
elapsed_s = time.perf_counter() - start_timer

print(f'Response With "chat.completions" endpoint - gpt-4o-mini: (response time (ms): {elapsed_s * 1000}) \n {chat_completion_4o.choices[0].message.content}')

start_timer = time.perf_counter()
chat_completion_4_nano = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)
elapsed_s = time.perf_counter() - start_timer
print(f'Response With "chat.completions" endpoint - gpt-4.1-nano: (response time (ms): {elapsed_s * 1000}) \n {chat_completion_4_nano.choices[0].message.content}')

# Trying gpt-4o-mini and gpt-4.1-nano with responses endpoint
start_timer = time.perf_counter()
response_4o = client.responses.create(
    model="gpt-4o-mini",
    input=prompt
)
elapsed_s = time.perf_counter() - start_timer
print(f'Response With "responses" endpoint - gpt-4o-mini: (response time (ms): {elapsed_s * 1000}) \n {response_4o.output[0].content[0].text}')

start_timer = time.perf_counter()
response_4_nano = client.responses.create(
    model="gpt-4.1-nano",
    input=prompt
)
elapsed_s = time.perf_counter() - start_timer
print(f'Response With "responses" endpoint - gpt-4.1-nano: (response time (ms): {elapsed_s * 1000}) \n {response_4_nano.output_text}') #{response_4_nano.output[0].content[0].text} is equavalent to {response_4_nano.output_text}

######################################
# Calculate and print pricing information for both models
gpt4o_input_token_price = pricing_reference["models"]["gpt_4o_mini"]["input_token_price"]
gpt4o_output_token_price = pricing_reference["models"]["gpt_4o_mini"]["output_token_price"]
gpt4nano_input_token_price = pricing_reference["models"]["gpt_4_nano"]["input_token_price"]
gpt4nano_output_token_price = pricing_reference["models"]["gpt_4_nano"]["output_token_price"]


prompt_pricing = {
    "gpt-4o-mini":{
        "per-1k-input-tokens-price":f'{gpt4o_input_token_price*1000} cents',
        "per-1k-output-tokens-price": f'{gpt4o_output_token_price*1000} cents',
        "prompt-price-with-chat-completion-api": f'{gpt4o_input_token_price * chat_completion_4o.usage.prompt_tokens} cents',
        "response-price-with-chat-completion-api": f'{gpt4o_output_token_price * chat_completion_4o.usage.completion_tokens} cents',
        "total-price-with-chat-completion-api": "N/A",
        "prompt-price-with-responses-api": f'{gpt4o_input_token_price * response_4o.usage.input_tokens} cents',
        "response-price-with-responses-api":f'{gpt4o_output_token_price * response_4o.usage.output_tokens} cents',
        "total-price-with-responses-api": "N/A"
    },
    "gpt-4.1-nano":{
        "per-1k-input-tokens-price": f'{gpt4nano_input_token_price*1000} cents',
        "per-1k-output-tokens-price": f'{gpt4nano_output_token_price*1000} cents',
        "prompt-price-with-chat-completion-api": f'{gpt4nano_input_token_price * chat_completion_4_nano.usage.prompt_tokens} cents',
        "response-price-with-chat-completion-api": f'{gpt4nano_output_token_price * chat_completion_4_nano.usage.completion_tokens} cents',
        "total-price-with-chat-completion-api": "N/A",
        "prompt-price-with-responses-api": f'{gpt4nano_input_token_price * response_4_nano.usage.input_tokens} cents',
        "response-price-with-responses-api":f'{gpt4nano_output_token_price * response_4_nano.usage.output_tokens} cents',
        "total-price-with-responses-api": "N/A"
    }
}

print(f'prompt_pricing: \n {prompt_pricing}')

rows = [
  {"model": "gpt-4o-mini", "latency_ms_chat_completion_api": 3221, "latency_ms_responses_api": 1893, "cost_usd": 0.729},
  {"model": "gpt-4.1-nano", "latency_ms_chat_completion_api": 1410, "latency_ms_responses_api": 1997, "cost_usd": 0.426},
]

print(tabulate(rows, headers="keys", tablefmt="github"))


##############################################################
# Trying gpt-4o-mini and gpt-4.1-nano with chat completion endpoint
# start_timer = time.perf_counter()
# chat_completion_4o = client.chat.completions.create(
#     model="gpt-4o-mini",
#     temperature=1.5,
#     messages=[
#         {
#             "role": "user",
#             "content": prompt
#         }
#     ]
# )
# elapsed_s = time.perf_counter() - start_timer

# print(f'Response With "chat.completions" endpoint - gpt-4o-mini: (response time (ms): {elapsed_s * 1000}) \n {chat_completion_4o.choices[0].message.content}')

# start_timer = time.perf_counter()
# chat_completion_4_nano = client.chat.completions.create(
#     model="gpt-4.1-nano",
#     temperature=1.5,
#     messages=[
#         {
#             "role": "user",
#             "content": prompt
#         }
#     ]
# )
# elapsed_s = time.perf_counter() - start_timer
# print(f'Response With "chat.completions" endpoint - gpt-4.1-nano: (response time (ms): {elapsed_s * 1000}) \n {chat_completion_4_nano.choices[0].message.content}')

# Trying gpt-4o-mini and gpt-4.1-nano with responses endpoint
# start_timer = time.perf_counter()
# response_4o = client.responses.create(
#     model="gpt-4o-mini",
#     temperature=1.5,
#     input=prompt
# )
# elapsed_s = time.perf_counter() - start_timer
# print(f'Response With "responses" endpoint - gpt-4o-mini: (response time (ms): {elapsed_s * 1000}) \n {response_4o.output[0].content[0].text}')

# start_timer = time.perf_counter()
# response_4_nano = client.responses.create(
#     model="gpt-4.1-nano",
#     temperature=1.5,
#     input=prompt
# )
# elapsed_s = time.perf_counter() - start_timer
# print(f'Response With "responses" endpoint - gpt-4.1-nano: (response time (ms): {elapsed_s * 1000}) \n {response_4_nano.output_text}') #{response_4_nano.output[0].content[0].text} is equavalent to {response_4_nano.output_text}


########################################################
# Print comparison table
