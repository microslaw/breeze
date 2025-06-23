from backend.datatypes import NodeType
from importlib import reload
from backend import BreezeApp
import backend.prefabs.pandas
import pandas as pd


def initalize_app() -> BreezeApp:
    app = BreezeApp()

    NodeType.clear_udns()
    reload(backend.prefabs.pandas)
    app.repository.load_workflow("backend/tests/workflows/pandas")
    app.repository.write_kwarg("backend/prefabs/data/iris.csv", 0, kwarg_name="file")

    return app


def test_initialization():
    app = initalize_app()
    assert app.repository.get_all_node_types() == [
        "read_csv",
        "select_columns",
        "groupby_agg",
        "filter",
    ]


def test_read_csv():
    app = initalize_app()
    app.processor.update_processing_schedule(0)
    app.processor.wait_till_finished()

    df: pd.DataFrame = app.repository.read_output(0)
    assert df.head(2).to_dict() == {
        "petal.length": {
            0: 1.4,
            1: 1.4,
        },
        "petal.width": {
            0: 0.2,
            1: 0.2,
        },
        "sepal.length": {
            0: 5.1,
            1: 4.9,
        },
        "sepal.width": {
            0: 3.5,
            1: 3.0,
        },
        "variety": {
            0: "Setosa",
            1: "Setosa",
        },
    }


def test_df_format_for_display():
    app = initalize_app()
    app.processor.update_processing_schedule(0)
    app.processor.wait_till_finished()

    with app.controller.test_client() as client:
        response = client.get("/processingResult/0")

    assert response.data == (
        b'<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align'
        b': right;">\n      <th></th>\n      <th>sepal.length</th>\n      <th>sepal.w'
        b"idth</th>\n      <th>petal.length</th>\n      <th>petal.width</th>\n      <"
        b"th>variety</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0<"
        b"/th>\n      <td>5.1</td>\n      <td>3.5</td>\n      <td>1.4</td>\n      <td>"
        b"0.2</td>\n      <td>Setosa</td>\n    </tr>\n    <tr>\n      <th>1</th>\n "
        b"     <td>4.9</td>\n      <td>3.0</td>\n      <td>1.4</td>\n      <td>0.2</t"
        b"d>\n      <td>Setosa</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <"
        b"td>4.7</td>\n      <td>3.2</td>\n      <td>1.3</td>\n      <td>0.2</td>\n   "
        b"   <td>Setosa</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>4.6</td"
        b">\n      <td>3.1</td>\n      <td>1.5</td>\n      <td>0.2</td>\n      <td>Set"
        b"osa</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>5.0</td>\n    "
        b"  <td>3.6</td>\n      <td>1.4</td>\n      <td>0.2</td>\n      <td>Setosa</t"
        b"d>\n    </tr>\n  </tbody>\n</table>"
    )
    assert response.status_code == 200


def test_select_columns():
    app = initalize_app()

    with app.controller.test_client() as client:
        response = client.put(
            "/nodeInstances/1/kwargs/colnames", data=b"variety,petal.width"
        )

        assert response.status_code == 200
        assert response.data == b"OK"

        assert app.repository.read_kwarg(1, "colnames") == ["variety", "petal.width"]

        app.processor.update_processing_schedule(1)
        app.processor.wait_till_finished()

        df: pd.DataFrame = app.repository.read_output(1)

        assert len(df) == 150
        assert list(df.columns) == ["variety", "petal.width"]


def test_groupby_agg():
    app = initalize_app()
    with app.controller.test_client() as client:
        response = client.put("/nodeInstances/2/kwargs/group_colnames", data=b"variety")
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.put(
            "/nodeInstances/2/kwargs/agg_dict",
            data=b"petal.length:mean,petal.width:max",
        )
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.get("/queueProcessing")
    app.processor.update_processing_schedule(2)
    app.processor.wait_till_finished()

    df: pd.DataFrame = app.repository.read_output(2)
    assert len(df) == 3
    assert list(df.columns) == ["variety", "petal.length", "petal.width"]


def test_filter_by_value_eq():
    app = initalize_app()

    with app.controller.test_client() as client:
        response = client.put("/nodeInstances/3/kwargs/colname", data=b"variety")
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.put("/nodeInstances/3/kwargs/value", data=b"Setosa")
        assert response.data == b"OK"
        assert response.status_code == 200

    app.processor.update_processing_schedule(3)
    app.processor.wait_till_finished()

    df: pd.DataFrame = app.repository.read_output(3)
    assert all(df["variety"] == "Setosa")
    assert len(df) == 50


def test_filter_by_value_less_than():
    app = initalize_app()

    with app.controller.test_client() as client:
        response = client.put("/nodeInstances/3/kwargs/colname", data=b"sepal.length")
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.put("/nodeInstances/3/kwargs/value", data=b"5")
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.put("/nodeInstances/3/kwargs/condition", data=b"less_than")
        assert response.data == b"OK"
        assert response.status_code == 200

    app.processor.update_processing_schedule(3)
    app.processor.wait_till_finished()

    df: pd.DataFrame = app.repository.read_output(3)
    assert len(df) == 22
    assert df["sepal.length"].min() < 5
