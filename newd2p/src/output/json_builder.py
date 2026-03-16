"""
newd2p - JSON Builder for Video Team Handover
"""

import json
from datetime import datetime
from pathlib import Path
from src.utils.logger import get_logger

logger = get_logger("json_builder")


def build_handover_json(
    narrative_json: str,
    doc_summary: str,
    file_id: str,
    filename: str,
    output_path: str,
    chart_paths: list = None,
) -> str:
    try:
        narrative = json.loads(narrative_json)
    except:
        narrative = {"title": "Presentation", "slides": []}

    try:
        summary = json.loads(doc_summary)
    except:
        summary = {"main_theme": "", "key_topics": []}

    handover = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "generator": "newd2p AI",
            "version": "0.1.0",
            "source_file": filename,
            "file_id": file_id,
        },
        "document_analysis": {
            "main_theme": summary.get("main_theme", ""),
            "key_topics": summary.get("key_topics", []),
            "data_points": summary.get("data_points", []),
            "conclusion": summary.get("conclusion", ""),
        },
        "presentation": {
            "title": narrative.get("title", ""),
            "subtitle": narrative.get("subtitle", ""),
            "total_slides": len(narrative.get("slides", [])),
            "total_duration_seconds": sum(
                s.get("duration_seconds", 45) for s in narrative.get("slides", [])
            ),
        },
        "slides": [],
        "charts": [],
    }

    for slide in narrative.get("slides", []):
        slide_data = {
            "slide_number": slide.get("slide_number", 0),
            "slide_type": slide.get("slide_type", "content"),
            "title": slide.get("title", ""),
            "bullet_points": slide.get("bullet_points", []),
            "speaker_notes": slide.get("speaker_notes", ""),
            "visual_cue": slide.get("visual_cue", ""),
            "duration_seconds": slide.get("duration_seconds", 45),
        }
        handover["slides"].append(slide_data)

    if chart_paths:
        for cp in chart_paths:
            handover["charts"].append({
                "title": cp.get("title", ""),
                "path": cp.get("path", ""),
                "type": cp.get("data", {}).get("chart_type", "bar"),
            })

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(handover, f, indent=2, ensure_ascii=False)

    logger.info(f"Handover JSON saved: {output_path}")
    return output_path
