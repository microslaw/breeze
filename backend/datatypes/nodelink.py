from typing import Self


class NodeLink:

    # omiting uuid, for simplicity of api calls and testing
    origin_node_id: int = None
    # origin node may have only single input, in that case this field should be None
    origin_node_output: str = None
    destination_node_id: int = None
    destination_node_input: str = None

    def __init__(
        self,
        origin_node_id,
        origin_node_output,
        destination_node_id,
        destination_node_input,
    ):
        self.origin_node_id = origin_node_id
        self.origin_node_output = origin_node_output
        self.destination_node_id = destination_node_id
        self.destination_node_input = destination_node_input

    def toNameDict(self) -> dict[str, object]:
        return {
            "origin_node_id": self.origin_node_id,
            "origin_node_output": self.origin_node_output,
            "destination_node_id": self.destination_node_id,
            "destination_node_input": self.destination_node_input,
        }

    def fromNamedDict(nameDict: dict[str, object]) -> Self:
        return NodeLink(
            origin_node_id=nameDict["origin_node_id"],
            origin_node_output=nameDict["origin_node_output"],
            destination_node_id=nameDict["destination_node_id"],
            destination_node_input=nameDict.get("destination_node_input"),
        )
