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

class GridItem:
    """
    Item for a :class:`~uicord.Grid`

    Parameters
    ----------
    text:
        The string (or :class:`~uicord.UIString`) to display.
    emoji:
        Optional emoji to be seen besides the text.
    """

    def __init__(self, text="Hi", emoji=None):
        self.text = text
        self.emoji = emoji

class Grid:
    """
    Grid display for a :class:`~uicord.View`
    
    Parameters
    ----------
    rows:
        The amount of rows in a grid.
    cols:
        The amount of cols in a grid.
    texts:
        The list of :class:`~uicord.GridItem` to display.
    width:
        The maximum width a column can take.
    """

    def __init__(
        self,
        rows: int = 2,
        cols: int | None = None,
        texts: list[GridItem] | None = None,
        width: int = 30
    ):
        self.texts = texts or []
        self.rows  = rows
        self.cols  = cols or (len(self.texts) // rows or 1)
        self.width = width

    def build(self):
        cell_width = self.width // self.cols
        res = ""

        row_cells = []
        emojis = []

        for i, item in enumerate(self.texts):
            text = item.text

            if len(text) > cell_width - 1:
                text = text[:cell_width - 2] + "…"

            padded = text.ljust(cell_width)

            row_cells.append(padded)
            emojis.append(item.emoji or "")

            prefix = " ".join(e for e in emojis if e)
            content = "".join(row_cells)

            if prefix:
                res += f"{prefix} `{content}`\n"
            else:
                res += f"`{content}`\n"
            row_cells = []
            emojis = []

        if row_cells:
            content = "".join(row_cells)
            prefix = " ".join(e for e in emojis if e)

            if prefix:
                res += f"{prefix} `{content}`"
            else:
                res += f"`{content}`"

        return Text(res)
