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
^^^^^^^

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
