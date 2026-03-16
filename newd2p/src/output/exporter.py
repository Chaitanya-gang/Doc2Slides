"""
newd2p - Export Helpers (PDF / others)
"""

from pathlib import Path
from typing import Optional

from src.utils.logger import get_logger


logger = get_logger("exporter")


def convert_ppt_to_pdf(ppt_path: str, pdf_path: str) -> Optional[str]:
    """
    Convert a PPTX file to PDF.

    Uses pptx2pdf if available; otherwise returns None.
    """
    try:
        from pptx2pdf import convert  # type: ignore
    except Exception:
        logger.warning("pptx2pdf not installed, skipping PDF export")
        return None

    try:
        Path(pdf_path).parent.mkdir(parents=True, exist_ok=True)
        convert(ppt_path, pdf_path)
        logger.info(f"PDF export saved: {pdf_path}")
        return pdf_path
    except Exception as e:
        logger.error(f"PDF export failed: {e}")
        return None

