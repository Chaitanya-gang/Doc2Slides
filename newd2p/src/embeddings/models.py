"""
newd2p - Embedding Data Models
"""

from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class EmbeddedChunk:
    chunk_id: str
    text: str
    embedding: np.ndarray
    source_section: str = None

    def to_dict(self) -> dict:
        return {
            "chunk_id": self.chunk_id,
            "text": self.text,
            "source_section": self.source_section,
        }
