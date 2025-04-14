import pandas as pd

display_format_map = {
}


def add_display_format(type: type, format_function: callable):
    display_format_map[type] = format_function


def format_for_display(obj: object) -> object:
    if type(obj) in display_format_map:
        return display_format_map[type(obj)](obj)

    obj_str = obj.__str__()

    if len(obj_str) > 100:
        obj_str = obj_str[:100] + "..."

    return obj_str
