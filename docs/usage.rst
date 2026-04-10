Components
==========

Layouts
--------

.. autoclass:: uicord.View
   :members:
   :undoc-members:
   :show-inheritance:
   
.. autoclass:: uicord.Modal
   :members:
   :undoc-members:
   :show-inheritance:

Decorators
----------

.. autofunction:: uicord.interaction

Example
"""""""

.. code-block:: python

    MyView = View()
    MyBtn = Button()
    MyView.add(MyBtn)

    @uicord.interaction(component=MyBtn)
    async def btnclick(ctx):
        print("BUTTON WAS CLICKED!!!!")
        await ctx.respond("Yay you clicked my button")


Components
----------

.. autoclass:: uicord.Container
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.Button
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.Toggle
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.ActionRow
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.Text
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.Separator
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.Thumbnail
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.Section
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.MediaGallery
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.MediaGalleryItem
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.ButtonChoices
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.Choices
   :members:
   :undoc-members:
   :show-inheritance:

Pycord 2.8+ Components
-----------------------

.. note::
   The following components require **pycord ≥ 2.8**.  On older versions,
   instantiating them raises :class:`NotImplementedError`.

.. autoclass:: uicord.Checkbox
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.CheckboxGroup
   :members:
   :undoc-members:
   :show-inheritance:

Internationalisation
--------------------

.. autoclass:: uicord.UIString
   :members:
   :undoc-members:
   :show-inheritance:

Example
"""""""

.. code-block:: python

    from uicord import state, UIString, View, Button

    # Plug in your own translation backend
    state.translator_function = lambda text, lang: my_i18n(text, lang)

    # Strings are translated at construction time
    label = UIString("btn.confirm")            # uses lang=None (default locale)
    label_fr = UIString("btn.confirm", lang="fr")

    # Views and Modals carry a lang that UIString picks up automatically
    view = View(lang="fr")
    btn  = Button(view._("btn.confirm"))       # translated to French

State
-----

.. autoclass:: uicord.state
   :members:
   :undoc-members:

Utilities
---------

.. autofunction:: uicord.format_values----------

.. autoclass:: uicord.Container
   :members:
   :undoc-members:
   :show-inheritance:

   
.. autoclass:: uicord.Button
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.ActionRow
   :members:
   :undoc-members:
   :show-inheritance:

   
.. autoclass:: uicord.Text
   :members:
   :undoc-members:
   :show-inheritance:
   
.. autoclass:: uicord.Separator
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.Thumbnail
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.Section
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.ButtonChoices
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: uicord.Choices
   :members:
   :undoc-members:
   :show-inheritance:

dev
