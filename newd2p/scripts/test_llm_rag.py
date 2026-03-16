"""
newd2p - Test LLM + RAG Pipeline
"""

import sys
sys.path.insert(0, ".")

from src.parsers.parser_factory import parse_document
from src.rag.pipeline import RAGPipeline


def test_llm_rag():
    print("=" * 50)
    print("TESTING LLM + RAG PIPELINE")
    print("=" * 50)

    # Step 1: Parse
    print("\n📄 Step 1: Parsing document...")
    doc = parse_document(
        file_path="samples/input/sample.txt",
        file_id="test_002",
        file_extension=".txt"
    )
    print(f"   Parsed: {doc.total_words} words")

    # Step 2: RAG Pipeline
    print("\n🔗 Step 2: Running RAG pipeline...")
    rag = RAGPipeline()
    result = rag.process_document(doc)

    print(f"   Chunks: {len(result['chunks'])}")
    print(f"   Context length: {len(result['context'])} chars")

    print("\n📋 Step 3: Document Summary:")
    print(result['summary'])

    # Step 3: Generate narrative
    print("\n🎬 Step 4: Generating narrative (this takes 1-2 minutes)...")
    narrative = rag.generate_narrative(
        context=result['context'],
        style="ted_talk",
        slide_count=8,
    )

    print("\n--- Generated Narrative ---")
    print(narrative[:2000])
    if len(narrative) > 2000:
        print(f"\n... ({len(narrative)} total chars)")

    print("\n✅ LLM + RAG Pipeline test PASSED!")


if __name__ == "__main__":
    test_llm_rag()
