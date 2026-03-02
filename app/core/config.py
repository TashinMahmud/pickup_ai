"""
Pickup AI — Configuration
Loads environment variables from .env file.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # ── Provider Selection ─────────────────────────────────────────────
    MODEL_PROVIDER: str = "openai"  # "openai" | "gemini" | "anthropic"

    # ── OpenAI ─────────────────────────────────────────────────────────
    OPENAI_API_KEY: Optional[str] = None

    # ── Gemini ─────────────────────────────────────────────────────────
    GEMINI_API_KEY: Optional[str] = None

    # ── Model Config ───────────────────────────────────────────────────
    MODEL_NAME: str = "gpt-4o-mini"  # Auto-resolved if not set
    MODEL_TEMPERATURE: float = 0.2

    # ── Database ───────────────────────────────────────────────────────
    DATABASE_URL: str = ""
    PORT: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_litellm_model(self) -> str:
        """
        Resolve the full LiteLLM model string based on provider.
        LiteLLM uses prefixes: 'gemini/' for Google, no prefix for OpenAI.
        """
        provider = self.MODEL_PROVIDER.lower()

        # If user set a custom MODEL_NAME with prefix, use it directly
        if "/" in self.MODEL_NAME:
            return self.MODEL_NAME

        # Auto-prefix based on provider
        model_defaults = {
            "openai": "gpt-4o-mini",
            "gemini": "gemini-2.0-flash",
            "anthropic": "claude-3-5-haiku-latest",
        }

        model_name = self.MODEL_NAME or model_defaults.get(provider, "gpt-4o-mini")

        prefixes = {
            "openai": "",          # No prefix for OpenAI
            "gemini": "gemini/",   # LiteLLM Gemini prefix
            "anthropic": "",       # No prefix for Anthropic
        }

        prefix = prefixes.get(provider, "")

        # Don't double-prefix
        if model_name.startswith(prefix) and prefix:
            return model_name

        return f"{prefix}{model_name}"

    def get_active_api_key(self) -> str:
        """Return the API key for the active provider."""
        provider = self.MODEL_PROVIDER.lower()
        keys = {
            "openai": self.OPENAI_API_KEY,
            "gemini": self.GEMINI_API_KEY,
            "anthropic": None,
        }
        key = keys.get(provider)
        if not key:
            raise RuntimeError(
                f"❌ No API key set for provider '{provider}'. "
                f"Set the corresponding key in your .env file."
            )
        return key


@lru_cache()
def get_settings() -> Settings:
    return Settings()
