"""
newd2p - Recursive Text Chunker
Splits text into overlapping chunks
"""

from typing import List
from src.chunking.models import TextChunk
from src.parsers.models import ParsedDocument
from src.config import get_settings
from src.utils.logger import get_logger

logger = get_logger("recursive_chunker")
settings = get_settings()


class RecursiveChunker:

    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap

    def chunk_document(self, doc: ParsedDocument) -> List[TextChunk]:
        """Chunk a parsed document into text chunks"""

        chunks = []

        # If document has sections, chunk by section
        if doc.sections:
            for section in doc.sections:
                section_text = f"{section.title}\n\n{section.content}"
                section_chunks = self._split_text(
                    text=section_text,
                    source_section=section.title,
                    page_number=section.page_number,
                )
                chunks.extend(section_chunks)
        else:
            # Chunk the full text
            chunks = self._split_text(
                text=doc.cleaned_text,
                source_section="Full Document",
            )

        # Set chunk indices
        for i, chunk in enumerate(chunks):
            chunk.chunk_index = i
            chunk.total_chunks = len(chunks)

        logger.info(f"Document chunked into {len(chunks)} chunks")
        return chunks

    def _split_text(
        self,
        text: str,
        source_section: str = None,
        page_number: int = None,
    ) -> List[TextChunk]:
        """Split text into chunks with overlap"""

        if not text or not text.strip():
            return []

        # If text is small enough, return as single chunk
        if len(text) <= self.chunk_size:
            return [TextChunk(
                chunk_id=f"chunk_0",
                text=text.strip(),
                source_section=source_section,
                page_number=page_number,
            )]

        chunks = []
        separators = ["\n\n", "\n", ". ", " "]

        parts = self._recursive_split(text, separators)

        current_chunk = ""
        chunk_count = 0

        for part in parts:
            if len(current_chunk) + len(part) <= self.chunk_size:
                current_chunk += part
            else:
                if current_chunk.strip():
                    chunks.append(TextChunk(
                        chunk_id=f"chunk_{chunk_count}",
                        text=current_chunk.strip(),
                        source_section=source_section,
                        page_number=page_number,
                    ))
                    chunk_count += 1

                    # Add overlap
                    overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else ""
                    current_chunk = overlap_text + part
                else:
                    current_chunk = part

        # Add last chunk
        if current_chunk.strip():
            chunks.append(TextChunk(
                chunk_id=f"chunk_{chunk_count}",
                text=current_chunk.strip(),
                source_section=source_section,
                page_number=page_number,
            ))

        return chunks

    def _recursive_split(self, text: str, separators: list) -> list:
        """Split text using separators in order of preference"""

        if not separators:
            return [text]

        separator = separators[0]
        parts = text.split(separator)

        result = []
        for i, part in enumerate(parts):
            if i < len(parts) - 1:
                result.append(part + separator)
            else:
                result.append(part)

        return result
