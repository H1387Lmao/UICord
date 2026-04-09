# UICord
[![Python](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FH1387Lmao%2FUICord%2Frefs%2Fheads%2Fmaster%2Fpyproject.toml&query=project.requires-python&label=python&logo=python&logoColor=white)](https://python.org)
[![Documentation](https://img.shields.io/badge/view-Documentation-red?style=for-the-badge)](https://uicord.readthedocs.io/en/latest)

A UI helper library for [pycord](https://github.com/Pycord-Development/pycord) that makes Discord's Components V2 simple to work with.

> [!CAUTION]
> This project is a work in progress. Contributions are very welcome!

---

## Features

- Clean wrappers around every Components V2 primitive (Button, Select, Container, Section, MediaGallery, …)
- `View` and `Modal` subclasses with built-in owner-checking and auto-reload
- `@interaction` decorator with automatic error reporting to developers
- `UIString` - a `str` subclass with pluggable i18n via `state.translator_function`
- `lang=` keyword on `View` and `Modal` for per-instance translations
- Graceful pycord 2.7 / 2.8 compatibility shims (`MediaGalleryItem`, `Checkbox`, `CheckboxGroup`)

---

## Installation

```bash
pip install git+https://github.com/H1387Lmao/UICord
```

Requires **pycord ≥ 2.7**.

For `Checkbox` / `CheckboxGroup` support, use **pycord ≥ 2.8**.

---

## Quick Start

```python
import discord
from discord.ext import commands
import uicord

bot = commands.Bot(command_prefix="!")

@bot.slash_command()
async def demo(ctx):
    view = uicord.View(owner=ctx.author.id)
    btn  = uicord.Button("Click me!", color=uicord.Colors.Blue)
    view.add(btn)

    @uicord.interaction(component=btn)
    async def on_click(ictx):
        await ictx.respond("You clicked it!", ephemeral=True)

    await ctx.respond("Here you go:", view=view)

bot.run("TOKEN")
```

---

## Internationalisation / Localisation

```python
from uicord import state, UIString, View

# Plug in any translation backend
state.translator_function = lambda text, lang: my_i18n(text, lang)

# Translate at construction time
greeting = UIString("hello.world", lang="fr")

# Or let the View handle it - view._("key") returns a UIString in view.lang
view = View(lang="ja")
label = view._("btn.confirm")   # → translated to Japanese
```

---

## Components at a Glance

| Class | Description |
|---|---|
| `View` | Main component container with owner-check and reload |
| `Modal` | Input/output modal with label helpers |
| `Button` | Interactable button |
| `Toggle` | Stateful on/off button |
| `ButtonChoices` | Radio-style button group |
| `Choices` | Select / drop-down menu |
| `ActionRow` | Manual row layout |
| `Container` | Component container |
| `Section` | Section block *(pycord ≥ 2.7)* |
| `Separator` | Visual divider |
| `Thumbnail` | Inline thumbnail |
| `MediaGallery` | Media gallery block *(pycord ≥ 2.7)* |
| `MediaGalleryItem` | Item inside a MediaGallery *(pycord ≥ 2.7)* |
| `Text` | Text display |
| `Checkbox` | Single checkbox *(pycord ≥ 2.8)* |
| `CheckboxGroup` | Group of checkboxes *(pycord ≥ 2.8)* |
| `UIString` | Translatable string subclass |

Full API reference → [uicord.readthedocs.io](https://uicord.readthedocs.io/en/latest)

---

## Contributing

This project genuinely needs contributors. Bug reports, feature requests, and pull requests are all appreciated.

---

*Originally made for you and the community by H1387Lmao ♥ - open-source, no license. Please keep it that way.*
