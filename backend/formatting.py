from types import GenericAlias
from typing import Optional, Callable, Any

display_format_map: dict[type, Callable[[Any], Any]] = {}
input_format_map: dict[type, Callable[[Any], Any]] = {}

# TODO implement formatting exception


def add_display_format(type: type, format_function: Callable[[type], Any]):
    display_format_map[type] = format_function


def add_input_format(type: type, format_function: Callable[[type], Any]):
    input_format_map[type] = format_function


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
