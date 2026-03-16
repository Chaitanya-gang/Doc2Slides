"""
newd2p - Input Validation
"""

from src.config import SUPPORTED_EXTENSIONS, PRESENTATION_STYLES
from src.constants import MAX_FILE_SIZE_BYTES, MIN_SLIDES, MAX_SLIDES


def validate_file_size(size_bytes: int) -> tuple:
    if size_bytes > MAX_FILE_SIZE_BYTES:
        return False, f"File too large. Max: {MAX_FILE_SIZE_BYTES // (1024*1024)}MB"
    if size_bytes == 0:
        return False, "File is empty"
    return True, "OK"


def validate_slide_count(count: int) -> tuple:
    if count < MIN_SLIDES:
        return False, f"Minimum slides: {MIN_SLIDES}"
    if count > MAX_SLIDES:
        return False, f"Maximum slides: {MAX_SLIDES}"
    return True, "OK"


def validate_style(style: str) -> tuple:
    if style not in PRESENTATION_STYLES:
        available = ", ".join(PRESENTATION_STYLES.keys())
        return False, f"Unknown style. Available: {available}"
    return True, "OK"
