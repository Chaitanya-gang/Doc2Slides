"""
newd2p - FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config import get_settings, ensure_directories, PRESENTATION_STYLES
from src.utils.logger import setup_logger, get_logger
from src.api.routes import upload, generate, download

settings = get_settings()
logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger(settings.log_level)
    ensure_directories()
    logger.info(f"🚀 {settings.app_name} v{settings.app_version} starting...")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    logger.info(f"Ollama Model: {settings.ollama_model}")
    yield
    logger.info(f"👋 {settings.app_name} shutting down...")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered document to narrative presentation converter.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(generate.router, prefix="/api", tags=["Generate"])
app.include_router(download.router, prefix="/api", tags=["Download"])


@app.get("/")
async def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "endpoints": {
            "upload": "POST /api/upload",
            "generate": "POST /api/generate",
            "download_ppt": "GET /api/download/ppt/{file_id}",
            "download_json": "GET /api/download/json/{file_id}",
            "styles": "GET /api/styles",
            "health": "GET /health",
        }
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "version": settings.app_version}


@app.get("/api/styles")
async def get_styles():
    return {
        "presentation_styles": PRESENTATION_STYLES,
        "themes": ["vibrant", "ocean", "sunset", "forest", "royal"],
        "templates": {
            "academic": {"style": "training", "theme": "forest"},
            "business": {"style": "executive_summary", "theme": "royal"},
            "ted_talk": {"style": "ted_talk", "theme": "sunset"},
            "minimal": {"style": "training", "theme": "vibrant"},
        },
        "export_formats": ["pptx", "pdf", "markdown"],
    }
