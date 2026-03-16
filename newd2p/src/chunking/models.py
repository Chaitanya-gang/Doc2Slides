"""
newd2p - Chunk Data Models
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TextChunk:
    chunk_id: str
    text: str
    source_section: Optional[str] = None
    page_number: Optional[int] = None
    chunk_index: int = 0
    total_chunks: int = 0

    @property
    def word_count(self) -> int:
        return len(self.text.split())

    @property
    def char_count(self) -> int:
        return len(self.text)

    def to_dict(self) -> dict:
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "source_section": self.source_section,
            "page_number": self.page_number,
            "chunk_index": self.chunk_index,
            "word_count": self.word_count,
        }
