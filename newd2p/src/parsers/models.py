"""
newd2p - Parser Data Models
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class ExtractedTable:
    table_id: str
    headers: List[str]
    rows: List[List[str]]
    page_number: Optional[int] = None
    caption: Optional[str] = None

    @property
    def num_rows(self) -> int:
        return len(self.rows)

    @property
    def num_cols(self) -> int:
        return len(self.headers) if self.headers else 0


@dataclass
class DocumentSection:
    level: int
    title: str
    content: str
    page_number: Optional[int] = None


@dataclass
class ParsedDocument:
    file_id: str
    filename: str
    file_type: str
    total_pages: int
    raw_text: str
    cleaned_text: str
    sections: List[DocumentSection] = field(default_factory=list)
    tables: List[ExtractedTable] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

    @property
    def total_characters(self) -> int:
        return len(self.cleaned_text)

    @property
    def total_words(self) -> int:
        return len(self.cleaned_text.split())

    @property
    def has_tables(self) -> bool:
        return len(self.tables) > 0

    def summary(self) -> dict:
        return {
            "file_id": self.file_id,
            "filename": self.filename,
            "file_type": self.file_type,
            "total_pages": self.total_pages,
            "total_words": self.total_words,
            "total_characters": self.total_characters,
            "sections_found": len(self.sections),
            "tables_found": len(self.tables),
        }
