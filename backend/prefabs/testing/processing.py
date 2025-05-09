from backend.datatypes import NodeType
from backend.formatting import add_display_format

@NodeType(tags=["testing"])
def add_int(a: int, b: int) -> int:
    return a + b


@NodeType(tags=["testing"])
def const_1():
    return 1


@NodeType(tags=["testing"])
def const_2():
    return 2


@NodeType(tags=["testing"])
def const_a():
    return "a"


class MyClass:
    def __init__(self, name: str):
        self.name = name

    def describe(self):
        return f"MyClass named {self.name}"


add_display_format(MyClass, lambda x: x.describe())


@NodeType(tags=["testing"])
def create_my_class():
    return MyClass("a class")
