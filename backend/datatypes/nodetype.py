from typing import Self


class NodeType:

    all_udn: list[Self] = []

    # Prefferable way of doing that (see below) will be made possible in python 3.14 (see pep 749)
    # all_udn: list[NodeType] = []

    def __init__(self, func):
        self.func = func
        NodeType.all_udn.append(self)

    def clear_udns():
        NodeType.all_udn = []

    def wrapper(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    __call__ = wrapper

    def get_name(self):
        return self.func.__name__

    def get_arg_types_names(self):
        return {
            arg_name: arg_type.__name__
            for arg_name, arg_type in self.func.__annotations__.items()
            if arg_name != "return"
        }

    def get_arg_names(self):
        return [arg_name for arg_name in self.func.__code__.co_varnames]

    def toJSON(self):
        return {
            "name": self.get_name(),
            "arg_names": self.func.__code__.co_varnames,
            "arg_types": self.get_arg_types_names(),
            "return_type": self.func.__annotations__["return"].__name__,
        }
