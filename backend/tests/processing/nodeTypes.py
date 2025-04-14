from backend.datatypes import NodeType
from backend.formatting import add_display_format

# data in .csv files will create a following workflow:
# +--+
# |n0|->\
# +--+   \     +--+
#         +--> |n2|->\
# +--+   /     +--+   \   +--+
# |n1|->/              +->|n4|
# +--+         +--+   /   +--+
#              |n3|->/
#              +--+
# +--+
# |n6|->\
# +--+   \     +--+
#         +--> |n7|->\
# +--+   /     +--+   \   +--+
# |n5|->+--------------+->|n8|
# +--+                    +--+
#
# +--+
# |n9|
# +--+


@NodeType
def add_int(a: int, b: int) -> int:
    return a + b


@NodeType
def const_1():
    return 1


@NodeType
def const_2():
    return 2


@NodeType
def const_a():
    return "a"


class MyClass:
    def __init__(self, name: str):
        self.name = name

    def describe(self):
        return f"MyClass named {self.name}"


add_display_format(MyClass, lambda x: x.describe())


@NodeType
def create_my_class():
    return MyClass("a class")
