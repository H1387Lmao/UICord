import functools
from .layout import *
from .buttons import *
from .view import *
from ..state import state

# taken directly and slightly modified from uma bot lmao.
# umabot already has a good ecosystem so why cant i just reuse in other projects.

def page_buttons(parent_factory, max_pages, current_page=0, loop=False, back_factory=None, far_buttons=False, custom_emojis=False):
    """
    Used to make buttons for navigation

    Args:
        parent_factory (callable): The function called to generate the next view.
        max_pages (int): The amount of pages until it stops allowing for movement.
        current_page (int): The current page to track the page number.
        loop (bool): Flag to allow wrap around
        back_factory (optional callable): If this factory is not none, add a back button to the list of elements.
        custom_emojis (bool): Checks whether it uses custom emojis. Assumes that state.bot is set and has a get_em(str) function. Also assumes that you have ui_farl, ui_farr, ui_r, ui_l, ui_back as emojis.
    Returns:
        List[Separator|ActionRow]: A list with the first being a separator object and the other having an actionrow object

    Examples:
        def simple_pages(page=0):
            return View(
                Text(f"page: {page}"),
                page_buttons(
                    lambda p: simple_pages(page=p),
                    10,
                    page,
                    True,
                    None,
                    True
                )
            )
        >>> None
        page_buttons(lambda p: 0, 10)
        >>> [<Separator divider=True spacing=<SeparatorSpacingSize.small: 1> id=None>, <ActionRow children=[<Button style=2 url=None disabled=True label=None emoji=<PartialEmoji animated=False name='⬅️' id=None> sku_id=None row=None custom_id='4ed6023278c3e482b996ececb21dbcd4' id=None>, <Button style=2 url=None disabled=None label=None emoji=<PartialEmoji animated=False name='➡️' id=None> sku_id=None row=None custom_id='d6fdf85cfd8cd67cbb7d45711288bca2' id=None>] id=None>]
    """
    components = []
    if max_pages== 0:
        loop=False
    back = None if not custom_emojis else state.bot.get_em("ui_back")
    if back_factory: components.append(_create_back_button(back_factory, "Back", back))
    fr = state.bot.get_em("ui_farr") if custom_emojis else "⏩"
    fl = state.bot.get_em("ui_farl") if custom_emojis else "⏪"
    r = state.bot.get_em("ui_r") if custom_emojis else "➡️"
    l = state.bot.get_em("ui_l") if custom_emojis else "⬅️"

    if parent_factory:
        first = Button(None, disabled=(current_page == 0), emoji=fl)
        left = Button(None, disabled=(current_page == 0 and not loop), emoji=l)
        right = Button(None, disabled=(current_page >= max_pages and not loop),emoji=r)
        last = Button(None, disabled=(current_page >= max_pages), emoji=fr)

        @interaction(first)
        async def _first(ctx): await ctx.response.edit_message(view=parent_factory(0))
        @interaction(left)
        async def _left(ctx):
            p = (current_page - 1) % (max_pages + 1) if loop else current_page - 1
            await ctx.response.edit_message(view=parent_factory(p))
        @interaction(right)
        async def _right(ctx):
            p = (current_page + 1) % (max_pages + 1) if loop else current_page + 1
            await ctx.response.edit_message(view=parent_factory(p))
        @interaction(last)
        async def _last(ctx): await ctx.response.edit_message(view=parent_factory(max_pages))
        
        if far_buttons:
            if back_factory: return [Separator(), ActionRow(components[0]), ActionRow(first, left, right, last)]
            return [Separator(), ActionRow(first, left, right, last)]
        components.extend([left, right])
    return [Separator(), ActionRow(*components)]

def _create_back_button(view_factory, text="Back", custom_emoji=None):
    emoji = custom_emojis or "🔙"
    button = Button(emoji=emoji, text=text)
    @interaction(button)
    async def _back(ctx): await ctx.response.edit_message(view=view_factory())
    return button

_back_button = _create_back_button #macro
