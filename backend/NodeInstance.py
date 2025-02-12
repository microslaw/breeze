# creating instances of nodes as pickled classes, may be changed to something like sqlite later
class NodeInstance:
    # omiting uuid, for simplicity of api calls and testing
    node_id: int = None
    node_type: str = None
    node_inputs: dict = None
    # will add handling for multiple outputs later
    node_output = None

    def __init__(self, node_id, node_type, input_nodes_ids):
        self.node_id = node_id
        self.node_type = node_type
        self.node_inputs = input_nodes_ids

    def toJSON(self):
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "node_inputs": self.node_inputs,
            "node_output": self.node_output
        }

    def process(self):
        raise NotImplementedError
