from typing import Self


class NodeLink:

    def __init__(
        self,
        node_link_id,
        origin_node_id,
        origin_node_output,
        destination_node_id,
        destination_node_input,
    ):
        self.node_link_id = node_link_id
        self.origin_node_id = origin_node_id
        self.origin_node_output = origin_node_output
        self.destination_node_id = destination_node_id
        self.destination_node_input = destination_node_input

    def toNameDict(self) -> dict[str, object]:
        return {
            "node_link_id": self.node_link_id,
            "origin_node_id": self.origin_node_id,
            "origin_node_output": self.origin_node_output,
            "destination_node_id": self.destination_node_id,
            "destination_node_input": self.destination_node_input,
        }

    def fromNameDict(nameDict: dict[str, object]) -> Self:
        return NodeLink(
            node_link_id=nameDict.get("node_link_id"),
            origin_node_id=nameDict["origin_node_id"],
            origin_node_output=nameDict["origin_node_output"],
            destination_node_id=nameDict["destination_node_id"],
            destination_node_input=nameDict.get("destination_node_input"),
        )
