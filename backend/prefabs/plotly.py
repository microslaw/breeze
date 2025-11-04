import plotly.express as px
from plotly.graph_objects import Figure
import pandas as pd
from breeze import NodeType
from backend.formatting import add_display_format, FrontendDisplayType
from typing import Optional


@NodeType(tags=["plotly"])
def histogram(
    df: pd.DataFrame,
    x: str,
    color: Optional[str] = None,
) -> Figure:
    """
    Create a histogram plot using Plotly.

    :param df: DataFrame containing the data to plot.
    :type df: pandas.DataFrame
    :param x: Colname to plot on the x-axis.
    :type x: str
    :param color: Optional column name for color grouping.
    :type color: str, optional
    :return: Histogram as plotly Figure object.
    :rtype: plotly.graph_objects.Figure
    """
    return px.histogram(data_frame=df, x=x, color=color, barmode="group")


@NodeType(tags=["plotly"])
def scatterplot(
    df: pd.DataFrame = None,
    x: str = None,
    y: str = None,
    color: Optional[str] = None,
    trendline: Optional[str] = None,
) -> Figure:
    """
    Create a scatterplot using Plotly.

    :param df: DataFrame containing the data to plot.
    :type df: pandas.DataFrame
    :param x: Colname to plot on the x-axis.
    :type x: str
    :param y: Colname to plot on the y-axis.
    :type y: str
    :param color: Optional column name for color grouping.
    :type color: str, optional
    :param trendline: Option whether to add trendline to the plot
    :type trendline: str, optional
    :return: Scatterplot as plotly Figure object.
    :rtype: plotly.graph_objects.Figure
    """
    return px.scatter(data_frame=df, x=x, y=y, color=color, trendline=trendline)


@NodeType(tags=["plotly"])
def scatterplot_3d(
    df: pd.DataFrame = None,
    x: str = None,
    y: str = None,
    z: str = None,
    color: Optional[str] = None,
) -> Figure:
    """
    Create a 3d scatterplot using Plotly.

    :param df: DataFrame containing the data to plot.
    :type df: pandas.DataFrame
    :param x: Colname to plot on the x-axis.
    :type x: str
    :param y: Colname to plot on the y-axis.
    :type y: str
    :param z: Colname to plot on the z-axis.
    :type z: str
    :param color: Optional column name for color grouping.
    :type color: str, optional
    :return: 3d scatterplot as plotly Figure object.
    :rtype: plotly.graph_objects.Figure
    """
    return px.scatter_3d(data_frame=df, x=x, y=y, z=z, color=color)

@NodeType(tags=["plotly"])
def corr_plot(df:pd.DataFrame):
    return px.imshow(df.corr())


add_display_format(Figure, lambda x: x.to_html(), FrontendDisplayType.html_website)
