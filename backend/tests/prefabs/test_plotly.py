from backend.datatypes import NodeType
from importlib import reload
from backend import BreezeApp
import backend.prefabs.pandas
import backend.prefabs.plotly
import pandas as pd


def initalize_app() -> BreezeApp:
    app = BreezeApp()

    NodeType.clear_udns()
    reload(backend.prefabs.plotly)
    reload(backend.prefabs.pandas)
    app.repository.load_workflow("backend/tests/workflows/plotly")
    app.repository.write_kwarg("backend/prefabs/data/iris.csv", 0, kwarg_name="file")

    return app


def test_initialization():
    app = initalize_app()
    assert app.repository.get_all_node_types() == [
        "histogram",
        "scatterplot",
        "scatterplot_3d",
        "read_csv",
        "select_columns",
        "groupby_agg",
        "filter",
    ]


def test_histogram():
    app = initalize_app()

    app.repository.write_kwarg("sepal.length", 1, "x")
    app.repository.write_kwarg("variety", 1, "color")

    app.processor.update_processing_schedule(1)
    app.processor.wait_till_finished()

    assert app.processor.get_processing_schedule() == []


def test_scatterplot():
    app = initalize_app()

    app.repository.write_kwarg("sepal.length", 2, "x")
    app.repository.write_kwarg("sepal.width", 2, "y")
    app.repository.write_kwarg("variety", 2, "color")
    app.repository.write_kwarg("ols", 2, "trendline")

    app.processor.update_processing_schedule(2)
    app.processor.wait_till_finished()

    assert app.processor.get_processing_schedule() == []


def test_scatterplot_3d():
    app = initalize_app()

    app.repository.write_kwarg("sepal.length", 3, "x")
    app.repository.write_kwarg("sepal.width", 3, "y")
    app.repository.write_kwarg("petal.length", 3, "z")
    app.repository.write_kwarg("variety", 3, "color")

    app.processor.update_processing_schedule(3)
    app.processor.wait_till_finished()

    assert app.processor.get_processing_schedule() == []
