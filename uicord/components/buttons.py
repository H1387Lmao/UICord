"""
components/buttons.py
---------------------
:class:`Button` and :class:`Toggle`.
"""
from __future__ import annotations

import discord.ui as ui

from uicord.components.colors  import Colors
from uicord.components.helpers import EMPTY_CALLBACK


class Button(ui.Button):
    """
    An interactable button.

    Parameters
    ----------
    text:
        Label shown on the button.
    label:
        Alias for text.
    emoji:
        Optional emoji displayed alongside the label.
    color:
        One of the :class:`Colors` constants.  Defaults to grey.
    url:
        If provided the button becomes a link-button.
    id:
        Custom ID used to identify the button interaction.
    disabled:
        Whether the button is greyed-out.
    callback:
        Optional coroutine to set as the callback immediately.
    """

    def __init__(
        self,
        text:     str         = "My Button",
        label:    str         = None,
        emoji                 = None,
        color:    int         = Colors.Grey,
        url:      str | None  = None,
        id:       str | None  = None,
        disabled: bool        = False,
        callback              = None,
    ):
        text=text or label
        if text is None and emoji is None:
            text = "\u200b"
        super().__init__(
            label=text,
            custom_id=id,
            style=color,
            url=url,
            disabled=disabled,
        )
        self.emoji = emoji
        if callback:
            self.callback = callback

    # ------------------------------------------------------------------
    # Convenience property so callers can read/write ``btn.color``
    # ------------------------------------------------------------------

    @property
    def color(self) -> int:
        """The style / colour of the button."""
        return self.style

    @color.setter
    def color(self, value: int) -> None:
        self.style = value


class Toggle(Button):
    """
    A stateful toggle button that flips between an on and off emoji.

    Parameters
    ----------
    *args / **kwargs:
        Forwarded to :class:`Button`.
    cb:
        Async callback invoked after the toggle state changes.
    default:
        Initial state - ``True`` = on, ``False`` = off.
    custom_on:
        Emoji shown when the toggle is *on*.  Defaults to ``"✅"``.
    custom_off:
        Emoji shown when the toggle is *off*.  Defaults to ``"❌"``.
    """

    def __init__(
        self,
        *args,
        cb          = EMPTY_CALLBACK,
        default:    bool = True,
        custom_on:  str | None = None,
        custom_off: str | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.active     = default
        self.off_button = custom_off or "❌"
        self.on_button  = custom_on  or "✅"
        self.emoji      = self.on_button if default else self.off_button
        self.cb         = cb

    async def callback(self, ctx) -> None:
        """Flip the toggle state then call the user's callback."""
        if self.active:
            self.emoji = self.off_button
        else:
            self.emoji = self.on_button
        self.active = not self.active
        await self.cb(ctx)
