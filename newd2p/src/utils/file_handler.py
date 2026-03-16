"""
newd2p - File Upload & Management
"""

import uuid
import shutil
from pathlib import Path
from datetime import datetime
from typing import Tuple
from dataclasses import dataclass

from src.config import get_settings, SUPPORTED_EXTENSIONS
from src.utils.logger import get_logger

logger = get_logger("file_handler")
settings = get_settings()


@dataclass
class UploadedFile:
    file_id: str
    original_filename: str
    saved_path: str
    file_extension: str
    file_type: str
    file_size_bytes: int
    file_size_readable: str
    uploaded_at: str
    status: str = "uploaded"

    def to_dict(self) -> dict:
        return self.__dict__


def get_readable_size(size_bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def validate_file(filename: str) -> Tuple[bool, str]:
    if not filename:
        return False, "No filename provided"

    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(SUPPORTED_EXTENSIONS.keys())
        return False, f"Unsupported: {extension}. Supported: {supported}"

    return True, f"File type {extension} is supported"


def save_uploaded_file(file_content: bytes, original_filename: str) -> UploadedFile:
    is_valid, message = validate_file(original_filename)
    if not is_valid:
        raise ValueError(message)

    file_id = str(uuid.uuid4())[:12]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    extension = Path(original_filename).suffix.lower()
    file_type = SUPPORTED_EXTENSIONS[extension]

    save_dir = Path(settings.upload_dir) / file_id
    save_dir.mkdir(parents=True, exist_ok=True)

    saved_filename = f"{timestamp}_{original_filename}"
    saved_path = save_dir / saved_filename

    with open(saved_path, "wb") as f:
        f.write(file_content)

    file_size = len(file_content)

    uploaded = UploadedFile(
        file_id=file_id,
        original_filename=original_filename,
        saved_path=str(saved_path),
        file_extension=extension,
        file_type=file_type,
        file_size_bytes=file_size,
        file_size_readable=get_readable_size(file_size),
        uploaded_at=datetime.now().isoformat(),
    )

    logger.info(f"File saved: {original_filename} ({uploaded.file_size_readable})")
    return uploaded


def cleanup_file(file_id: str):
    file_dir = Path(settings.upload_dir) / file_id
    if file_dir.exists():
        shutil.rmtree(file_dir)
        logger.info(f"Cleaned up: {file_id}")
