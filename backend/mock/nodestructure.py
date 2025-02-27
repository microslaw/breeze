import backend.repository as repository
from backend.datatypes import NodeInstance, NodeLink
# in a full implementation this file would not exist, as all the data contained here would be read either from code or
# created on the frontend

# this file creates a following workflow:
# +--+
# |n1|->\
# +--+   \     +--+
#         +--> |n3|->\
# +--+   /     +--+   \   +--+
# |n2|->/              \->|n4|
# +--+                    +--+


repository.create_node_link(NodeLink(1, None, 3, 'a'))
repository.create_node_link(NodeLink(2, None, 3, 'b'))
repository.create_node_link(NodeLink(3, None, 4, 'sd_limit'))

repository.create_node_instance(NodeInstance(1, 'add_int'))
repository.create_node_instance(NodeInstance(2, 'add_int'))
repository.create_node_instance(NodeInstance(3, 'add_int'))
repository.create_node_instance(NodeInstance(4, 'remove_outliers'))
