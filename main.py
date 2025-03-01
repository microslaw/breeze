from backend import create_api_server
from backend.datatypes import NodeType, NodeInstance, NodeLink
import backend.repository as repository
import pandas as pd

@NodeType
def add_int(a, b: int) -> int:
    return a + b

@NodeType
def remove_outliers(df:pd.DataFrame, colname:str, sd_limit:float) -> pd.DataFrame:
    df = df.copy()
    df['z_score'] = (df[colname] - df[colname].mean()) / df[colname].std()
    df = df[df['z_score'].abs() < sd_limit]
    return df



# this lines create a following workflow:
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


api_server = create_api_server()
api_server.run(debug=True)

