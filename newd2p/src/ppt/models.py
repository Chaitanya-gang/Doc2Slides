"""
newd2p - PPT Data Models
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SlideData:
    slide_number: int
    slide_type: str
    title: str
    bullet_points: List[str] = field(default_factory=list)
    speaker_notes: str = ""
    visual_cue: str = ""
    duration_seconds: int = 45
    chart_path: Optional[str] = None


@dataclass
class PresentationData:
    title: str
    subtitle: str
    slides: List[SlideData] = field(default_factory=list)
    style: str = "ted_talk"
    total_duration: int = 0

    def calculate_duration(self):
        self.total_duration = sum(s.duration_seconds for s in self.slides)
