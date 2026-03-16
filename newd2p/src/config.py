"""
newd2p - Central Configuration
"""

from pathlib import Path
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "newd2p"
    app_version: str = "0.1.0"
    debug: bool = True
    log_level: str = "INFO"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    ollama_timeout: int = 300

    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_dimension: int = 384

    faiss_index_path: str = "./data/faiss_index"

    upload_dir: str = "./temp_uploads"
    output_dir: str = "./generated_output"
    ppt_output_dir: str = "./generated_output/ppts"
    json_output_dir: str = "./generated_output/jsons"
    narration_output_dir: str = "./generated_output/narrations"
    chart_output_dir: str = "./generated_output/charts"
    image_output_dir: str = "./generated_output/images"
    diagram_output_dir: str = "./generated_output/diagrams"
    pdf_output_dir: str = "./generated_output/pdfs"
    markdown_output_dir: str = "./generated_output/markdown"

    default_slide_count: int = 10
    max_slide_count: int = 15
    min_slide_count: int = 6

    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_chunks_for_context: int = 15

    sarvam_api_key: Optional[str] = None
    sarvam_api_url: str = "https://api.sarvam.ai"
    krutrim_api_key: Optional[str] = None

    llm_provider: str = "ollama"

    host: str = "0.0.0.0"
    port: int = 8000
    streamlit_port: int = 8501

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on", "debug", "development"}:
                return True
            if normalized in {"0", "false", "no", "off", "release", "prod", "production"}:
                return False
        return bool(value)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


_settings = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def ensure_directories():
    settings = get_settings()
    dirs = [
        settings.upload_dir,
        settings.output_dir,
        settings.ppt_output_dir,
        settings.json_output_dir,
        settings.narration_output_dir,
        settings.chart_output_dir,
            settings.image_output_dir,
            settings.diagram_output_dir,
            settings.pdf_output_dir,
            settings.markdown_output_dir,
        settings.faiss_index_path,
        "./data",
        "./logs",
    ]
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)


SUPPORTED_EXTENSIONS = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".doc": "docx",
    ".txt": "text",
}

PRESENTATION_STYLES = {
    "ted_talk": {
        "name": "TED Talk",
        "description": "Engaging, story-driven narrative",
        "tone": "inspiring, clear, conversational",
    },
    "executive_summary": {
        "name": "Executive Summary",
        "description": "Concise, data-driven for leadership",
        "tone": "professional, direct, authoritative",
    },
    "training": {
        "name": "Training / Educational",
        "description": "Step-by-step educational",
        "tone": "clear, patient, instructional",
    },
    "storytelling": {
        "name": "Storytelling",
        "description": "Narrative-driven, emotional",
        "tone": "warm, engaging, relatable",
    },
    "pitch_deck": {
        "name": "Pitch Deck",
        "description": "Startup/business pitch",
        "tone": "confident, exciting, persuasive",
    },
}
