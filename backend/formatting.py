from types import GenericAlias
from typing import Optional, Callable, Any, TypeVar

display_format_map: dict[type, Callable[[Any], Any]] = {}
input_format_map: dict[type, Callable[[Any], Any]] = {}

# TODO implement formatting exception


T_display = TypeVar("T_display", bound=type)


def add_display_format(
    object_type: T_display, format_function: Callable[[T_display], Any]
):
    display_format_map[object_type] = format_function


T_input = TypeVar("T_input", bound=type)


def add_input_format(input_type: T_input, format_function: Callable[[T_input], Any]):
    input_format_map[input_type] = format_function


def format_for_display(obj: object) -> object:
    if type(obj) in display_format_map:
        return display_format_map[type(obj)](obj)

    if type(obj) is GenericAlias:
        obj_str = str(obj)
    else:
        obj_str = obj.__str__()

    if len(obj_str) > 100:
        obj_str = obj_str[:100] + "..."

    return obj_str


def format_from_input(obj: object, type: Optional[type] = None) -> object:
    if type is None or type not in input_format_map:
        return str(obj)

    return input_format_map[type](obj)


def show(x: object):
    """Function intended for debugging formatting"""
    print(f"Formatting object of type {type(x)}  :")
    print(x)


# default formattings
add_input_format(str, lambda x: x.decode("utf-8"))
add_input_format(float, lambda x: float(x.decode("utf-8")))
add_input_format(int, lambda x: int(x.decode("utf-8")))
add_display_format(type, lambda x: x.__name__)
add_display_format(type(None), lambda _: None)
