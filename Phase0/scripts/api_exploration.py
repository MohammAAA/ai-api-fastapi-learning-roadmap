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
import argparse
from tabulate import tabulate
from app.services.openai_benchmark import run_once


def parse_args():
    parser = argparse.ArgumentParser(
        description="Benchmark OpenAI models across chat_completions vs responses."
    )

    parser.add_argument("--prompt", required=True, type=str, help="Prompt to send")
    parser.add_argument(
        "--models",
        nargs="+",
        default=["gpt-4o-mini", "gpt-4.1-nano"],
        help="Models to test (space-separated)",
    )
    parser.add_argument(
        "--apis",
        nargs="+",
        default=["chat_completions", "responses"],
        help="API types to test (chat_completions, responses)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Temperature (optional). If omitted, API default is used.",
    )
    parser.add_argument(
        "--tablefmt",
        type=str,
        default="github",
        help="tabulate format (e.g., github, pipe, grid)",
    )
    return parser.parse_args()

def print_response(model: str, response: str):
    print(f"{model} response with chat_completions API: \n {response}\n")
    print("-----\n")

def main():
    args = parse_args()

    benchmark_results = []
    for model in args.models:
        for api_type in args.apis:
            model_response = run_once(
                prompt=args.prompt,
                model=model,
                api_type=api_type,
                temperature=args.temperature,
            )
            benchmark_results.append(model_response)

    # Dynamic table
    # Sort for nicer readability
    benchmark_results.sort(key=lambda x: (x["model"], x["api_type"]))
    print("Comparison summary: \n")
    print(tabulate(benchmark_results, headers="keys", tablefmt=args.tablefmt))


if __name__ == "__main__":
    main()
