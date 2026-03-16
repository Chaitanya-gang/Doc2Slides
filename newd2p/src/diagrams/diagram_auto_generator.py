"""
newd2p - Automatic Diagram Generator using Graphviz
"""

import json
from pathlib import Path
from typing import List, Dict

from src.llm.provider_factory import get_llm_provider
from src.llm.prompt_templates import DIAGRAM_ANALYSIS_PROMPT, SYSTEM_PROMPT
from src.diagrams.diagram_generator import create_flow_diagram
from src.utils.logger import get_logger


logger = get_logger("diagram_auto_generator")


def analyze_text_for_diagrams(text: str) -> List[Dict]:
    """
    Use the LLM to detect workflows / processes and return structured diagram specs.
    """
    try:
        llm = get_llm_provider()
        prompt = DIAGRAM_ANALYSIS_PROMPT.format(content=text)
        response = llm.generate(prompt, system_prompt=SYSTEM_PROMPT)

        start = response.find("{")
        end = response.rfind("}") + 1
        if start != -1 and end > start:
            data = json.loads(response[start:end])
            diagrams = data.get("diagrams", [])

            valid_diagrams: List[Dict] = []
            for diag in diagrams:
                steps = diag.get("steps", [])
                if isinstance(steps, list) and 2 <= len(steps) <= 8:
                    clean_steps = [str(s).strip() for s in steps if str(s).strip()]
                    if len(clean_steps) >= 2:
                        diag["steps"] = clean_steps
                        title = diag.get("title") or "Process Flow"
                        diag["title"] = str(title).strip()
                        valid_diagrams.append(diag)

            logger.info(f"Found {len(valid_diagrams)} valid diagrams")
            return valid_diagrams
    except Exception as e:
        logger.error(f"Diagram analysis failed: {e}")
    return []


def generate_all_diagrams(text: str, output_dir: str) -> List[Dict]:
    """
    Analyze text and generate diagram PNGs for each detected flow.
    Returns a list of dicts with path + metadata, suitable for PPTBuilder.
    """
    diagrams_data = analyze_text_for_diagrams(text)
    diagram_paths: List[Dict] = []

    for i, diag in enumerate(diagrams_data):
        title = diag.get("title", f"Diagram {i + 1}")
        steps = diag.get("steps", [])
        output_base = Path(output_dir) / f"diagram_{i}"
        img_path = create_flow_diagram(
            title=title,
            stages=steps,
            output_path=str(output_base),
        )
        if img_path:
            diagram_paths.append(
                {
                    "path": img_path,
                    "title": title,
                    "data": diag,
                }
            )

    logger.info(f"Generated {len(diagram_paths)} diagrams")
    return diagram_paths

