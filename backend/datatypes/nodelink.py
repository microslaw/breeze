from typing import Optional


class NodeLink:
    def __init__(
        self,
        node_link_id: int,
        origin_node_id: int,
        origin_node_output: Optional[str],
        destination_node_id: int,
        destination_node_input: str,
    ):
        self.node_link_id: int = node_link_id
        self.origin_node_id: int = origin_node_id
        self.origin_node_output: Optional[str] = origin_node_output
        self.destination_node_id: int = destination_node_id
        self.destination_node_input: str = destination_node_input

    def toNameDict(self) -> dict[str, object]:
        """
        Used to serialize this object
        Inverse of fromNameDict

        :return: dictionary in format: {field_name : field_value}
        """
        return {
            "node_link_id": self.node_link_id,
            "origin_node_id": self.origin_node_id,
            "origin_node_output": self.origin_node_output,
            "destination_node_id": self.destination_node_id,
            "destination_node_input": self.destination_node_input,
        }

    @staticmethod
    def fromNameDict(nameDict: dict[str, object]) -> "NodeLink":
        """
        Creates a NodeLink object from json serializable name dict
        Inverse of toNameDict

        :param nameDict: dictionary in format: {field_name : field_value}, e.g. output of `NodeLink.toNameDict`
        """
        return NodeLink(
            node_link_id=nameDict.get("node_link_id"),
            origin_node_id=nameDict.get("origin_node_id"),
            origin_node_output=nameDict.get("origin_node_output"),
            destination_node_id=nameDict.get("destination_node_id"),
            destination_node_input=nameDict.get("destination_node_input"),
        )
