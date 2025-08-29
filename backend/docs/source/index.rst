.. breeze documentation master file, created by
   sphinx-quickstart on Tue Jul 22 18:38:48 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Breeze
====================

**Breeze** is a Python library for visualization of computations, similar to tools like KNIME<https://www.knime.com/>.

.. note::

   This project is under active development.

To create your first breeze app run:

.. code-block:: Python

   from breeze import BreezeApp
   br = BreezeApp()
   br.start()

To get more nodetypes you can:

1. Import some of builtin prefabs:

   .. code-block:: Python

      from breeze import BreezeApp, prefabs

      prefabs.load_pandas()

      if __name__ == "__main__":
         br = BreezeApp()
         br.start()


2. Add some nodetypes of your own:

   .. code-block:: Python

      from breeze import BreezeApp, NodeType

      @NodeType
      def add(a, b):
         return a + b

      if __name__ == "__main__":
      br = BreezeApp()
      br.start()

See also:

.. toctree::
   :maxdepth: 1

   prefabs.rst
   creating_nodetypes.rst
   datatypes.rst
   helper_classes.rst