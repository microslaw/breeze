# in a full implementation this file would not exist, as all the data contained here would be read either from code or
# created on the frontend

from NodeInstance import NodeInstance
from utils import persistance
import os
import shutil

node1 = NodeInstance(
    node_id=1,
    node_type="add_int",
    input_nodes_ids={},
)
node2 = NodeInstance(
    node_id=2,
    node_type="add_int",
    input_nodes_ids={},
)
node3 = NodeInstance(
    node_id=3,
    node_type="add_int",
    input_nodes_ids={"a": 1, "b": 2},
)

node4 = NodeInstance(
    node_id=4,
    node_type="remove_outliers",
    input_nodes_ids={"sd_limit", 3},
)

# +--+
# |n1|->\
# +--+   \     +--+
#         +--> |n3|->\
# +--+   /     +--+   \   +--+
# |n2|->/              \->|n4|
# +--+                    +--+

nodes_dir = "./backend/data/nodes"
if os.path.exists(nodes_dir):
    shutil.rmtree(nodes_dir)
os.makedirs(nodes_dir)

node_instances = [node1, node2, node3, node4]
print("writing")
for node in node_instances:
    persistance.write_pickle(node, f"{nodes_dir}/node_{node.node_id}.pickle")
