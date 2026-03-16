"""
newd2p - Parser Factory
Auto-selects the right parser based on file type
"""

from src.parsers.txt_parser import TxtParser
from src.parsers.pdf_parser import PDFParser
from src.parsers.docx_parser import DocxParser
from src.parsers.models import ParsedDocument
from src.utils.logger import get_logger

logger = get_logger("parser_factory")

# All available parsers
PARSERS = [
    TxtParser(),
    PDFParser(),
    DocxParser(),
]


def get_parser(file_extension: str):
    """Get the right parser for a file type"""
    for parser in PARSERS:
        if parser.can_parse(file_extension):
            logger.info(f"Selected parser: {parser.__class__.__name__} for {file_extension}")
            return parser

    raise ValueError(f"No parser found for: {file_extension}")


def parse_document(file_path: str, file_id: str, file_extension: str) -> ParsedDocument:
    """Parse any supported document"""
    parser = get_parser(file_extension)
    return parser.parse(file_path, file_id)
