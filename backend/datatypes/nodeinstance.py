from backend.formatting import format_for_display, format_from_input
from typing import Self


# intermediate object for node instances
class NodeInstance:

    # omiting uuid, for simplicity of api calls and testing

    def __init__(
        self, node_id, node_type, position_x, position_y, overwrite_kwargs=None
    ):
        self.node_id = node_id
        self.node_type = node_type
        self.position_x = position_x
        self.position_y = position_y
        self.overwrite_kwargs = overwrite_kwargs if overwrite_kwargs is not None else {}

    def toNameDict(self) -> dict[str, object]:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "position_x": self.position_x,
            "position_y": self.position_y,
            "overwrite_kwargs": {
                arg_name: format_for_display(value)
                for arg_name, value in self.overwrite_kwargs.items()
            },
        }

    def fromNameDict(nameDict: dict[str, object]) -> Self:

        if "overwrite_kwargs" in nameDict:
            overwrite_kwargs = {
                arg_name: format_from_input(value)
                for arg_name, value in nameDict["overwrite_kwargs"]
            }
        else:
            overwrite_kwargs = {}

        return NodeInstance(
            node_id=nameDict.get("node_id"),
            node_type=nameDict.get("node_type"),
            position_x=nameDict.get("position_x"),
            position_y=nameDict.get("position_y"),
            overwrite_kwargs=overwrite_kwargs,
        )
