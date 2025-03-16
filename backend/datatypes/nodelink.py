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

    def toJSON(self):
        return {
            "origin_node_id": self.origin_node_id,
            "origin_node_output": self.origin_node_output,
            "destination_node_id": self.destination_node_id,
            "destination_node_input": self.destination_node_input,
        }

    def fromJSON(json):
        return NodeLink(
            origin_node_id=json["origin_node_id"],
            origin_node_output=json["origin_node_output"],
            destination_node_id=json["destination_node_id"],
            destination_node_input=json.get("destination_node_input", None),
        )
