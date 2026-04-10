UICord Dev Module
=============

The `uicord.dev` module provides tools for creating and managing development commands within Discord bots using interactive UI panels, modals, and select menus. It simplifies building commands that accept various argument types (strings, integers, files, channels, roles, etc.) via Discord components.

.. note::
   This module is intended for **developer** only commands

Installation
============

.. code-block:: bash

   pip install uicord

Then import the development module:

.. code-block:: python

   import uicord.dev

Quick Start
===========

1. **Register a command** using the ``@register`` decorator.
2. **Create a Panel** with the registered commands.
3. **Show the panel** in response to a Discord interaction.

Example:

.. code-block:: python

   import discord
   from uicord.dev import register, Panel
   from uicord.components import View  # if needed

   @register()
   async def hello(ctx, name: str = "World"):
       await ctx.respond(f"Hello, {name}!")

   @register("echo")
   async def repeat(ctx, message: str):
       await ctx.respond(f"You said: {message}")

   # Inside a command or event
   @bot.slash_command()
   async def dev_panel(ctx: discord.ApplicationContext):
       panel = Panel(state.DEV_CMDS)   # state.DEV_CMDS holds all registered commands
       await panel.show(ctx)

API Reference
=============

.. currentmodule:: uicord.dev

Decorators
----------

.. autofunction:: register

Classes
-------

.. autoclass:: Option
   :members:

.. autoclass:: MultiStr
   :show-inheritance:

.. autoclass:: Panel
   :members: show, run

Helper Types
------------

.. autoclass:: Option
   :members:

Detailed Documentation
======================

register
--------

.. function:: register(name=None)

   Decorator to register a function as a development command.

   :param name: Optional custom name for the command. If not provided, the function's ``__name__`` is used.
   :type name: str, optional

   The decorated function can have parameters with type hints. The panel will automatically generate a modal or selector based on the type annotation.

   **Supported parameter types:**

   * ``str``, ``int`` → short text input
   * ``MultiStr`` → long text input (paragraph)
   * ``discord.File`` → file upload (single)
   * ``bool`` → checkbox
   * ``discord.User`` / ``discord.Member`` → user select menu
   * ``discord.TextChannel`` → channel select menu
   * ``discord.Role`` → role select menu
   * ``Option[list]`` → choice select menu (see `Option` below)

   Example:

   .. code-block:: python

       @register("greet")
       async def greet(ctx, user: discord.User, message: str = "Hi!"):
           await ctx.respond(f"{user.mention}: {message}")

   The command will be stored in ``state.DEV_CMDS`` dictionary.

Option
------

.. class:: Option(options)

   Used to create a choice select menu for a command parameter.

   :param options: List of possible values. Each value will be displayed as a label.
   :type options: list

   Usage in a parameter annotation:

   .. code-block:: python

       from uicord.dev import Option

       @register()
       async def choose(ctx, color: Option["red", "green", "blue"]):
           await ctx.respond(f"You chose {color}")

MultiStr
--------

.. class:: MultiStr

   A marker class that indicates a parameter should be a multi-line text input.

   Example:

   .. code-block:: python

       from uicord.dev import MultiStr

       @register()
       async def feedback(ctx, comment: MultiStr):
           await ctx.respond("Thank you for your feedback!")

Panel
-----

.. class:: Panel(cmds)

   Creates an interactive panel that displays registered commands as buttons.

   :param cmds: Dictionary mapping command names to callables (usually ``state.DEV_CMDS``).
   :type cmds: dict

   The panel organizes buttons into rows (maximum 5 per row). When a button is clicked, a modal is shown to collect arguments based on the command's signature.

   .. method:: show(ctx)

      Sends the panel as an ephemeral message.

      :param ctx: Discord interaction context (must have ``respond`` and ``author`` attributes).
      :type ctx: discord.Interaction

   .. method:: run(ctx, cmd)

      Internal method that builds and sends a modal for the given command, then executes it upon submission.

   Example:

   .. code-block:: python

       from uicord.dev import Panel, state

       panel = Panel(state.DEV_CMDS)
       await panel.show(ctx)

   The panel will only be visible to the user who invoked it (ephemeral).

How It Works
============

1. **Registration**: The ``@register`` decorator adds the function to ``state.DEV_CMDS``.
2. **Panel Creation**: ``Panel`` iterates over the registered commands and creates a button for each.
3. **Interaction**: When a button is clicked, the panel analyses the command's signature and generates a modal with appropriate input components:
   - Required parameters are marked as required in the modal.
   - Default values are pre-filled.
   - Supported types map to Discord UI elements (text inputs, select menus, file uploads, etc.).
4. **Execution**: After the user submits the modal, the panel calls the command with the collected arguments.

Notes
=====

- The module depends on ``discord.py`` (or a fork like ``py-cord``) and the custom ``.components`` module (presumably from UICord).
- Commands are stored in a global state dictionary; restarting the bot clears them.
- Use only for development – not secure for production because any user who can trigger the panel can execute arbitrary registered commands.

Full Example
============

.. code-block:: python

   import discord
   from discord.ext import commands
   from uicord.dev import register, Panel, Option, MultiStr, state

   bot = commands.Bot(command_prefix="!")

   @register()
   async def ping(ctx):
       await ctx.respond("Pong!")

   @register("add")
   async def add_numbers(ctx, a: int, b: int = 0):
       await ctx.respond(f"Result: {a + b}")

   @register()
   async def announce(ctx, channel: discord.TextChannel, message: MultiStr):
       await channel.send(message)
       await ctx.respond(f"Sent to {channel.mention}")

   @register()
   async def pick_role(ctx, role: Option(["admin", "mod", "member"])):
       await ctx.respond(f"You picked {role}")

   @bot.slash_command()
   async def dev(ctx: discord.ApplicationContext):
       panel = Panel(state.DEV_CMDS)
       await panel.show(ctx)

   bot.run("TOKEN")

.. warning::
   Ensure the bot has the required intents (e.g., ``message_content``, ``members``) for some features to work.
