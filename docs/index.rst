Welcome to UICord's Documentation!
==================================

This is the main page for the UICord library.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   examples

Overview
--------

UICord is a Python library for helping make Components V2 in Pycord.

Example
-------

Here’s a small example of how to use UICord:

.. code-block:: python

    from uicord import *

    def ExampleView():
        MyView = View()
        MyButton = Button("MyButton", color=Colors.Green)
        MyContainer = Container(
            Text("Hello this is my text!"),
            MyButton
        )
        MyView.add(MyContainer)

        @interaction(component=MyButton)
        async def clicked_on_button(ctx):
            MyButton.label="Changed!"
            await View.reload(ctx) #reloads the view, (Updates all the Component Buffers)

        return MyView
