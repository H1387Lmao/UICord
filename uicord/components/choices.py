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

class RadioButtonOption:
    def __init__(self, label: str, value, default: bool = False, disabled=False):
        self.label = label
        self.value = value
        self.default = default
        self.disabled=disabled


class RadioButtons(ui.ActionRow):
    def __init__(self, *, options: RadioButtonOption=[], custom_on="✔", custom_off="✖"):
        super().__init__()
        self.btns: list[ui.Button] = []
        self.map: dict[str, RadioButtonOption] = {}

        self.custom_on = custom_on
        self.custom_off = custom_off

        self.picked: RadioButtonOption | None = None

        self._has_default=True

        for opt in options:
            if opt.default and opt.disabled:
                opt.default=False
            self.add(opt)

    @property
    def value(self):
        return self.picked.value if self.picked else None

    async def cb(self, ctx):
        await ctx.response.edit_message(view=self.view)

    async def callback(self, ctx):
        pressed = ctx.data["custom_id"]

        if self.picked and pressed == self._id_of(self.picked):
            return await self.cb(ctx)
        else:
            self.picked = self.map.get(pressed)


        for btn in self.btns:
            active = self.picked and btn.custom_id == self._id_of(self.picked)
            btn.active = bool(active)
            btn.emoji = self.custom_on if active else self.custom_off

        await self.cb(ctx)

    def _id_of(self, option: RadioButtonOption) -> str:
        for cid, opt in self.map.items():
            if opt is option:
                return cid
        return ""

    def add(self, option: RadioButtonOption, id: str | None = None):
        cid = id or option.label + "_id"

        button = ui.Button(
            label=option.label,
            emoji=self.custom_on if option.default else self.custom_off,
            disabled=option.disabled
        )

        button.custom_id = cid
        button.callback = self.callback
        button.active = option.default

        self.map[cid] = option
        self.btns.append(button)
        self.add_item(button)

        if option.default:
            self.picked = option
