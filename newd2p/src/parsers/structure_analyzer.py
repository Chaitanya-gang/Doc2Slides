"""
newd2p - Document Structure Analyzer
Analyzes parsed document to understand its structure
"""

from src.parsers.models import ParsedDocument
from src.utils.logger import get_logger

logger = get_logger("structure_analyzer")


def analyze_structure(doc: ParsedDocument) -> dict:
    """Analyze document structure and return insights"""

    analysis = {
        "total_words": doc.total_words,
        "total_characters": doc.total_characters,
        "total_pages": doc.total_pages,
        "sections_count": len(doc.sections),
        "tables_count": len(doc.tables),
        "has_tables": doc.has_tables,
        "key_topics": [],
        "complexity": "simple",
        "recommended_slides": 10,
    }

    # Determine complexity
    if doc.total_words > 5000:
        analysis["complexity"] = "complex"
    elif doc.total_words > 2000:
        analysis["complexity"] = "moderate"

    # Recommend slide count based on content
    if doc.total_words < 1000:
        analysis["recommended_slides"] = 6
    elif doc.total_words < 3000:
        analysis["recommended_slides"] = 8
    elif doc.total_words < 5000:
        analysis["recommended_slides"] = 10
    else:
        analysis["recommended_slides"] = 12

    # Extract key topics from section titles
    for section in doc.sections:
        if section.title and section.title != "Main Content":
            analysis["key_topics"].append(section.title)

    logger.info(f"Structure analysis: {analysis['complexity']}, {analysis['recommended_slides']} slides recommended")
    return analysis
