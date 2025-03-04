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

repository.init_db()
repository.from_csv("backend/tests/default/nodeInstances.csv", "nodeInstances")
repository.from_csv("backend/tests/default/nodeLinks.csv", "nodeLinks")

api_server = create_api_server()
api_server.run(debug=True)

