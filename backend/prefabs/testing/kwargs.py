from backend.datatypes import NodeType
import pandas as pd
from backend.formatting import add_input_format

@NodeType(tags=["testing"])
def add_float(a: float, b: float) -> float:
    return a + b

@NodeType(tags=["testing"])
def round_float(to_round:float, digits:int = 2):
    return round(to_round, ndigits=digits)

class MyClass:
    def __init__(self, name: str):
        self.name = name

    def describe(self):
        return f"MyClass named {self.name}"


add_input_format(MyClass, lambda x: MyClass(x.decode("utf-8")))
@NodeType(tags=["testing"])
def describe_myclass(instance: MyClass):
    return instance.describe()
