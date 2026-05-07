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


## UIL

- Allows users to write UIs using a builtin language.
- Free of hassle using hoisting and multiline lambdas.

Example:

```py
@home(){
    elements = []
    elements.append(
        ActionRow(
            Button(
                text: "Click me",
                    emoji: null,
                    gid: "HelloBTN"
                ),
            Button(
                text: "Dont click me",
                emoji: null,
                gid: "Dont"
            )
        )
    )

    HelloBTN::interact(i) => {
        await i.respond(
            "You clicked me!"
        )
    }

    @async why(i){
        await i.response.edit_message(
            view: other.warning(prof, uid)
        )
    }

    Dont.attach(why)

    -> View(
        elements,
        uid: uid
    )
}
```

### Generated equivalent
```py
def home(prof,uid,page):
  elements=[]
  HelloBTN=Button(text='Click me',emoji=null)
  Dont=Button(text='Dont click me',emoji=null)
  elements.append(ActionRow(HelloBTN,Dont))
  async def lambda_0(i):
    await i.respond('You clicked me!')

  HelloBTN.interact=lambda_0
  async def why(i):
    await i.response.edit_message(view=other.warning(prof,uid))

  Dont.attach(why)
  return View(elements,uid=uid)
```

- UI management using `uil.load_uis`

```py
import uicord.uil as uil
uil.load_uis("./my_uis")

print(uicord.state.uis) # will have every file you have in your ui folder as modules.
```

- Single File UI Testing with `python -m uicord.uil examples/test.uil`

---

## Installation

```bash
pip install uicord
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
    view.add(ActionRow(btn))

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
| `RadioButtons` | Radio-button group |
| `RadioButtonOption` | Option inside "Radio buttons" component|
| `Choices` | Select / drop-down menu |
| `ActionRow` | Manual row layout |
| `Container` | Component container |
| `Section` | Section block *(pycord ≥ 2.7)* |
| `Separator` | Visual divider |
| `Thumbnail` | Inline thumbnail |
| `MediaGallery` | Media gallery block *(pycord ≥ 2.7)* |
| `MediaGalleryItem` | Item inside a MediaGallery *(pycord ≥ 2.7)* |
| `Text` | Text display |
| `GridItem` | Item inside a Grid |
| `Grid` | Grid display |
| `Checkbox` | Single checkbox *(pycord ≥ 2.8)* |
| `CheckboxGroup` | Group of checkboxes *(pycord ≥ 2.8)* |
| `UIString` | Translatable string subclass |

Full API reference → [uicord.readthedocs.io](https://uicord.readthedocs.io/en/latest)

---

## Contributing

This project genuinely needs contributors. Bug reports, feature requests, and pull requests are all appreciated.

---

*Originally made for you and the community by H1387Lmao ♥ - open-source, no license. Please keep it that way.*
