from typing import Self
from backend.formatting import format_for_display
from typing import Callable, Optional, Any

class NodeType:
    """
    This class represents specific type of a node, and is tightly connected with a specific python function
    """

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
        self.__doc__ = __func.__doc__

        if self.func is not None:
            # TODO: Replace with ObjectAlreadyInDBException
            if self.get_name() in NodeType.all_udn:
                raise ValueError(
                    f"NodeType with name '{self.get_name()}' already exists"
                )
            NodeType.all_udn[self.get_name()] = self

    @classmethod
    def clear_udns(cls) -> None:
        """
        Clears all known NodeTypes
        """
        cls.all_udn = {}

    def wrapper(self, *args, **kwargs):
        """
        Will finish creating new NodeType if decorator had some arguments
        Otherwise will call decorated function

        :param \*args: All args for decorated function
        :param \*kwargs: All kwargs for decorated function
        :return: returned value of decorated function
        """
        if self.func is not None:
            return self.func(*args, **kwargs)
        return self.ending_constructor(*args, **kwargs)

    def ending_constructor(self, __func: Callable[[Any], Any]):
        """
        Final stage of creating node type. It may be called either immediatelly when NodeType is created,
        or after parameters are assigned, depending on decorator use (`@NodeType` vs `@NodeType()`) respectively
        """
        self.func = __func
        self.__doc__ = __func.__doc__
        NodeType.all_udn[self.get_name()] = self
        return self

    __call__ = wrapper

    def get_name(self) -> str:
        """
        :return: `Name of function`.
        """
        return self.func.__name__

    def get_arg_types_names(self) -> dict[str, str]:
        """
        :return: dictionary in format {arg_name: arg_type_name}
        """
        return {
            arg_name: arg_type.__name__
            for arg_name, arg_type in self.func.__annotations__.items()
            if arg_name != "return"
        }

    def get_arg_types(self) -> dict[str, type]:
        """
        :return: dictionary in format {arg_name: arg_type}
        """
        return {
            arg_name: arg_type
            for arg_name, arg_type in self.func.__annotations__.items()
            if arg_name != "return"
        }

    def get_arg_names(self) -> list[str]:
        """
        :return: list of input arguments
        """
        return [
            arg_name
            for arg_name in self.func.__code__.co_varnames[: self.get_arg_count()]
        ]

    def get_default_args(self) -> dict[str, object]:
        """
        :return: list of default function arguments of a specific node type
        """
        if self.func.__defaults__ is None:
            return {}

        arg_names = self.get_arg_names()[-len(self.func.__defaults__) :]
        return {
            arg_name: default
            for arg_name, default in zip(arg_names, self.func.__defaults__)
        }

    def get_arg_count(self) -> int:
        """
        :return: count of function arguments
        """
        return self.func.__code__.co_argcount

    def toJSON(self) -> dict[str, object]:
        """
        Sertalizes this object in order to send it through the rest api

        :return: dictionary in format: {field_name : field_value}
        """
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
