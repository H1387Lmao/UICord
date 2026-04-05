"""
components/choices.py
---------------------
:class:`Choices` (select menus) and :class:`ButtonChoices` (radio-style buttons).
"""
from __future__ import annotations

import discord
import discord.ui as ui
from discord import SelectOption

from uicord.components.colors  import Colors
from uicord.components.helpers import EMPTY_CALLBACK


class Choices(ui.Select):
    """
    A select / drop-down menu.

    Parameters
    ----------
    type:
        ``discord.ComponentType`` for the select kind (string, user, role …).
    placeholder:
        Hint text shown when nothing is selected.
    options:
        Pre-built list of :class:`discord.SelectOption` objects.
    """

    def __init__(
        self,
        type        = discord.ComponentType.string_select,
        placeholder = "Pick",
        options     = [],
    ):
        super().__init__(type, placeholder=placeholder, options=options)
        self.DEFAULTOPTION  = None
        self.component_type = type

    def add(
        self,
        option:      str         = "Option",
        emoji                    = None,
        description: str | None  = None,
        default:     bool        = False,
    ) -> None:
        """
        Add a new select option.

        Parameters
        ----------
        option:
            Displayed label.
        emoji:
            Optional emoji.
        description:
            Sub-text below the label.
        default:
            Whether this option is pre-selected.
        """
        opt = SelectOption(
            label=option,
            emoji=emoji,
            description=description,
            default=default,
            value=option.replace(" ", "-").lower(),
        )
        self.append_option(opt)
        if default:
            self.DEFAULTOPTION = opt

    @property
    def picked(self):
        """The currently selected value, or the default option's value."""
        if not self.values:
            return self.DEFAULTOPTION.value if self.DEFAULTOPTION else None
        return self.values[0]

    async def force(self, index: int) -> None:
        """*DEPRECATED* - no longer functional, kept for API compatibility."""
        return

    async def disable(self, v: bool = True) -> None:
        """Disable (or re-enable) the select and persist the selection."""
        if self.component_type != discord.ComponentType.channel_select:
            selected = self.picked
            if selected:
                for opt in self.options:
                    opt.default = (selected == opt.value)
        self.disabled = v

    async def update(self) -> None:
        """Refresh the select's buffer (re-enables it)."""
        if self.component_type != discord.ComponentType.channel_select:
            await self.disable(False)
        elif self.component_type != discord.ComponentType.user_select:
            await self.disable(False)

    async def callback(self, ctx) -> None:
        """Default callback: update then reload the parent view."""
        await self.update()
        await self.view.reload(ctx)


class ButtonChoices(ui.ActionRow):
    """
    Radio-button group - only one button can be *active* at a time.

    Parameters
    ----------
    *btns:
        Initial :class:`~uicord.Button` objects (optional).
    """

    def __init__(self, *btns):
        super().__init__()
        self.btns        = []
        self.saved_colors = []
        self.picked      = None

    async def cb(self, ctx) -> None:
        """Called after the selection changes.  Override to customise behaviour."""
        await ctx.response.edit_message(view=self.view)

    async def callback(self, ctx) -> None:
        """Internal callback that handles the radio-button logic."""
        pressed = ctx.data["custom_id"]
        for i, btn in enumerate(self.btns):
            if btn.custom_id == pressed:
                if btn.active:
                    btn.style = self.saved_colors[i]
                    self.picked = None
                    btn.active  = False
                else:
                    btn.style = (
                        Colors.Green
                        if self.saved_colors[i] != Colors.Green
                        else Colors.Red
                    )
                    self.picked = btn.label
                    btn.active  = True
            else:
                btn.style  = self.saved_colors[i]
                btn.active = False
        await self.cb(ctx)

    def add(self, button, id: str | None = None):
        """
        Add *button* to the group.

        Parameters
        ----------
        button:
            A :class:`~uicord.Button` instance.
        id:
            Custom ID override; defaults to ``button.label + "_id"``.
        """
        self.btns.append(button)
        button.custom_id  = id or button.label + "_id"
        button.callback   = self.callback
        button.active     = False
        self.add_item(button)
        self.saved_colors.append(button.color)
