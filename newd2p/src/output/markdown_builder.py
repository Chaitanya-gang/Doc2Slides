"""
newd2p - Markdown Export Builder
"""

import json
from pathlib import Path

from src.utils.logger import get_logger


logger = get_logger("markdown_builder")


def build_markdown_from_narrative(narrative_json: str, output_path: str) -> str:
    try:
        data = json.loads(narrative_json)
    except Exception:
        data = {"title": "Presentation", "subtitle": "", "slides": []}

    lines = []

    title = data.get("title", "Presentation")
    subtitle = data.get("subtitle", "")

    lines.append(f"# {title}")
    if subtitle:
        lines.append(f"_{subtitle}_")
    lines.append("")

    for slide in data.get("slides", []):
        slide_number = slide.get("slide_number", 0)
        slide_title = slide.get("title", "")
        slide_type = slide.get("slide_type", "content")
        bullets = slide.get("bullet_points", [])
        notes = slide.get("speaker_notes", "")

        heading_prefix = "##" if slide_type != "title" else "##"
        lines.append(f"{heading_prefix} {slide_number}. {slide_title}")
        lines.append("")

        for b in bullets:
            lines.append(f"- {b}")

        if notes:
            lines.append("")
            lines.append("> " + notes.replace("\n", "\n> "))

        lines.append("")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    logger.info(f"Markdown export saved: {output_path}")
    return output_path

