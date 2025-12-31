"""
OpenAI API hello world.

This module provides a simple interface to interact with OpenAI's GPT-4o-mini model
for text generation tasks. It demonstrates basic usage of the OpenAI client library
with API key management and response processing.

Example Usage:
    >>> # Set environment variable first
    >>> os.environ["OPENAI_API_KEY"] = "xxxxx"
    >>> # The script will automatically use the API key
    >>> # and generate a response to "Say hello"
    >>> # Output will be the generated message content

Note:
    - Requires OPENAI_API_KEY environment variable to be set
    - Uses GPT-4o-mini model for free-tier text generation
    - Designed for learning and demonstration purposes

Author: Mohammed Abdelalim
Version: 1.0
License: MIT
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    # cheaper for learning
    messages=[
        {
            "role": "user",
            "content": "Say hello"
        }
    ]
)

print(response.choices[0].message.content)
