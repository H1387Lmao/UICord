"""
components/text.py
------------------
:class:`Text` - a simple text display for Views and Modals.
"""
from __future__ import annotations

import discord.ui as ui


class Text(ui.TextDisplay):
    """
    Text display for a :class:`~uicord.View` or
    :class:`~uicord.Modal`.

    Parameters
    ----------
    text:
        The string (or :class:`~uicord.UIString`) to display.
    """

    def __init__(self, text: str = "myText"):
        super().__init__(text)
