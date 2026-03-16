"""
Lightweight local presentation generation helpers.
"""

import json
import re
from collections import Counter
from pathlib import Path
from typing import List

from src.parsers.models import ParsedDocument


STOP_WORDS = {
    "the", "and", "for", "that", "with", "this", "from", "into", "have", "has",
    "are", "was", "were", "will", "shall", "would", "could", "should", "about",
    "their", "there", "them", "then", "than", "been", "being", "also", "such",
    "your", "our", "but", "not", "can", "may", "using", "used", "use", "each",
    "through", "within", "between", "where", "when", "what", "which", "while",
    "document", "presentation", "slide",
}

PROJECT_KEYWORDS = {
    "fastapi", "streamlit", "ollama", "llama", "rag", "faiss", "embedding",
    "vector", "chunking", "parser", "python-pptx", "ppt", "presentation",
    "retrieval", "generation", "api", "backend", "frontend",
}


def _normalize_title(filename: str) -> str:
    stem = Path(filename).stem
    stem = re.sub(r"^\d{8}_\d{6}_", "", stem)
    stem = stem.replace("_", " ").replace("-", " ").strip()
    return stem.title() or "Presentation"


def _split_sentences(text: str) -> List[str]:
    raw_parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    sentences = []
    for part in raw_parts:
        cleaned = " ".join(part.split()).strip(" -•\t")
        if len(cleaned) >= 20:
            sentences.append(cleaned)
    return sentences


def _top_keywords(text: str, limit: int = 5) -> List[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9\-]{2,}", text.lower())
    filtered = [word for word in words if word not in STOP_WORDS]
    counts = Counter(filtered)
    return [word.title() for word, _ in counts.most_common(limit)]


def _contains_project_markers(text: str) -> bool:
    lowered = text.lower()
    hits = sum(1 for keyword in PROJECT_KEYWORDS if keyword in lowered)
    return hits >= 3


def _extract_matching_sentences(text: str, keywords: List[str], limit: int = 4) -> List[str]:
    sentences = _split_sentences(text)
    matches = []
    for sentence in sentences:
        lowered = sentence.lower()
        if any(keyword in lowered for keyword in keywords):
            matches.append(sentence)
        if len(matches) >= limit:
            break
    return matches


def _compact_points(sentences: List[str], fallback: List[str]) -> List[str]:
    points = []
    for sentence in sentences:
        cleaned = sentence.strip()
        if cleaned and cleaned not in points:
            points.append(cleaned[:140])
        if len(points) >= 4:
            break
    return points or fallback


def _section_blocks(doc: ParsedDocument) -> List[dict]:
    blocks = []
    for section in doc.sections:
        content = section.content.strip()
        title = section.title.strip()
        if title or content:
            blocks.append(
                {
                    "title": title or "Key Topic",
                    "content": content,
                }
            )

    if blocks:
        return blocks

    paragraphs = [p.strip() for p in doc.cleaned_text.split("\n\n") if p.strip()]
    for index, paragraph in enumerate(paragraphs[:12], start=1):
        blocks.append({"title": f"Topic {index}", "content": paragraph})
    return blocks


def build_simple_summary(doc: ParsedDocument) -> str:
    text = doc.cleaned_text[:8000]
    keywords = _top_keywords(text)
    sentences = _split_sentences(text)
    summary = {
        "main_theme": _normalize_title(doc.filename),
        "key_topics": keywords,
        "data_points": [],
        "conclusion": sentences[-1] if sentences else "",
    }
    return json.dumps(summary, ensure_ascii=False)


