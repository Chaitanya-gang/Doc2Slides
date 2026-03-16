"""
newd2p - Abstract Base Parser
All parsers must inherit from this
"""

from abc import ABC, abstractmethod
from src.parsers.models import ParsedDocument


class BaseParser(ABC):

    @abstractmethod
    def parse(self, file_path: str, file_id: str) -> ParsedDocument:
        raise NotImplementedError

    @abstractmethod
    def can_parse(self, file_extension: str) -> bool:
        raise NotImplementedError
