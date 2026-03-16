"""
newd2p - Upload Endpoint
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from src.utils.file_handler import save_uploaded_file, validate_file
from src.utils.logger import get_logger

logger = get_logger("api_upload")
router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document for processing"""

    is_valid, message = validate_file(file.filename)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    content = await file.read()

    if len(content) == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    uploaded = save_uploaded_file(content, file.filename)

    return {
        "status": "uploaded",
        "file_id": uploaded.file_id,
        "filename": uploaded.original_filename,
        "file_type": uploaded.file_type,
        "file_size": uploaded.file_size_readable,
        "message": f"File uploaded successfully. Use file_id '{uploaded.file_id}' to generate presentation.",
    }
