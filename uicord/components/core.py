import inspect

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
                    try:
                        await dev.send(
                            f"FROM: {ctx.user.mention}\n"
                            f"SERVER: `{ctx.guild.name if ctx.guild else "DMS"}`\n"
                            f"COMPONENT: {component.__class__.__name__}\n"
                            f"```\n{exc}\n```"
                        )
                    except:
                        pass
                await ctx.respond(
                    f"Error found while interacting with: "
                    f"{component.__class__.__name__}\n"
                    "Already contacted the developer on this issue!",
                    ephemeral=True,
                )
                print(f"\033[91m{exc}\033[0m")

        # Toggle / Text / RadioButtons use `.cb`; everything else uses `.callback`
        from uicord.components.buttons import Toggle
        from uicord.components.text    import Text
        from uicord.components.choices import RadioButtons

        if not isinstance(component, (Toggle, Text, RadioButtons)):
            component.callback = interact
        else:
            component.cb = interact

    return wrapper

class UIMember:
    def attach(self, fn):
        interaction(self)(fn) # attaches
    def interact(self, fn):
        self.attach(fn)