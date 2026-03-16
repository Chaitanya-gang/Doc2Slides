"""
newd2p - FAISS Vector Store
"""

from typing import List, Tuple
import numpy as np
import faiss
from src.chunking.models import TextChunk
from src.embeddings.embedder import embed_texts, embed_single
from src.utils.logger import get_logger

logger = get_logger("vector_store")


class VectorStore:

    def __init__(self):
        self.index = None
        self.chunks: List[TextChunk] = []
        self.dimension = None

    def build_index(self, chunks: List[TextChunk]):
        """Build FAISS index from text chunks"""

        if not chunks:
            logger.warning("No chunks to index")
            return

        self.chunks = chunks
        texts = [chunk.text for chunk in chunks]

        logger.info(f"Embedding {len(texts)} chunks...")
        embeddings = embed_texts(texts)

        self.dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings.astype(np.float32))

        logger.info(f"FAISS index built: {self.index.ntotal} vectors, dimension {self.dimension}")

    def search(self, query: str, top_k: int = 5) -> List[Tuple[TextChunk, float]]:
        """Search for similar chunks"""

        if self.index is None or self.index.ntotal == 0:
            logger.warning("Index is empty")
            return []

        query_embedding = embed_single(query).astype(np.float32).reshape(1, -1)
        distances, indices = self.index.search(query_embedding, min(top_k, self.index.ntotal))

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.chunks):
                results.append((self.chunks[idx], float(dist)))

        logger.info(f"Search returned {len(results)} results for: {query[:50]}...")
        return results

    def get_all_chunks(self) -> List[TextChunk]:
        """Return all stored chunks"""
        return self.chunks

    @property
    def size(self) -> int:
        return self.index.ntotal if self.index else 0