def _build_project_narrative(doc: ParsedDocument, slide_count: int, style: str) -> str:
    text = doc.cleaned_text
    title = _normalize_title(doc.filename)
    keywords = _top_keywords(text, limit=6)
    section_titles = [section.title for section in doc.sections if section.title.strip()]

    slide_specs = [
        ("Problem Statement", ["problem", "challenge", "manual", "time consuming"], [
            "Manual PPT creation is slow",
            "Large documents take time",
            "Important points may be missed",
            "Automation is needed",
        ]),
        ("Objective", ["objective", "aim", "goal", "system"], [
            "Convert documents into PPT",
            "Reduce manual summarization",
            "Improve presentation speed",
            "Keep slide flow structured",
        ]),
        ("System Architecture", ["architecture", "streamlit", "fastapi", "backend", "frontend"], [
            "Streamlit user interface",
            "FastAPI backend processing",
            "Parser and AI pipeline",
            "PPT generation module",
        ]),
        ("Workflow / Methodology", ["workflow", "upload", "parse", "chunk", "retrieve"], [
            "Upload input document",
            "Extract and clean text",
            "Generate structured slides",
            "Export final PPT",
        ]),
        ("Tech Stack", ["fastapi", "streamlit", "faiss", "ollama", "python"], [
            "FastAPI backend services",
            "Streamlit demo interface",
            "Ollama local LLM",
            "python-pptx slide creation",
        ]),
        ("AI Pipeline", ["rag", "embedding", "vector", "faiss", "ollama", "llm"], [
            "Chunking for long documents",
            "Embeddings for retrieval",
            "FAISS vector search",
            "LLM-based slide drafting",
        ]),
        ("Code Modules", ["api", "parser", "ppt", "llm", "rag", "module"], [
            "API route handlers",
            "Document parsers",
            "LLM and RAG modules",
            "PPT builder components",
        ]),
        ("Results / Output", ["output", "result", "ppt", "presentation"], [
            "Generated PPTX output",
            "Structured slide flow",
            "Downloadable presentation file",
            "Narrative speaker notes",
        ]),
        ("Limitations", ["limitation", "resource", "time", "memory"], [
            "Large files take longer",
            "Local models need memory",
            "Design customization is limited",
            "AI output may vary",
        ]),
        ("Future Scope", ["future", "scope", "improvement", "deploy"], [
            "Better slide design",
            "Image and diagram automation",
            "Multi-model support",
            "Cloud deployment options",
        ]),
    ]

    content_slots = max(1, slide_count - 2)
    chosen_specs = slide_specs[:content_slots]
    slides = [{
        "slide_number": 1,
        "slide_type": "title",
        "title": title,
        "subtitle": f"Project explanation in {style.replace('_', ' ')} style",
        "bullet_points": [],
        "speaker_notes": f"This presentation explains the project workflow and implementation of {title}.",
        "visual_cue": "Clean architecture overview with system modules",
        "duration_seconds": 30,
    }]

    for index, (slide_title, search_terms, fallback) in enumerate(chosen_specs, start=2):
        matches = _extract_matching_sentences(text, search_terms, limit=4)
        if slide_title == "Code Modules" and section_titles:
            matches = section_titles[:4]
        if slide_title in {"Results / Output", "Limitations", "Future Scope"} and keywords:
            matches = matches or keywords[:4]

        bullet_points = _compact_points(matches, fallback)
        slides.append(
            {
                "slide_number": index,
                "slide_type": "content",
                "title": slide_title,
                "bullet_points": bullet_points,
                "speaker_notes": " ".join(bullet_points[:2]),
                "visual_cue": f"Diagram or layout for {slide_title.lower()}",
                "duration_seconds": 45,
                "style": style,
            }
        )

    slides.append(
        {
            "slide_number": len(slides) + 1,
            "slide_type": "closing",
            "title": "Conclusion",
            "bullet_points": keywords[:4] or ["AI-powered automation", "Structured slide output"],
            "speaker_notes": "End by summarizing how the project automates document-to-presentation generation.",
            "visual_cue": "Closing summary with project highlights",
            "duration_seconds": 30,
        }
    )

    narrative = {
        "title": title,
        "subtitle": "AI powered document to presentation system",
        "slides": slides,
    }
    return json.dumps(narrative, ensure_ascii=False)


def build_simple_narrative(doc: ParsedDocument, slide_count: int = 8, style: str = "ted_talk") -> str:
    if _contains_project_markers(doc.cleaned_text):
        return _build_project_narrative(doc, slide_count, style)

    title = _normalize_title(doc.filename)
    blocks = _section_blocks(doc)
    max_content_slides = max(1, slide_count - 2)
    selected_blocks = blocks[:max_content_slides]
    slides = []

    slides.append(
        {
            "slide_number": 1,
            "slide_type": "title",
            "title": title,
            "subtitle": f"Generated from {doc.filename}",
            "bullet_points": [],
            "speaker_notes": f"This presentation summarizes {doc.filename}.",
            "visual_cue": "",
            "duration_seconds": 30,
        }
    )

    for index, block in enumerate(selected_blocks, start=2):
        sentences = _split_sentences(block["content"])
        bullets = sentences[:4]
        if not bullets and block["content"]:
            bullets = [block["content"][:140]]
        if not bullets:
            bullets = ["Key information extracted from the document."]

        slides.append(
            {
                "slide_number": index,
                "slide_type": "content",
                "title": block["title"][:80],
                "bullet_points": bullets,
                "speaker_notes": " ".join(bullets[:2]),
                "visual_cue": "",
                "duration_seconds": 45,
                "style": style,
            }
        )

    keywords = _top_keywords(doc.cleaned_text)
    slides.append(
        {
            "slide_number": len(slides) + 1,
            "slide_type": "closing",
            "title": "Conclusion",
            "bullet_points": keywords[:4] or ["Summary complete"],
            "speaker_notes": "Close by reinforcing the main takeaway from the document.",
            "visual_cue": "",
            "duration_seconds": 30,
        }
    )

    narrative = {
        "title": title,
        "subtitle": f"Simple {style.replace('_', ' ')} presentation",
        "slides": slides,
    }
    return json.dumps(narrative, ensure_ascii=False)
