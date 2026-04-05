"""
lang/uistring.py
----------------
UIString - a ``str`` subclass that passes itself through
``state.translator_function`` at construction time (or lazily when
``.translate(lang)`` is called explicitly).

Usage
-----
::

    from uicord.lang import UIString
    from uicord import state

    state.translator_function = lambda text, lang: my_i18n(text, lang)

    label = UIString("hello.greeting")          # translated with lang=None
    label_fr = UIString("hello.greeting", lang="fr")  # translated with lang="fr"
"""

from __future__ import annotations

from uicord.state import state


class UIString(str):
    """
    A string subclass that is optionally passed through
    ``state.translator_function`` at creation time.

    Parameters
    ----------
    text:
        The raw string or translation key.
    lang:
        The language code to pass to the translator.  When *None* the
        translator receives *None* and can fall back to a default locale.
    """

    # Keep the original key around so callers can re-translate later.
    _original: str
    _lang: str | None

    def __new__(cls, text: str = "", lang: str | None = None) -> "UIString":
        translated = cls._apply_translator(text, lang)
        instance = super().__new__(cls, translated)
        instance._original = text
        instance._lang = lang
        return instance

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def translate(self, lang: str | None = None) -> "UIString":
        """Return a new :class:`UIString` translated into *lang*."""
        return UIString(self._original, lang=lang)

    def with_lang(self, lang: str | None) -> "UIString":
        """Alias for :meth:`translate`."""
        return self.translate(lang)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    @staticmethod
    def _apply_translator(text: str, lang: str | None) -> str:
        fn = state.translator_function
        if fn is None:
            return text
        try:
            return fn(text, lang)
        except Exception:
            return text

    def __repr__(self) -> str:
        return f"UIString({str(self)!r}, lang={self._lang!r})"
