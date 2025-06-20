import pandas as pd
from breeze import NodeType
from backend.formatting import add_display_format, add_input_format
import ast


@NodeType(tags=["pandas", "import"])
def read_csv(file: str):
    return pd.read_csv(file)


@NodeType(tags=["pandas"])
def select_columns(df: pd.DataFrame, colnames: list[str]) -> pd.DataFrame:
    return df[colnames]


@NodeType(tags=["pandas"])
def groupby_agg(df: pd.DataFrame, group_colnames: list[str], agg_dict: dict[str, str]):
    return df.groupby(group_colnames,as_index=False).agg(agg_dict)


@NodeType(tags=["pandas"])
def filter(df: pd.DataFrame, colname: str, value: str, condition: str = "equal"):
    filtered_column = df[colname].astype(str)
    if condition == "equal":
        filtered_rows = filtered_column == value
    elif condition == "less_than":
        filtered_rows = filtered_column < value
    elif condition == "greater_than":
        filtered_rows = filtered_column > value

    return df[filtered_rows]


add_input_format(list[str], lambda x: x.decode("utf-8").split(","))
add_input_format(
    dict[str, str],
    lambda x: {x.split(":")[0]: x.split(":")[1] for x in x.decode("utf-8").split(",")},
)
add_display_format(pd.DataFrame, lambda x: x.head().to_html())
