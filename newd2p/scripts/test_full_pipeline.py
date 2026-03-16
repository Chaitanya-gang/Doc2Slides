"""
newd2p - Full Pipeline: Document → PPT + JSON
"""

import sys
sys.path.insert(0, ".")

from src.parsers.parser_factory import parse_document
from src.rag.pipeline import RAGPipeline
from src.ppt.builder import PPTBuilder
from src.output.json_builder import build_handover_json


def test_full():
    print("=" * 50)
    print("FULL PIPELINE: Document → PPT + JSON")
    print("=" * 50)

    # Step 1: Parse
    print("\n📄 Step 1: Parsing document...")
    doc = parse_document(
        file_path="samples/input/sample.txt",
        file_id="test_006",
        file_extension=".txt"
    )
    print(f"   ✅ {doc.total_words} words, {len(doc.sections)} sections")

    # Step 2: RAG
    print("\n🔗 Step 2: RAG pipeline...")
    rag = RAGPipeline()
    result = rag.process_document(doc)
    print(f"   ✅ Context: {len(result['context'])} chars")

    # Step 3: Generate slide content
    print("\n🎬 Step 3: Generating slide content (1-2 minutes)...")
    narrative = rag.generate_narrative(
        context=result['context'],
        style="ted_talk",
        slide_count=8,
    )
    print(f"   ✅ Slide content: {len(narrative)} chars")

    # Step 4: Build PPT (all themes)
    print("\n🎨 Step 4: Building PPTs...")
    themes = ["vibrant", "ocean", "sunset", "royal", "emerald"]
    for t in themes:
        builder = PPTBuilder(t)
        path = f"generated_output/ppts/presentation_{t}.pptx"
        builder.build_from_json(narrative, path)
        print(f"   ✅ {t}: {path}")

    # Step 5: Handover JSON
    print("\n📋 Step 5: Handover JSON...")
    json_path = "generated_output/jsons/handover.json"
    build_handover_json(
        narrative_json=narrative,
        doc_summary=result['summary'],
        file_id="test_006",
        filename="sample.txt",
        output_path=json_path,
    )
    print(f"   ✅ JSON: {json_path}")

    print("\n" + "=" * 50)
    print("🎉 DONE! Check generated_output/ppts/")
    print("=" * 50)


if __name__ == "__main__":
    test_full()
