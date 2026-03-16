"""
newd2p - Download Endpoint
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from src.config import get_settings
from src.utils.logger import get_logger

logger = get_logger("api_download")
router = APIRouter()
settings = get_settings()


@router.get("/download/ppt/{file_id}")
async def download_ppt(file_id: str):
    """Download generated PPT"""
    ppt_path = Path(f"{settings.ppt_output_dir}/{file_id}_presentation.pptx")

    if not ppt_path.exists():
        raise HTTPException(status_code=404, detail="PPT not found. Generate first.")

    return FileResponse(
        path=str(ppt_path),
        filename=f"{file_id}_presentation.pptx",
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )


@router.get("/download/json/{file_id}")
async def download_json(file_id: str):
    """Download handover JSON"""
    json_path = Path(f"{settings.json_output_dir}/{file_id}_handover.json")

    if not json_path.exists():
        raise HTTPException(status_code=404, detail="JSON not found. Generate first.")

    return FileResponse(
        path=str(json_path),
        filename=f"{file_id}_handover.json",
        media_type="application/json",
    )


@router.get("/download/pdf/{file_id}")
async def download_pdf(file_id: str):
    """Download generated PDF (if available)"""
    pdf_path = Path(f"{settings.pdf_output_dir}/{file_id}_presentation.pdf")

    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF not found. Generate with PDF export enabled.")

    return FileResponse(
        path=str(pdf_path),
        filename=f"{file_id}_presentation.pdf",
        media_type="application/pdf",
    )


@router.get("/download/markdown/{file_id}")
async def download_markdown(file_id: str):
    """Download generated Markdown export (if available)"""
    md_path = Path(f"{settings.markdown_output_dir}/{file_id}_presentation.md")

    if not md_path.exists():
        raise HTTPException(status_code=404, detail="Markdown not found. Generate with Markdown export enabled.")

    return FileResponse(
        path=str(md_path),
        filename=f"{file_id}_presentation.md",
        media_type="text/markdown",
    )
