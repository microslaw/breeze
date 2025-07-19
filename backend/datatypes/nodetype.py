from typing import Self
from backend.formatting import format_for_display
from typing import Callable, Optional, Any


class NodeType:
    all_udn: dict[str, Self] = {}

    # Prefferable way of doing that (see below) will be made possible in python 3.14 (see pep 749)
    # all_udn: dict[str, NodeType] = {}

    # This constuctor may be used in two ways:
    # @NodeType or @NodeType(args)
    # First case will end up as @NodeType(__func), and the function will be assigned correctly
    # In second case, expression will unfold to @NodeType(args)(__func)
    def __init__(
        self,
        __func: Optional[Callable[[Any], Any]] = None,
        tags: list[str] = [],
    ):
        self.func: Callable[[Any], Any] = __func
        self.tags = tags

        if self.func is not None:
            # TODO: Replace with ObjectAlreadyInDBException
            if self.get_name() in NodeType.all_udn:
                raise ValueError(
                    f"NodeType with name '{self.get_name()}' already exists"
                )
            NodeType.all_udn[self.get_name()] = self

    @classmethod
    def clear_udns(cls):
        cls.all_udn = {}

    def wrapper(self, *args, **kwargs):
        if self.func is not None:
            return self.func(*args, **kwargs)
        return self.ending_constructor(*args, **kwargs)

    def ending_constructor(self, __func: Callable[[Any], Any]):
        self.func = __func
        NodeType.all_udn[self.get_name()] = self
        return self

    __call__ = wrapper

    def get_name(self) -> str:
        return self.func.__name__

    def get_arg_types_names(self):
        return {
            arg_name: arg_type.__name__
            for arg_name, arg_type in self.func.__annotations__.items()
            if arg_name != "return"
        }

    def get_arg_types(self) -> dict[str, type]:
        return {
            arg_name: arg_type
            for arg_name, arg_type in self.func.__annotations__.items()
            if arg_name != "return"
        }

    def get_arg_names(self) -> list[str]:
        return [
            arg_name
            for arg_name in self.func.__code__.co_varnames[: self.get_arg_count()]
        ]

    def get_default_args(self) -> dict[str, object]:
        if self.func.__defaults__ is None:
            return {}

        arg_names = self.get_arg_names()[-len(self.func.__defaults__) :]
        return {
            arg_name: default
            for arg_name, default in zip(arg_names, self.func.__defaults__)
        }

    def get_arg_count(self) -> int:
        return self.func.__code__.co_argcount

    def toJSON(self) -> dict[str, object]:
        func_annotations: dict[str, type] = self.func.__annotations__
        if "return" not in func_annotations:
            return_type = None
        else:
            return_type = func_annotations["return"].__name__

        return {
            "name": self.get_name(),
            "arg_names": self.get_arg_names(),
            "arg_types": self.get_arg_types_names(),
            "default_args": {
                arg_name: format_for_display(default_value)
                for arg_name, default_value in self.get_default_args().items()
            },
            "return_type": return_type,
            "tags": self.tags,
        }
