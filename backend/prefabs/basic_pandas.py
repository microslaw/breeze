import pandas as pd
from breeze import NodeType

@NodeType(tags=["pandas", "loading"])
def read_csv(file:str):
    return pd.read_csv(file)

@NodeType(tags=["pandas"])
def select_subset(df:pd.DataFrame, subset:list[str]) -> pd.DataFrame:
    return df[subset]

@NodeType(tags=["pandas"])
def groupby_agg(df:pd.DataFrame, group_colnames:list[str], agg_map:dict[str, str]):
    return df.groupby(group_colnames).agg(agg_map)
