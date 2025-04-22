from backend.formatting import format_for_display, format_from_input


# intermediate object for node instances
class NodeInstance:

    # omiting uuid, for simplicity of api calls and testing

    def __init__(self, node_id, node_type, position_x, position_y, overwrite_kwargs=None):
        self.node_id = node_id
        self.node_type = node_type
        self.position_x = position_x
        self.position_y = position_y
        self.overwrite_kwargs = overwrite_kwargs if overwrite_kwargs is not None else {}

    def toJSON(self):
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

    def fromJSON(json):

        if "overwrite_kwargs" in json:
            overwrite_kwargs = {
                arg_name: format_from_input(value) for arg_name, value in json["overwrite_kwargs"]
            }
        else:
            overwrite_kwargs = {}

        return NodeInstance(
            node_id=json["node_id"] if "node_id" in json else None,
            node_type=json["node_type"] if "node_type" in json else None,
            position_x=json["position_x"] if "position_x" in json else None,
            position_y=json["position_y"] if "position_y" in json else None,
            overwrite_kwargs=overwrite_kwargs,
        )
