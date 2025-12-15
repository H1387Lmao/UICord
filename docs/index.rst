Welcome to UICord's Documentation!
==================================

UICord is a Python library for helping make Components V2 in Pycord.

.. note::
   This project is currently in developement, any contributions is welcome!

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage


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
