"""
components/view.py
------------------
:class:`View` and the :func:`interaction` decorator.
"""
from __future__ import annotations

import inspect
import traceback

import discord
import discord.ui as ui

from uicord.state import state
from uicord.lang.uistring import UIString


class View(ui.DesignerView):
    """
    The main container for every component.

    Parameters
    ----------
    *items:
        Components to add at construction time.
    owner:
        User ID that is allowed to interact with this view.
        When *None* anyone may use it.
    lang:
        Default language passed to :class:`UIString` when resolving
        translated labels inside this view.
    """

    def __init__(self, *items, owner: int | None = None, lang: str | None = None):
        super().__init__(*items, timeout=None)
        self.owner = owner
        self.lang  = lang

    # ------------------------------------------------------------------
    # UIString helper
    # ------------------------------------------------------------------

    def _(self, text: str) -> UIString:
        """Translate *text* using this view's language."""
        return UIString(text, lang=self.lang)

    # ------------------------------------------------------------------
    # Discord overrides
    # ------------------------------------------------------------------

    async def interaction_check(self, ctx: discord.Interaction) -> bool:
        if self.owner is None:
            return True
        if self.owner != ctx.user.id:
            await ctx.response.send_message(
                self._("This is not yours!"),
                ephemeral=True,
            )
            return False
        return True

    def add(self, component):
        """
        Add *component* to the view and return it (fluent helper).

        :param component: The component to be added.
        :return: The component that was added.
        """
        self.add_item(component)
        return component

    async def reload(self, ctx: discord.Interaction) -> None:
        """
        Reload the current view, updating every unsynced component.

        Silently defers if the interaction has already been responded to.
        """
        try:
            await ctx.response.defer()
        except discord.errors.InteractionResponded:
            await ctx.edit_original_response(view=self)


# ---------------------------------------------------------------------------
# interaction() decorator
# ---------------------------------------------------------------------------

def interaction(component=None):
    """
    Decorator that assigns an async callback to *component*.

    Any exception raised inside the callback is:

    * Pretty-printed to stdout.
    * DMed to every user ID in :data:`state.DEV_IDS`.
    * Reported to the interacting user with an ephemeral error message.

    Usage::

        btn = Button("Click me")

        @interaction(btn)
        async def on_click(ctx):
            await ctx.respond("clicked!")
    """
    def wrapper(func):
        if not component:
            raise TypeError("interaction() needs a component")
        if not inspect.iscoroutinefunction(func):
            raise TypeError(
                f"{component.__class__.__name__} callback MUST be asynchronous"
            )

        async def interact(*args):
            ctx = args[0]
            try:
                await func(*args)
            except Exception:
                exc = traceback.format_exc()
                for dev_id in state.DEV_IDS:
                    dev = ctx.client.get_user(dev_id)
                    if dev is None:
                        dev = await ctx.client.fetch_user(dev_id)
                    await dev.send(
                        f"FROM: {ctx.user.mention}\n"
                        f"SERVER: `{ctx.guild.name}`\n"
                        f"COMPONENT: {component.__class__.__name__}\n"
                        f"```\n{exc}\n```"
                    )
                await ctx.respond(
                    f"Error found while interacting with: "
                    f"{component.__class__.__name__}\n"
                    "Already contacted the developer on this issue!",
                    ephemeral=True,
                )
                print(f"\033[91m{exc}\033[0m")

        # Toggle / Text / ButtonChoices use `.cb`; everything else uses `.callback`
        from uicord.components.buttons import Toggle
        from uicord.components.text    import Text
        from uicord.components.choices import ButtonChoices

        if not isinstance(component, (Toggle, Text, ButtonChoices)):
            component.callback = interact
        else:
            component.cb = interact

    return wrapper
