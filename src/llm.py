"""
LLM client. The whole point of this file: every model call goes through
ONE function. Swap the body to move from OpenAI to Bedrock without
touching the rest of the app. This is your "vendor flexibility" talking point.
"""
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # reads .env and loads it into the environment

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

MODEL = "gpt-4o-mini"  # cheap + fast; fine for tagging/summarization


def call_llm(prompt: str, system: str = "You are a helpful assistant.") -> str:
    """Send a prompt, get raw text back. The single choke-point for model calls."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,  # low = more consistent structured output
    )
    return response.choices[0].message.content


# --- Day 2 will add this: structured JSON instead of raw text ---
def call_llm_json(prompt: str, system: str) -> dict:
    """
    Ask the model for JSON and parse it safely.
    Models sometimes wrap JSON in ```json fences or add stray text,
    so we strip and guard. Returning None signals 'parse failed' to the caller.
    """
    raw = call_llm(prompt, system)
    cleaned = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None  # caller decides what to do -> this is your guardrail hook
