installation
============

.. _installation:

.. note::
   This project requires Pycord version 2.7 or more

Dependencies
------------
| To install the needed depedencies,
Windows:
.. code-block:: console

   PS> pip install -U pycord --pre

Linux:
.. code-block:: console

   $ python3 -m pip install -U py-cord --pre

UICord
------
| To install UICord, make sure you have the correct dependencies.

.. code-block:: console
   $ git clone https://github.com/H1387Lmao/UICord.git --depth=1
   $ pip install .

Check
-----
| To check installation. run these:
.. code-block:: python

    >> import uicord
    >> print("Installed:",uicord.View.__class__.__name__=="View")
    # [Should print out "Installed: True"]
