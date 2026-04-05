"""
components/compat.py
--------------------
Runtime compatibility shims for pycord 2.7 and 2.8 features.

Pycord 2.7 additions
~~~~~~~~~~~~~~~~~~~~
* ``discord.MediaGalleryItem``  - exposed in layout.py
* ``discord.ui.role_select``    - decorator helper exposed here

Pycord 2.8 additions
~~~~~~~~~~~~~~~~~~~~
* ``discord.ui.Checkbox``
* ``discord.ui.CheckboxGroup``

When the installed version does not support these objects, placeholder
classes are provided that raise :class:`NotImplementedError` with a
helpful message, so the rest of the library still imports cleanly.
"""
from __future__ import annotations

import discord
import discord.ui as ui

# ---------------------------------------------------------------------------
# Pycord 2.7 - role_select (and other typed selects)
# ---------------------------------------------------------------------------

if hasattr(ui, "role_select"):
    role_select = ui.role_select
else:
    def role_select(*args, **kwargs):  # type: ignore[misc]
        raise NotImplementedError("role_select requires pycord ≥ 2.7")


# ---------------------------------------------------------------------------
# Pycord 2.8 - Checkbox / CheckboxGroup
# ---------------------------------------------------------------------------

def _make_stub(name: str, version: str):
    """Return a placeholder class that raises NotImplementedError."""
    class _Stub:
        def __init__(self, *a, **kw):
            raise NotImplementedError(
                f"{name} requires pycord ≥ {version}. "
                "Install it with: pip install py-cord>=2.8"
            )
        def __init_subclass__(cls, **kw):
            pass
    _Stub.__name__     = name
    _Stub.__qualname__ = name
    return _Stub


if hasattr(ui, "Checkbox"):
    class Checkbox(ui.Checkbox):  # type: ignore[misc]
        """
        A Discord checkbox component (pycord ≥ 2.8).

        Parameters
        ----------
        custom_id:
            The interaction ID for this checkbox.
        default:
            Whether the checkbox is checked by default.
        id:
            The component's numeric ID.
        label:
            Human-readable label (library convenience - wraps in a
            :class:`discord.ui.Label` automatically when added to a modal).
        """
        def __init__(
            self,
            *,
            custom_id: str | None  = None,
            default:   bool        = False,
            id:        int | None  = None,
            label:     str | None  = None,
        ):
            super().__init__(custom_id=custom_id, default=default, id=id)
            self._label = label

        @property
        def label(self) -> str | None:
            return self._label

        @property
        def checked(self) -> bool | None:
            """Whether the user checked this box (available after submission)."""
            return self.value

else:
    Checkbox = _make_stub("Checkbox", "2.8")  # type: ignore[assignment,misc]


if hasattr(ui, "CheckboxGroup"):
    class CheckboxGroup(ui.CheckboxGroup):  # type: ignore[misc]
        """
        A group of Discord checkboxes (pycord ≥ 2.8).

        Parameters
        ----------
        *checkboxes:
            :class:`Checkbox` instances to include.
        custom_id:
            Interaction ID for the group.
        required:
            Whether at least one checkbox must be selected.
        min_values / max_values:
            Selection count constraints (0-10 / 1-10).
        """
        def __init__(
            self,
            *checkboxes,
            custom_id:  str | None = None,
            required:   bool       = True,
            min_values: int        = 0,
            max_values: int        = 1,
        ):
            super().__init__(
                *checkboxes,
                custom_id=custom_id,
                required=required,
                min_values=min_values,
                max_values=max_values,
            )

        @property
        def checked_values(self) -> list[bool] | None:
            """List of selected states after submission."""
            return self.values

else:
    CheckboxGroup = _make_stub("CheckboxGroup", "2.8")  # type: ignore[assignment,misc]


__all__ = [
    "role_select",
    "Checkbox",
    "CheckboxGroup",
]
