"""Shared, validated settings for demos 10–12. Never log API keys."""
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv(Path(__file__).with_name(".env"), override=False)


def build_model() -> ChatGroq:
    """Create a model without making a network request."""
    if not os.getenv("GROQ_API_KEY", "").strip():
        raise ValueError("Set GROQ_API_KEY in the project .env file.")
    timeout = float(os.getenv("GROQ_TIMEOUT_SECONDS", "30"))
    retries = int(os.getenv("GROQ_MAX_RETRIES", "2"))
    tokens = int(os.getenv("GROQ_MAX_TOKENS", "1024"))
    if timeout <= 0 or retries < 0 or tokens <= 0:
        raise ValueError("Timeout/tokens must be positive; retries must be nonnegative.")
    return ChatGroq(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        temperature=float(os.getenv("GROQ_TEMPERATURE", "0")),
        timeout=timeout, max_retries=retries, max_tokens=tokens,
    )
