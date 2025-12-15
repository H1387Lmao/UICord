usage
=====

View
--------

.. py:class:: View(discord.ui.DesignerView)
   The main container of every component!
   :param discord.ui.DesignerView: Pycord's DesignerView
   .. py:method:: __init__()
      The class's init function
   .. py:method:: add(component)
      Adds the component to the view.
      :param component: The component to be put
      :return: Returns the component, helpful for single line adds.
   .. py:method:: reload(ctx)
      Reloads the main buffer, basically updating every component.
      :param ctx: The pycord's interaction context
      :return: None
