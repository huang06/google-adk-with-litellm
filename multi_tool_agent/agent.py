from __future__ import annotations

import os
import random

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_API_BASE = os.getenv("AZURE_API_BASE")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
MODEL_NAME = "azure/gpt-35-turbo-auto"


# Tool: Currency conversion (mock)
def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convert currency using mock rates.

    Args:
        amount: Amount to convert.
        from_currency: Source currency code.
        to_currency: Target currency code.

    Returns:
        dict: Conversion result or error message.
    """
    rates = {("USD", "TWD"): 32.5, ("TWD", "USD"): 0.031}
    key = (from_currency.upper(), to_currency.upper())
    if key in rates:
        result = amount * rates[key]
        return {"status": "ok", "result": f"{amount} {from_currency}  {result:.2f} {to_currency}"}
    return {"status": "fail", "error_message": "Conversion rate not available."}


# Tool: Random joke
def tell_joke() -> dict:
    """Return a random joke.

    Returns:
        dict: A random joke.
    """
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the math book look sad? Because it had too many problems.",
    ]
    return {"status": "ok", "joke": random.choice(jokes)}  # nosec


# Tool: Simple math
def multiply(a: float, b: float) -> dict:
    """Multiply two numbers.

    Args:
        a: First number.
        b: Second number.

    Returns:
        dict: Multiplication result.
    """
    return {"status": "ok", "result": a * b}


root_agent = Agent(
    name="utility_agent",
    model=LiteLlm(model=MODEL_NAME),
    description="Agent for currency conversion, jokes, and math operations.",
    instruction="Ask me to convert currency, tell a joke, or do simple math!",
    tools=[convert_currency, tell_joke, multiply],
)
