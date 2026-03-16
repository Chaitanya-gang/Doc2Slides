"""
newd2p - PDF Parser
Uses PyMuPDF for text and pdfplumber for tables
"""

import fitz  # PyMuPDF
import pdfplumber
from pathlib import Path
from src.parsers.base_parser import BaseParser
from src.parsers.models import ParsedDocument, DocumentSection, ExtractedTable
from src.utils.text_cleaner import clean_text
from src.utils.logger import get_logger

logger = get_logger("pdf_parser")


class PDFParser(BaseParser):

    def can_parse(self, file_extension: str) -> bool:
        return file_extension.lower() in [".pdf"]

    def parse(self, file_path: str, file_id: str) -> ParsedDocument:
        logger.info(f"Parsing PDF: {file_path}")

        path = Path(file_path)
        raw_text = self._extract_text(file_path)
        cleaned = clean_text(raw_text)
        sections = self._extract_sections(file_path)
        tables = self._extract_tables(file_path)
        total_pages = self._get_page_count(file_path)

        doc = ParsedDocument(
            file_id=file_id,
            filename=path.name,
            file_type="pdf",
            total_pages=total_pages,
            raw_text=raw_text,
            cleaned_text=cleaned,
            sections=sections,
            tables=tables,
            metadata={
                "file_size": path.stat().st_size,
                "page_count": total_pages,
            }
        )

        logger.info(f"PDF parsed: {doc.total_words} words, {len(sections)} sections, {len(tables)} tables")
        return doc

    def _get_page_count(self, file_path: str) -> int:
        try:
            pdf = fitz.open(file_path)
            count = len(pdf)
            pdf.close()
            return count
        except Exception as e:
            logger.error(f"Error getting page count: {e}")
            return 1

    def _extract_text(self, file_path: str) -> str:
        try:
            pdf = fitz.open(file_path)
            text_parts = []
            for page_num in range(len(pdf)):
                page = pdf[page_num]
                text = page.get_text()
                if text.strip():
                    text_parts.append(text)
            pdf.close()
            return "\n\n".join(text_parts)
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return ""

    def _extract_sections(self, file_path: str) -> list:
        sections = []
        try:
            pdf = fitz.open(file_path)

            for page_num in range(len(pdf)):
                page = pdf[page_num]
                blocks = page.get_text("dict")["blocks"]

                for block in blocks:
                    if "lines" not in block:
                        continue

                    for line in block["lines"]:
                        text = ""
                        max_font_size = 0

                        for span in line["spans"]:
                            text += span["text"]
                            if span["size"] > max_font_size:
                                max_font_size = span["size"]

                        text = text.strip()
                        if not text:
                            continue

                        # Detect headings by font size
                        if max_font_size > 14:
                            level = 1 if max_font_size > 18 else 2
                            sections.append(DocumentSection(
                                level=level,
                                title=text,
                                content="",
                                page_number=page_num + 1,
                            ))
                        elif sections:
                            # Add content to last section
                            sections[-1].content += text + " "

            pdf.close()

            # If no sections found, create one big section
            if not sections:
                full_text = self._extract_text(file_path)
                sections.append(DocumentSection(
                    level=1,
                    title="Document Content",
                    content=full_text,
                    page_number=1,
                ))

        except Exception as e:
            logger.error(f"Error extracting sections: {e}")

        return sections

    def _extract_tables(self, file_path: str) -> list:
        tables = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()

                    for idx, table in enumerate(page_tables):
                        if not table or len(table) < 2:
                            continue

                        headers = [str(cell or "") for cell in table[0]]
                        rows = []
                        for row in table[1:]:
                            rows.append([str(cell or "") for cell in row])

                        tables.append(ExtractedTable(
                            table_id=f"table_p{page_num+1}_{idx+1}",
                            headers=headers,
                            rows=rows,
                            page_number=page_num + 1,
                        ))

        except Exception as e:
            logger.error(f"Error extracting tables: {e}")

        return tables
