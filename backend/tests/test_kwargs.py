from backend.datatypes import NodeType
from importlib import reload
from backend import BreezeApp
import backend.tests.kwargs.nodeTypes
import threading
import time
from flask import Flask


def initalize_app() -> BreezeApp:
    app = BreezeApp()

    NodeType.clear_udns()
    reload(backend.tests.kwargs.nodeTypes)

    app.repository.from_csv("backend/tests/kwargs/nodeInstances.csv", "nodeInstances")
    app.repository.from_csv("backend/tests/kwargs/nodeLinks.csv", "nodeLinks")

    return app


def test_initialization():
    app = initalize_app()
    assert app.repository.get_all_node_types() == [
        "add_float",
        "round_float",
        "describe_myclass",
    ]


def test_get_default_arg():
    app = initalize_app()

    with app.controller.test_client() as client:
        response = client.get("/nodeTypes/round_float")

        assert response.json == {
            "arg_names": [
                "to_round",
                "digits",
            ],
            "arg_types": {
                "digits": "int",
                "to_round": "float",
            },
            "default_args": {"digits": "2"},
            "name": "round_float",
            "return_type": None,
        }
        assert response.status_code == 200


def test_put_kwarg():
    app = initalize_app()

    with app.controller.test_client() as client:
        response = client.put("/nodeInstances/0/kwargs/a", data=b"3.1415")

        assert response.status_code == 200
        assert response.data == b"OK"

        response = client.get("/nodeInstances/0")

        assert response.status_code == 200
        assert response.json == {
            "node_id": 0,
            "node_type": "add_float",
            "overwrite_kwargs": {"a": "3.1415"},
        }


def test_put_overwriting_kwarg():
    app = initalize_app()

    with app.controller.test_client() as client:
        response = client.put("/nodeInstances/2/kwargs/digits", data=b"1")

        assert response.status_code == 200
        assert response.data == b"OK"

        response = client.get("/nodeInstances/2")

        assert app.repository.read_kwarg(2, "digits") == 1

        assert response.status_code == 200
        assert response.json == {
            "node_id": 2,
            "node_type": "round_float",
            "overwrite_kwargs": {
                "digits": "1",
            },
        }


def test_put_missing_kwargname():
    app = initalize_app()

    with app.controller.test_client() as client:
        response = client.put("/nodeInstances/2/kwargs/missing", data=b"1")

        assert response.status_code == 404
        assert (
            response.data
            == b'Nodes of type_name= "round_float" do not have any argument with kwarg_name="missing"'
        )


def test_put_kwargname_missing_node():
    app = initalize_app()

    with app.controller.test_client() as client:
        response = client.put("/nodeInstances/100/kwargs/digits", data=b"1")

        assert response.status_code == 404
        assert response.data == b"Node instance with node_id=100 not found"


def test_get_kwargs_overwriting_only():
    app = initalize_app()

    with app.controller.test_client() as client:
        app.repository.write_kwarg(1.0, 0, "a")
        app.repository.write_kwarg(2.0, 0, "b")

        kwargs = app.processor.get_kwargs(app.repository.get_node_instance(0))

        assert kwargs == {"a": 1.0, "b": 2.0}


def test_kwarg_prerequisite_overwriting():
    app = initalize_app()

    app.repository.write_output(1.0, 0)
    app.repository.write_kwarg(2.0, 1, "a")
    app.repository.write_kwarg(4.0, 1, "b")

    kwargs = app.processor.get_kwargs(app.repository.get_node_instance(1))
    assert kwargs == {"a": 1.0, "b": 4.0}


def test_kwarg_overwriting_default():
    app = initalize_app()

    app.repository.write_output(3.1415, 1)
    app.repository.write_kwarg(1, 2, "digits")

    kwargs = app.processor.get_kwargs(app.repository.get_node_instance(2))

    assert kwargs == {"to_round": 3.1415, "digits": 1}


def test_processing_overwriting_default():
    app = initalize_app()

    app.repository.write_output(3.1415, 1)
    app.repository.write_kwarg(1, 2, "digits")

    app.processor.update_processing_schedule(2)
    app.processor.wait_till_finished(0.05)

    assert app.repository.read_output(2) == 3.1


def test_kwargs_processing():
    app = initalize_app()

    app.repository.write_kwarg(1.0, 0, "a")
    app.repository.write_kwarg(2.0, 0, "b")

    app.processor.update_processing_schedule(0)
    app.processor.wait_till_finished(0.05)

    output = app.repository.read_output(0)
    assert output == 3.0
    assert type(output) == type(3.0)


def test_custom_format_from_input():
    app = initalize_app()

    with app.controller.test_client() as client:
        response = client.put("/nodeInstances/3/kwargs/instance", data=b"name")
        assert response.status_code == 200
        assert response.data == b"OK"


    assert app.repository.does_kwarg_exist(node_id=3, kwarg_name="instance")
    instance = app.repository.read_kwarg(parent_node_id=3, kwarg_name="instance")
    assert instance.describe() == backend.tests.kwargs.nodeTypes.MyClass("name").describe()
