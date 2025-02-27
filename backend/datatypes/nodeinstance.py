# intermediate object for node instances
class NodeInstance:

    # omiting uuid, for simplicity of api calls and testing
    node_id: int = None
    node_type: str = None

    def __init__(self, node_id, node_type):
        self.node_id = node_id
        self.node_type = node_type

    def toJSON(self):
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
        }

    def fromJSON(json):
        return NodeInstance(
            node_id=json["node_id"],
            node_type=json["node_type"],
        )

    def process(self):
        raise NotImplementedError
