"""
newd2p - Plain Text Parser
"""

import re
from pathlib import Path
from src.parsers.base_parser import BaseParser
from src.parsers.models import ParsedDocument, DocumentSection
from src.utils.text_cleaner import clean_text
from src.utils.logger import get_logger

logger = get_logger("txt_parser")


class TxtParser(BaseParser):

    def can_parse(self, file_extension: str) -> bool:
        return file_extension.lower() in [".txt"]

    def parse(self, file_path: str, file_id: str) -> ParsedDocument:
        logger.info(f"Parsing TXT: {file_path}")

        path = Path(file_path)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()

        cleaned = clean_text(raw_text)
        sections = self._extract_sections(raw_text)

        # Estimate pages (roughly 3000 chars per page)
        total_pages = max(1, len(raw_text) // 3000)

        doc = ParsedDocument(
            file_id=file_id,
            filename=path.name,
            file_type="text",
            total_pages=total_pages,
            raw_text=raw_text,
            cleaned_text=cleaned,
            sections=sections,
            metadata={
                "encoding": "utf-8",
                "file_size": path.stat().st_size,
            }
        )

        logger.info(f"TXT parsed: {doc.total_words} words, {len(sections)} sections")
        return doc

    def _extract_sections(self, text: str) -> list:
        sections = []
        lines = text.split("\n")
        current_section = None
        current_content = []

        for line in lines:
            stripped = line.strip()

            # Detect headings: ALL CAPS lines or lines ending with ':'
            if stripped and (
                stripped.isupper() or
                stripped.endswith(":") or
                (len(stripped) < 80 and not stripped.endswith("."))
            ):
                # Save previous section
                if current_section:
                    sections.append(DocumentSection(
                        level=1,
                        title=current_section,
                        content="\n".join(current_content).strip(),
                    ))
                current_section = stripped.rstrip(":")
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_section:
            sections.append(DocumentSection(
                level=1,
                title=current_section,
                content="\n".join(current_content).strip(),
            ))
        elif current_content:
            sections.append(DocumentSection(
                level=1,
                title="Main Content",
                content="\n".join(current_content).strip(),
            ))

        return sections
