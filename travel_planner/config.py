import os
import logging
from functools import lru_cache
from crewai import LLM

# Load API Keys
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
SERP_API_KEY = os.environ.get("SERP_API_KEY")

# Initialize Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def initialize_llm():
    """Initialize and cache the LLM instance to avoid repeated initializations."""
    return LLM(
        model="gemini/gemini-2.0-flash",
        provider="google",
        api_key=GEMINI_API_KEY
    )
