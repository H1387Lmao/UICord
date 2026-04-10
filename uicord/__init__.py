"""
uicord
==========
A friendly wrapper around pycord's UI component system.

Quick start
-----------
::

    from uicord import View, Button, Modal, UIString, state

    # Optional: hook in your i18n backend
    state.translator_function = lambda text, lang: my_translate(text, lang)

    view = View(lang="en")
    btn  = Button("click_me_key")   # use UIString for auto-translation

Module layout
-------------
uicord/
├── state.py                  ← global mutable state (DEV_IDS, translator_function)
├── lang/
│   ├── __init__.py
│   └── uistring.py           ← UIString (str subclass with translation)
└── components/
    ├── __init__.py
    ├── colors.py             ← Colors constants
    ├── helpers.py            ← EMPTY_CALLBACK, format_values
    ├── text.py               ← Text display
    ├── buttons.py            ← Button, Toggle
    ├── choices.py            ← Choices (select), RadioButtons RadioButtonOption (radio btns)
    ├── layout.py             ← ActionRow, Container, Separator, Section,
    │                            Thumbnail, MediaGallery, MediaGalleryItem
    ├── view.py               ← View, interaction() decorator
    ├── modal.py              ← Modal
    └── compat.py             ← pycord 2.7/2.8 shims
                                 (role_select, Checkbox, CheckboxGroup)

Pycord version compatibility
-----------------------------
* **2.6**  - core components (View, Modal, Button, etc.)
* **2.7**  - MediaGalleryItem, role_select, Section, MediaGallery, …
* **2.8**  - Checkbox, CheckboxGroup (gracefully stubbed on older versions)
"""

# ── State (always first so other modules can import it safely) ──────────────
from uicord.state import state

# ── Language / i18n ─────────────────────────────────────────────────────────
from uicord.lang.uistring import UIString

# ── Components ───────────────────────────────────────────────────────────────
from uicord.components import (
    # Utilities
    Colors,
    EMPTY_CALLBACK,
    format_values,
    # Basic display
    Text,
    # Buttons
    Button,
    Toggle,
    # Select / radio
    Choices,
    Choice,
    RadioButtons,
    RadioButtonOption,
    # Layout
    ActionRow,
    Container,
    Separator,
    Section,
    Thumbnail,
    MediaGallery,
    MediaGalleryItem,
    # View / Modal
    View,
    interaction,
    Modal,
    # Pycord 2.7+
    role_select,
    # Pycord 2.8+  (NotImplementedError if not installed)
    Checkbox,
    CheckboxGroup,
)

__all__ = [
    # State
    "state",
    # i18n
    "UIString",
    # Utilities
    "Colors",
    "EMPTY_CALLBACK",
    "format_values",
    # Display
    "Text",
    # Buttons
    "Button",
    "Toggle",
    # Select / radio
    "Choices",
    "Choice",
    "RadioButtons",
    "RadioButtonOption",
    # Layout
    "ActionRow",
    "Container",
    "Separator",
    "Section",
    "Thumbnail",
    "MediaGallery",
    "MediaGalleryItem",
    # View / Modal
    "View",
    "interaction",
    "Modal",
    # Pycord 2.7+
    "role_select",
    # Pycord 2.8+
    "Checkbox",
    "CheckboxGroup",
]
