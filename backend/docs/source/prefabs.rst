Prefabs
=======

Breeze has many builtin functions from other python libraries.
You can import them as prefabs by:

.. code-block:: Python

    from breeze import BreezeApp, prefabs

    prefabs.load_pandas()

    if __name__ == "__main__":
        br = BreezeApp()
        br.start()

Currently available prefabs are:

.. toctree::
   :maxdepth: 1

   prefabs/pandas.rst
   prefabs/plotly.rst