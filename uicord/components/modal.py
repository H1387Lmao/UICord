"""
components/modal.py
-------------------
:class:`Modal` - the main input/output container for Discord modals.
"""
from __future__ import annotations

import discord
import discord.ui as ui
from discord import enums
from uicord.lang.uistring import UIString
from .core import *

class Modal(ui.DesignerModal, UIMember):
    """
    The main input/output system for modal interactions.

    Parameters
    ----------
    title:
        Title displayed at the top of the modal.
    lang:
        Default language passed to :class:`UIString` when resolving
        translated labels inside this modal.
    """

    def __init__(self, title: str = "Modal Title", lang: str | None = None):
        super().__init__(title=title)
        self.inputs: list = []
        self.lang = lang

    # ------------------------------------------------------------------
    # UIString helper
    # ------------------------------------------------------------------

    def _(self, text: str) -> UIString:
        """Translate *text* using this modal's language."""
        return UIString(text, lang=self.lang)

    # ------------------------------------------------------------------
    # Adding inputs
    # ------------------------------------------------------------------

    def add_input(
        self,
        label:       str        = "input label",
        style:       str        = "short",
        placeholder: str | None = None,
        default:     str | None = None,
        required:    bool       = True,
    ) -> ui.InputText:
        """
        Add a text-input field to the modal.

        Parameters
        ----------
        label:
            The field's label (supports :class:`UIString`).
        style:
            ``"short"`` for a single-line input, ``"long"`` for paragraph.
        placeholder:
            Ghost text shown when the field is empty.
        default:
            Pre-filled value.
        required:
            Whether the user must fill in this field.

        Returns
        -------
        :class:`discord.ui.InputText`
            The underlying input object (useful for reading ``.value`` later).
        """
        inp_style = (
            enums.InputTextStyle.short
            if style == "short"
            else enums.InputTextStyle.paragraph
        )
        input_text = ui.InputText(
            style=inp_style,
            placeholder=placeholder,
            value=default,
            required=required,
        )
        super().add_item(ui.Label(label=label, item=input_text))
        self.inputs.append(input_text)
        return input_text

    def add_item(
        self,
        label:     str  = "input label",
        item              = None,
        component         = None
    ):
        """
        Add an arbitrary component to the modal wrapped in a :class:`ui.Label`.

        Parameters
        ----------
        label:
            The label shown above the component.
        item / component:
            The component to add (either keyword works).
        required:
            Whether the user requires a item to fill in
        Returns
        -------
        The component that was added.
        """
        input_text = item or component
        super().add_item(ui.Label(label=label, item=input_text))
        self.inputs.append(input_text)
        return input_text

    # ------------------------------------------------------------------
    # Callback
    # ------------------------------------------------------------------

    async def callback(self, ctx: discord.Interaction) -> None:
        """Called when the modal is submitted.  Override in subclasses."""
        pass

    # ------------------------------------------------------------------
    # Value helpers
    # ------------------------------------------------------------------

    @property
    def values(self) -> list:
        """All input values in order (``None`` for inputs without a value)."""
        return [
            a.value  if hasattr(a, "value")
            else a.values if hasattr(a, "values")
            else None
            for a in self.inputs
        ]

    async def get_value(self, index: int = 0):
        """
        Return the value of the text input at *index*.

        Parameters
        ----------
        index:
            Zero-based position of the input that was added.
        """
        return self.inputs[index].value
