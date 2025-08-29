Creating new nodetypes
======================


Creating your own node type is as simple as adding a decorator to function:

.. code-block:: Python

    from breeze import BreezeApp, NodeType

    @NodeType
    def add(a, b):
        return a + b

    if __name__ == "__main__":
    br = BreezeApp()
    br.start()


You can also specify tags, in order to group your nodetypes:

.. code-block:: Python

    from breeze import BreezeApp, NodeType

    @NodeType(tags=["math"])
    def add(a, b):
        return a + b

    @NodeType(tags=["math"])
    def subtract(a, b):
        return a - b

    @NodeType(tags=["utils"])
    def list_to_tuple(lst):
        return tuple(lst)

    if __name__ == "__main__":
        br = BreezeApp()
        br.start()


If you would like to display some new classes, you'll need to use formatting:

.. code-block:: Python

    from breeze import BreezeApp, NodeType, add_display_format

    class Square:
        def __init__(self, side_length):
            self.side_length = side_length

    @NodeType
    def create_square(side_length: float) -> Square:
        return Square(side_length)

    add_display_format(
        Square,
        lambda s: f"Square with side length {s.side_length}",
    )
    if __name__ == "__main__":
        br = BreezeApp()
        br.start()


If you'd like to create a new datatype based on some input from frontend you can:

.. code-block:: Python

    from breeze import BreezeApp, NodeType, add_input_format
    import re

    class Square:
        def __init__(self, side_length):
            self.side_length = side_length

        @staticmethod
        def from_string(s: str):
            re.match = re.match(r"Square\((\d+(\.\d+)?)\)", s)
            if not re.match:
                raise ValueError(f"Cannot parse {s} as Square")
            side_length = float(re.match.group(1))

            return Square(side_length)

    @NodeType
    def describe_square(square: Square) -> str:
        return f""" Square of type {type(square)},
            with side length {square.side_length}"""

    add_input_format(Square, lambda x: Square.from_string(x))

    if __name__ == "__main__":
        br = BreezeApp()
        br.start()


.. note::
    class to which the input will be formatted must be specified in type hint


