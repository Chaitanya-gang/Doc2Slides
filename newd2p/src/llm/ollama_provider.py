"""
newd2p - Ollama LLM Provider
"""

import ollama
from src.llm.base_provider import BaseLLMProvider
from src.config import get_settings
from src.utils.logger import get_logger

logger = get_logger("ollama_provider")
settings = get_settings()


class OllamaProvider(BaseLLMProvider):

    def __init__(self):
        self.model = settings.ollama_model
        self.base_url = settings.ollama_base_url
        self.client = ollama.Client(host=self.base_url)

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate text using Ollama"""

        try:
            messages = []

            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt,
                })

            messages.append({
                "role": "user",
                "content": prompt,
            })

            logger.info(f"Sending prompt to {self.model} ({len(prompt)} chars)...")

            response = self.client.chat(
                model=self.model,
                messages=messages,
            )

            if hasattr(response, "message") and hasattr(response.message, "content"):
                result = response.message.content
            else:
                result = response["message"]["content"]
            logger.info(f"Response received: {len(result)} chars")
            return result

        except Exception as e:
            logger.error(f"Ollama error: {e}")
            raise

    def is_available(self) -> bool:
        """Check if Ollama is running and model exists"""
        try:
            response = self.client.list()
            raw_models = getattr(response, "models", None)
            if raw_models is None and isinstance(response, dict):
                raw_models = response.get("models", [])
            raw_models = raw_models or []

            model_names = []
            for model in raw_models:
                if isinstance(model, dict):
                    name = model.get("name") or model.get("model")
                else:
                    name = getattr(model, "name", None) or getattr(model, "model", None)
                if name:
                    model_names.append(str(name))

            requested = self.model.lower()
            available = any(
                requested == name.lower() or
                name.lower().startswith(f"{requested}:") or
                requested in name.lower()
                for name in model_names
            )
            logger.info(f"Ollama available: {available}, Models: {model_names}")
            return available
        except Exception as e:
            logger.error(f"Ollama not available: {e}")
            return False

    def get_model_info(self) -> dict:
        """Get model information"""
        return {
            "provider": "ollama",
            "model": self.model,
            "base_url": self.base_url,
        }
