"""
newd2p - Text Preprocessing
"""

import re


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def remove_headers_footers(text: str) -> str:
    text = re.sub(r'\bPage \d+ of \d+\b', '', text)
    text = re.sub(r'\b\d+\s*\|', '', text)
    return text.strip()


def extract_sentences(text: str) -> list:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]
