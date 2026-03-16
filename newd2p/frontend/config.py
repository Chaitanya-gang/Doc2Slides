"""
Frontend configuration and presentation presets.
"""

API_BASE_URL = "http://localhost:8000"
DEFAULT_SLIDE_COUNT = 8
DEFAULT_THEME = "ocean"
DEFAULT_STYLE = "training"

THEME_PRESETS = {
    "Academic": {
        "theme": "forest",
        "style": "training",
        "slides": 9,
        "description": "Structured, explanatory, and viva-friendly.",
    },
    "Business": {
        "theme": "royal",
        "style": "executive_summary",
        "slides": 8,
        "description": "Sharper summaries for formal reviews.",
    },
    "Startup Pitch": {
        "theme": "sunset",
        "style": "pitch_deck",
        "slides": 7,
        "description": "More energetic slides with quick takeaways.",
    },
    "Minimal": {
        "theme": "ocean",
        "style": "ted_talk",
        "slides": 6,
        "description": "Cleaner flow with lighter slide density.",
    },
}

PIPELINE_STEPS = [
    "Uploading document",
    "Preparing slide outline",
    "Generating presentation",
    "Packaging downloads",
]
