"""
newd2p - Token Counting
"""


def count_tokens(text: str) -> int:
    return len(text) // 4


def truncate_to_tokens(text: str, max_tokens: int) -> str:
    max_chars = max_tokens * 4
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."
