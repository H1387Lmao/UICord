"""
state.py
--------
Global library state. Import and mutate freely from user code.
"""


class _State:
    """Mutable global state for the library."""

    DEV_IDS: list[int] = []
    """List of developer user IDs that receive error reports."""

    translator_function = None
    """
    Optional callable used by UIString to translate text.

    Signature: translator_function(text: str, lang: str | None) -> str

    Set this to hook in your own i18n backend::

        import mylib
        mylib.state.translator_function = my_translate_fn
    """


state = _State()
