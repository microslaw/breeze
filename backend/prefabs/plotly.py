import plotly.express as px
from plotly.graph_objects import Figure
import pandas as pd
from breeze import NodeType
from backend.formatting import add_display_format


@NodeType(tags=["plotly"])
def histogram(df: pd.DataFrame, x: str, color: str = None):
    return px.histogram(data_frame=df, x=x, color=color, barmode="group")


@NodeType(tags=["plotly"])
def scatterplot(
    df: pd.DataFrame = None,
    x: str = None,
    y: str = None,
    color: str = None,
    trendline: str = None,
):
    return px.scatter(data_frame=df, x=x, y=y, color=color, trendline=trendline)


@NodeType(tags=["plotly"])
def scatterplot_3d(
    df: pd.DataFrame = None,
    x: str = None,
    y: str = None,
    z: str = None,
    color: str = None,
):
    return px.scatter_3d(data_frame=df, x=x, y=y, z=z, color=color)


add_display_format(Figure, lambda x: x.to_html())
