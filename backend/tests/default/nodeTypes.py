from backend.datatypes import NodeType
import pandas as pd

# data in .csv files will create a following workflow:
# +--+
# |n0|->\
# +--+   \     +--+
#         +--> |n2|->\
# +--+   /     +--+   \   +--+
# |n1|->/              \->|n3|
# +--+                    +--+


@NodeType
def add_int(a, b: int) -> int:
    return a + b


@NodeType
def remove_outliers(df: pd.DataFrame, colname: str, sd_limit: float = 3) -> pd.DataFrame:
    df = df.copy()
    df["z_score"] = (df[colname] - df[colname].mean()) / df[colname].std()
    df = df[df["z_score"].abs() < sd_limit]
    return df
