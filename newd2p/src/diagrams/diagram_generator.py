"""
newd2p - Diagram Generator

Creates simple flow diagrams that can be embedded as slide images.
"""

from pathlib import Path
from typing import Optional, List

from src.utils.logger import get_logger

try:
    from graphviz import Digraph
except Exception:  # pragma: no cover - optional dependency
    Digraph = None  # type: ignore


logger = get_logger("diagram_generator")


def _safe_render(dot: "Digraph", output_path: str) -> Optional[str]:
    try:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        stem = Path(output_path).with_suffix("")
        dot.render(filename=str(stem), format="png", cleanup=True)
        png_path = f"{stem}.png"
        return png_path
    except Exception as e:
        logger.error(f"Diagram render failed: {e}")
        return None


def create_flow_diagram(
    title: str,
    stages: List[str],
    output_path: str,
) -> Optional[str]:
    """
    Create a left-to-right flow diagram for the given stages.
    """
    if Digraph is None:
        logger.warning("graphviz not available, skipping diagram generation")
        return None

    try:
        dot = Digraph(comment=title)
        dot.attr(rankdir="LR", bgcolor="#0f172a")
        dot.attr("node", shape="box", style="filled", color="#1e293b", fontcolor="#e2e8f0")
        dot.attr("edge", color="#38bdf8")

        last_id = None
        for idx, stage in enumerate(stages):
            node_id = f"n{idx}"
            dot.node(node_id, stage)
            if last_id is not None:
                dot.edge(last_id, node_id)
            last_id = node_id

        return _safe_render(dot, output_path)
    except Exception as e:
        logger.error(f"Diagram generation failed: {e}")
        return None

