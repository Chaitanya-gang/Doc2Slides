"""
newd2p - PPT Theme Manager
"""

from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN


THEMES = {
    "professional": {
        "bg_color": RGBColor(255, 255, 255),
        "title_color": RGBColor(27, 54, 93),
        "text_color": RGBColor(51, 51, 51),
        "accent_color": RGBColor(74, 144, 217),
        "title_font": "Calibri",
        "body_font": "Calibri",
        "title_size": Pt(36),
        "body_size": Pt(18),
        "bullet_size": Pt(16),
    },
    "creative": {
        "bg_color": RGBColor(255, 255, 255),
        "title_color": RGBColor(108, 52, 131),
        "text_color": RGBColor(44, 62, 80),
        "accent_color": RGBColor(231, 76, 60),
        "title_font": "Georgia",
        "body_font": "Arial",
        "title_size": Pt(40),
        "body_size": Pt(18),
        "bullet_size": Pt(16),
    },
    "dark": {
        "bg_color": RGBColor(26, 26, 46),
        "title_color": RGBColor(232, 232, 232),
        "text_color": RGBColor(200, 200, 200),
        "accent_color": RGBColor(187, 134, 252),
        "title_font": "Arial",
        "body_font": "Arial",
        "title_size": Pt(36),
        "body_size": Pt(18),
        "bullet_size": Pt(16),
    },
    "minimal": {
        "bg_color": RGBColor(255, 255, 255),
        "title_color": RGBColor(44, 62, 80),
        "text_color": RGBColor(44, 62, 80),
        "accent_color": RGBColor(26, 188, 156),
        "title_font": "Helvetica",
        "body_font": "Helvetica",
        "title_size": Pt(32),
        "body_size": Pt(16),
        "bullet_size": Pt(14),
    },
}


def get_theme(theme_name: str = "professional") -> dict:
    return THEMES.get(theme_name, THEMES["professional"])
