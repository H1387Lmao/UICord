Installation
============

.. _installation:

.. note::
   This project requires Pycord version 2.7 or more

UICord
------

| To install UICord, make sure you have the correct dependencies.

.. code-block:: console

   $ git clone https://github.com/H1387Lmao/UICord.git --depth=1
   $ pip install -r requirements.txt
   $ pip install .

Check
-----

| To check installation. run these:

.. code-block:: python

    >> import uicord
    >> print("Installed:",uicord.View.__class__.__name__=="View")
    # [Should print out "Installed: True"]
