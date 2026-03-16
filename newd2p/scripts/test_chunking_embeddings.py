"""
newd2p - Test Chunking & Embeddings
"""

import sys
sys.path.insert(0, ".")

from src.parsers.parser_factory import parse_document
from src.chunking.recursive_chunker import RecursiveChunker
from src.embeddings.vector_store import VectorStore


def test_full_pipeline():
    print("=" * 50)
    print("TESTING CHUNKING + EMBEDDINGS")
    print("=" * 50)

    # Step 1: Parse document
    print("\n📄 Step 1: Parsing document...")
    doc = parse_document(
        file_path="samples/input/sample.txt",
        file_id="test_001",
        file_extension=".txt"
    )
    print(f"   Parsed: {doc.total_words} words, {len(doc.sections)} sections")

    # Step 2: Chunk document
    print("\n✂️  Step 2: Chunking document...")
    chunker = RecursiveChunker(chunk_size=500, chunk_overlap=50)
    chunks = chunker.chunk_document(doc)
    print(f"   Created {len(chunks)} chunks")
    for chunk in chunks:
        print(f"   - {chunk.chunk_id}: {chunk.word_count} words | Section: {chunk.source_section}")

    # Step 3: Build vector store
    print("\n🧠 Step 3: Building vector store (this may take a moment first time)...")
    store = VectorStore()
    store.build_index(chunks)
    print(f"   Index size: {store.size} vectors")

    # Step 4: Search
    print("\n🔍 Step 4: Testing search...")
    queries = [
        "What are the CO2 levels?",
        "How to solve climate change?",
        "Impact on food and agriculture",
    ]

    for query in queries:
        print(f"\n   Query: '{query}'")
        results = store.search(query, top_k=2)
        for chunk, distance in results:
            print(f"   → [{distance:.2f}] {chunk.source_section}: {chunk.text[:80]}...")

    print("\n✅ Chunking + Embeddings test PASSED!")


if __name__ == "__main__":
    test_full_pipeline()
