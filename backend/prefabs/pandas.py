import pandas as pd
from breeze import NodeType
from backend.formatting import add_display_format, add_input_format, FrontendDisplayType


@NodeType(tags=["pandas", "import"])
def read_csv(file: str) -> pd.DataFrame:
    """
    Read a CSV file using pandas.

    :param file: Path to the CSV file.
    :type file: str
    :return: DataFrame containing the CSV data.
    :rtype: pandas.DataFrame
    """
    return pd.read_csv(file)


@NodeType(tags=["pandas"])
def select_columns(df: pd.DataFrame, colnames: list[str]) -> pd.DataFrame:
    """
    Select a subset of columns from a DataFrame.

    :param df: DataFrame to select columns from.
    :type df: pandas.DataFrame
    :param colnames: List of column names to select.
    :type colnames: list[str]
    :return: DataFrame with selected columns.
    :rtype: pandas.DataFrame
    """
    return df[colnames]


@NodeType(tags=["pandas"])
def groupby_agg(
    df: pd.DataFrame, group_colnames: list[str], agg_dict: dict[str, str]
) -> pd.DataFrame:
    """
    Group a DataFrame by columns and aggregate using specified functions.

    :param df: DataFrame to group and aggregate.
    :type df: pandas.DataFrame
    :param group_colnames: List of column names to group by.
    :type group_colnames: list[str]
    :param agg_dict: Dictionary mapping column names to aggregation functions.
    :type agg_dict: dict[str, str]
    :return: Aggregated DataFrame.
    :rtype: pandas.DataFrame
    """
    return df.groupby(group_colnames, as_index=False).agg(agg_dict)


@NodeType(tags=["pandas"])
def filter(
    df: pd.DataFrame, colname: str, value: str, condition: str = "equal"
) -> pd.DataFrame:
    """
    Filter rows in a DataFrame based on a condition.

    :param df: DataFrame to filter.
    :type df: pandas.DataFrame
    :param colname: Column name to apply the filter on.
    :type colname: str
    :param value: Value to compare against.
    :type value: str
    :param condition: Condition for filtering ('equal', 'less_than', 'greater_than').
    :type condition: str, optional
    :return: Filtered DataFrame.
    :rtype: pandas.DataFrame
    """
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
add_display_format(
    pd.DataFrame, lambda x: x.head().to_html(), FrontendDisplayType.html_div
)
add_display_format(list[str], lambda x: ",".join(x))
