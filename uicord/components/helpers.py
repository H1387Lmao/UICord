"""
components/helpers.py
---------------------
Small utilities shared across the library.
"""
from __future__ import annotations


async def EMPTY_CALLBACK(*args, **kwargs):
    """No-op async callback used as a safe default."""
    return 0


def format_values(values: list[str]) -> list:
    """
    Coerce a list of raw string values coming from Discord interactions.

    * Digit-only strings are cast to ``int``.
    * Empty strings become ``None``.
    """
    result = []
    for raw in values:
        if raw.isdigit():
            raw = int(raw)
        raw = raw or None
        result.append(raw)
    return result
