from backend.formatting import format_for_display, format_from_input
from typing import Optional, Any


# intermediate object for node instances
class NodeInstance:
    # omiting uuid, for simplicity of api calls and testing

    def __init__(
        self,
        node_id: int,
        node_type_name: str,
        position_x: int,
        position_y: int,
        overwrite_kwargs: Optional[dict[str, object]] = None,
        instance_name: Optional[str] = None,
    ):
        self.node_id: int = node_id
        self.node_type_name: str = node_type_name
        self.position_x: int = position_x
        self.position_y: int = position_y
        self.overwrite_kwargs: dict[str, object] = (
            overwrite_kwargs if overwrite_kwargs is not None else {}
        )
        self.instance_name: Optional[str] = instance_name

    def toNameDict(self) -> dict[str, object]:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type_name,
            "position_x": self.position_x,
            "position_y": self.position_y,
            "overwrite_kwargs": {
                arg_name: format_for_display(value)
                for arg_name, value in self.overwrite_kwargs.items()
            },
            "instance_name": self.instance_name,
        }

    @staticmethod
    def fromNameDict(nameDict: dict[str, Any]) -> "NodeInstance":
        if "overwrite_kwargs" in nameDict:
            overwrite_kwargs = {
                arg_name: format_from_input(value)
                for arg_name, value in nameDict["overwrite_kwargs"]
            }
        else:
            overwrite_kwargs = {}

        return NodeInstance(
            node_id=nameDict.get("node_id"),
            node_type_name=nameDict.get("node_type"),
            position_x=nameDict.get("position_x"),
            position_y=nameDict.get("position_y"),
            overwrite_kwargs=overwrite_kwargs,
            instance_name=nameDict.get("instance_name"),
        )
