"""
newd2p - LLM Provider Factory
"""

from src.llm.base_provider import BaseLLMProvider
from src.llm.ollama_provider import OllamaProvider
from src.config import get_settings
from src.utils.logger import get_logger

logger = get_logger("provider_factory")
settings = get_settings()

_provider = None


def get_llm_provider() -> BaseLLMProvider:
    """Get the configured LLM provider"""
    global _provider

    if _provider is None:
        if settings.llm_provider == "ollama":
            _provider = OllamaProvider()
            logger.info("Using Ollama LLM provider")
        else:
            _provider = OllamaProvider()
            logger.info("Defaulting to Ollama LLM provider")

    return _provider
