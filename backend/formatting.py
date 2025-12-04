from types import GenericAlias
from typing import Optional, Callable, Any, TypeVar
from datetime import datetime
from enum import Enum
from abc import ABCMeta

class FrontendDisplayType(Enum):
    image = "image"
    html_div = "html_div"
    html_website = "html_website"
    plaintext = "plaintext"
    json = "json"
    integer = "integer"
    decimal = "decimal"


display_format_map: dict[type, Callable[[Any], Any]] = {}
frontend_type_format_map: dict[type, FrontendDisplayType] = {}
input_format_map: dict[type, Callable[[Any], Any]] = {}
tag_color_map: dict[str, str] = {}

# TODO implement formatting exception


T_display = TypeVar("T_display", bound=type)


def add_display_format(
    object_type: T_display,
    format_function: Callable[[T_display], Any],
    frontend_type: FrontendDisplayType = FrontendDisplayType.plaintext,
) -> None:
    """
    Adds format of a specified type to global format dictionary

    :param object_type: type of object to be formatted
    :param format_function: function that takes in object of type `object_type` and returns a formatted object. Format function is called within `format_for_display`
    """
    display_format_map[object_type] = format_function
    frontend_type_format_map[object_type] = frontend_type


T_input = TypeVar("T_input", bound=type)


def add_input_format(input_type: T_input, format_function: Callable[[T_input], Any]):
    """
    Adds input mapping to global input list
    :param input_type: type of input to be mapped
    :param format_function: function that takes in object of type `input_type` and returns a python object. Format function is called within `format_from_input`
    """
    input_format_map[input_type] = format_function


def add_tag_color_mapping(tag: str, colour: str):
    """
    Makes tag appear with a specific color
    """

    if len(colour) != 7 or colour[0] != "#":
        raise ValueError(f"Colour should have format: #112233 but has {colour}")
    tag_color_map[tag] = colour


def format_for_display(obj: object) -> object:
    """
    Formats any object with a specified function before sending it to frontend.

    :param obj: object to be formatted
    :return: object prepared for display on the frontend
    """
    if type(obj) in display_format_map:
        return display_format_map[type(obj)](obj)

    if type(obj) is GenericAlias:
        obj_str = str(obj)
    elif isinstance(obj, type):
        obj_str = str(obj)
    else:
        obj_str = obj.__str__()

    if len(obj_str) > 100:
        obj_str = obj_str[:100] + "..."

    return obj_str


def frontend_display_type(obj: object) -> str:
    """
    Returns the FrontendDisplayType of the object
    :param obj: object to be checked
    :return: FrontendDisplayType name
    """
    if type(obj) in frontend_type_format_map:
        return frontend_type_format_map[type(obj)].name
    else:
        return FrontendDisplayType.plaintext.value


def get_tag_color_map():
    """
    Returns the map of frontend coloring
    """
    return tag_color_map


def format_from_input(obj: object, type: Optional[type] = None) -> object:
    """
    Formats any object with a specified function after receiving it from the frontend.
    :param obj: object to be formatted
    :return: python objects
    """
    if type is None or type not in input_format_map:
        return str(obj)

    return input_format_map[type](obj)


def show(x: object):
    """
    Function intended to be passed into add_input_format or add_display format
    for debugging formatting

    :param x: object to be printed
    """
    print(f"Formatting object of type {type(x)}  :")
    print(x)


# default formattings
add_input_format(str, lambda x: x.decode("utf-8"))
add_input_format(float, lambda x: float(x.decode("utf-8")))
add_input_format(int, lambda x: int(x.decode("utf-8")))
add_display_format(type, lambda x: x.__name__)
add_display_format(type(None), lambda _: None)
add_display_format(datetime, lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
add_display_format(int, lambda x: str(x), FrontendDisplayType.integer)
add_display_format(str, lambda x: str(x), FrontendDisplayType.plaintext)
add_display_format(ABCMeta, lambda x: str(x))
add_display_format(ABCMeta, lambda x: str(x))
add_display_format(type(None), lambda _: "None")

add_tag_color_mapping("plotly", "#89f1b6")
add_tag_color_mapping("pandas", "#9289f1")
add_tag_color_mapping("numpy", "#f7935d")
add_tag_color_mapping("import", "#f189d2")
