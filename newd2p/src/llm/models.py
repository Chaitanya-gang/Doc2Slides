"""
newd2p - LLM Data Models
"""

from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    model: str
    provider: str
    prompt_length: int
    response_length: int

    def to_dict(self) -> dict:
        return self.__dict__
