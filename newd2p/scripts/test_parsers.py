"""
newd2p - Test Document Parsers
"""

import sys
sys.path.insert(0, ".")

from src.parsers.parser_factory import parse_document


def test_txt():
    print("=" * 50)
    print("TESTING TXT PARSER")
    print("=" * 50)

    doc = parse_document(
        file_path="samples/input/sample.txt",
        file_id="test_001",
        file_extension=".txt"
    )

    print(f"\nFilename: {doc.filename}")
    print(f"Type: {doc.file_type}")
    print(f"Pages: {doc.total_pages}")
    print(f"Words: {doc.total_words}")
    print(f"Characters: {doc.total_characters}")
    print(f"Sections: {len(doc.sections)}")
    print(f"Tables: {len(doc.tables)}")

    print("\n--- Sections Found ---")
    for i, section in enumerate(doc.sections):
        print(f"\n  Section {i+1}: {section.title}")
        print(f"  Content preview: {section.content[:100]}...")

    print("\n--- Summary ---")
    print(doc.summary())

    # Test structure analyzer
    from src.parsers.structure_analyzer import analyze_structure
    analysis = analyze_structure(doc)
    print("\n--- Structure Analysis ---")
    for key, value in analysis.items():
        print(f"  {key}: {value}")

    print("\n✅ TXT Parser test PASSED!")


if __name__ == "__main__":
    test_txt()
