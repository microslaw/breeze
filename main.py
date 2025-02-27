from backend import api_server
from backend import NodeType
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

api_server.run(debug=True)
print(NodeType.all_udn)
