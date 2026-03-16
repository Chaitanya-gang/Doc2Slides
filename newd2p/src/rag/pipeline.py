"""
newd2p - RAG Pipeline
Retrieval Augmented Generation
"""

from typing import List
from src.parsers.models import ParsedDocument
from src.chunking.recursive_chunker import RecursiveChunker
from src.embeddings.vector_store import VectorStore
from src.llm.provider_factory import get_llm_provider
from src.llm.prompt_templates import SYSTEM_PROMPT, NARRATIVE_PROMPT, SUMMARY_PROMPT
from src.config import get_settings
from src.utils.logger import get_logger

logger = get_logger("rag_pipeline")
settings = get_settings()


class RAGPipeline:

    def __init__(self):
        self.chunker = RecursiveChunker()
        self.vector_store = VectorStore()
        self.llm = get_llm_provider()

    def process_document(self, doc: ParsedDocument) -> dict:
        """Full RAG pipeline: chunk → embed → retrieve → generate"""

        # Step 1: Chunk
        logger.info("Step 1: Chunking document...")
        chunks = self.chunker.chunk_document(doc)

        # Step 2: Build vector index
        logger.info("Step 2: Building vector index...")
        self.vector_store.build_index(chunks)

        # Step 3: Build context from all chunks
        logger.info("Step 3: Building context...")
        context = self._build_context(chunks)

        # Step 4: Get document summary
        logger.info("Step 4: Getting document summary...")
        summary = self._get_summary(context)

        return {
            "chunks": chunks,
            "context": context,
            "summary": summary,
            "vector_store": self.vector_store,
        }

    def generate_narrative(self, context: str, style: str = "ted_talk", slide_count: int = 10) -> str:
        """Generate narrative presentation JSON from context"""

        logger.info(f"Generating narrative: {style} style, {slide_count} slides")

        prompt = NARRATIVE_PROMPT.format(
            context=context,
            style=style,
            slide_count=slide_count,
        )

        response = self.llm.generate(prompt, system_prompt=SYSTEM_PROMPT)
        logger.info(f"Narrative generated: {len(response)} chars")
        return response

    def search_context(self, query: str, top_k: int = 5) -> str:
        """Search vector store and build context"""

        results = self.vector_store.search(query, top_k=top_k)
        context_parts = [chunk.text for chunk, _ in results]
        return "\n\n".join(context_parts)

    def _build_context(self, chunks) -> str:
        """Build full context from chunks"""

        max_chunks = settings.max_chunks_for_context
        selected = chunks[:max_chunks]
        context = "\n\n---\n\n".join([chunk.text for chunk in selected])
        logger.info(f"Context built: {len(context)} chars from {len(selected)} chunks")
        return context

    def _get_summary(self, context: str) -> str:
        """Get document summary from LLM"""

        try:
            prompt = SUMMARY_PROMPT.format(content=context[:3000])
            summary = self.llm.generate(prompt, system_prompt=SYSTEM_PROMPT)
            return summary
        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            return "{}"
