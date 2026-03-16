"""
newd2p - SentenceTransformer Embedder
"""

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from src.config import get_settings
from src.utils.logger import get_logger

logger = get_logger("embedder")
settings = get_settings()

_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info(f"Loading embedding model: {settings.embedding_model}")
        _model = SentenceTransformer(settings.embedding_model)
        logger.info("Embedding model loaded")
    return _model


def embed_texts(texts: List[str]) -> np.ndarray:
    """Generate embeddings for a list of texts"""
    model = get_model()
    embeddings = model.encode(texts, show_progress_bar=False)
    logger.info(f"Generated {len(texts)} embeddings")
    return np.array(embeddings)


def embed_single(text: str) -> np.ndarray:
    """Generate embedding for a single text"""
    model = get_model()
    embedding = model.encode([text], show_progress_bar=False)
    return np.array(embedding[0])
