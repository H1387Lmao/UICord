"""
components/layout.py
--------------------
Layout primitives: :class:`ActionRow`, :class:`Container`,
:class:`Separator`, :class:`Section`, :class:`Thumbnail`,
:class:`MediaGallery`, and :class:`MediaGalleryItem`.

MediaGalleryItem and role_select are guarded for pycord ≥ 2.7; the
full ``discord`` namespace is checked at import time so that older
installations still work (they simply won't expose these symbols).
"""
from __future__ import annotations

import discord
import discord.ui as ui
from .view import unpack_items

# ---------------------------------------------------------------------------
# ActionRow
# ---------------------------------------------------------------------------

class ActionRow(ui.ActionRow):
    """
    A regular pycord :class:`discord.ui.ActionRow`.

    Parameters
    ----------
    *args / **kwargs:
        Forwarded to the parent.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*unpack_items(args), **kwargs)

    def add(self, *a, **k):
        """Macro for :meth:`add_item`."""
        self.add_item(*a, **k)


# ---------------------------------------------------------------------------
# Container
# ---------------------------------------------------------------------------

class Container(ui.Container):
    """A regular Discord container component."""

    def __init__(self, *items, **kwargs):
        super().__init__(*unpack_items(items), **kwargs)


# ---------------------------------------------------------------------------
# Separator
# ---------------------------------------------------------------------------

class Separator(ui.Separator):
    """A regular Discord separator component."""

    def __init__(self, *, divider: bool = True):
        super().__init__(divider=divider)


# ---------------------------------------------------------------------------
# Section
# ---------------------------------------------------------------------------

class Section(ui.Section):
    """A regular Discord section component."""

    def __init__(self, *items, **kwargs):
        super().__init__(*unpack_items(items), **kwargs)


# ---------------------------------------------------------------------------
# Thumbnail
# ---------------------------------------------------------------------------

class Thumbnail(ui.Thumbnail):
    """A regular Discord thumbnail component."""

    def __init__(self, url: str):
        super().__init__(url)


# ---------------------------------------------------------------------------
# MediaGallery / MediaGalleryItem  (pycord ≥ 2.7)
# ---------------------------------------------------------------------------

class MediaGallery(ui.MediaGallery):
    """A regular Discord media gallery component."""

    def __init__(self, *items, **kwargs):
        super().__init__(*items, **kwargs)


# MediaGalleryItem lives on `discord` (not `discord.ui`) in pycord 2.7+
if hasattr(discord, "MediaGalleryItem"):
    class MediaGalleryItem(discord.MediaGalleryItem):
        """A regular Discord media gallery item."""

        def __init__(self, *items, **kwargs):
            super().__init__(*items, **kwargs)
else:
    # Stub so imports don't break on older versions
    class MediaGalleryItem:  # type: ignore[no-redef]
        """Placeholder - not available in this pycord version."""

        def __init__(self, *items, **kwargs):
            raise NotImplementedError(
                "MediaGalleryItem requires pycord ≥ 2.7"
            )
