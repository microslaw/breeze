from flask import Flask
from importlib import reload
import backend.prefabs.testing.default
from backend import NodeType
from backend import Repository
from backend import Processor
from backend import Controller


def initialize_server() -> Controller:
    repository = Repository()
    processor = Processor(repository)
    controller = Controller(repository, processor)

    NodeType.clear_udns()
    reload(backend.prefabs.testing.default)
    repository.load_workflow("backend/tests/workflows/default")

    return controller


def test_get_all_node_types():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.get("/nodeTypes")

        assert response.json == ["add_int", "remove_outliers"]
        assert response.status_code == 200


def test_get_node_type():
    controller = initialize_server()

    with controller.test_client() as client:

        response = client.get("/nodeTypes/add_int")
        assert response.json == {
            "name": "add_int",
            "arg_names": ["a", "b"],
            "arg_types": {"b": "int"},
            "return_type": "int",
            "default_args": {},
            "tags": ["testing"],
        }
        assert response.status_code == 200

        response = client.get("/nodeTypes/nonexistent_func")
        assert response.data == b"Node type nonexistent_func not found"
        assert response.status_code == 404


def test_get_undecorated_node_type():
    controller = initialize_server()

    @NodeType
    def multiply_int(x):
        return x * 2

    with controller.test_client() as client:

        response = client.get("/nodeTypes/multiply_int")
        assert response.json == {
            "name": "multiply_int",
            "arg_types": {},
            "arg_names": ["x"],
            "default_args": {},
            "return_type": None,
            "tags": [],
        }
        assert response.status_code == 200

        response = client.get("/nodeTypes/nonexistent_func")
        assert response.data == b"Node type nonexistent_func not found"
        assert response.status_code == 404


def test_get_all_node_instances():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.get("/nodeInstances")

    assert response.json == [
        {
            "node_id": 0,
            "node_type": "add_int",
            "position_x" : 100,
            "position_y" : 100,
            "overwrite_kwargs": {},
        },
        {
            "node_id": 1,
            "node_type": "add_int",
            "position_x" : 100,
            "position_y" : 300,
            "overwrite_kwargs": {},
        },
        {
            "node_id": 2,
            "node_type": "add_int",
            "position_x" : 400,
            "position_y" : 200,
            "overwrite_kwargs": {},
        },
        {
            "node_id": 3,
            "node_type": "remove_outliers",
            "position_x" : 700,
            "position_y" : 200,
            "overwrite_kwargs": {},
        },
    ]
    assert response.status_code == 200


def test_get_node_instance():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.get("/nodeInstances/0")

        assert response.json == {
            "node_id": 0,
            "node_type": "add_int",
            "position_x" : 100,
            "position_y" : 100,
            "overwrite_kwargs": {},
        }
        assert response.status_code == 200


def test_get_missing_node_instance():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.get("/nodeInstances/10")

        assert response.data == b"Node instance with node_id=10 not found"
        assert response.status_code == 404


def test_create_node_instance():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.post(
            "/nodeInstances",
            json={
                "node_type": "add_int",
                "position_x" : 100,
                "position_y" : 100
            },
        )
        assert response.json == {"node_id": 4}
        assert response.status_code == 200

        response = client.get("/nodeInstances")
        assert response.json == [
            {
                "node_id": 0,
                "node_type": "add_int",
                "position_x" : 100,
                "position_y" : 100,
                "overwrite_kwargs": {},
            },
            {
                "node_id": 1,
                "node_type": "add_int",
                "position_x" : 100,
                "position_y" : 300,
                "overwrite_kwargs": {},
            },
            {
                "node_id": 2,
                "node_type": "add_int",
                "position_x" : 400,
                "position_y" : 200,
                "overwrite_kwargs": {},
            },
            {
                "node_id": 3,
                "node_type": "remove_outliers",
                "position_x" : 700,
                "position_y" : 200,
                "overwrite_kwargs": {},
            },
            {
                "node_id": 4,
                "node_type": "add_int",
                "position_x" : 100,
                "position_y" : 100,
                "overwrite_kwargs": {},
            },
        ]
        assert response.status_code == 200


def test_delete_node_instance():
    controller = initialize_server()

    with controller.test_client() as client:

        response = client.delete("/nodeInstances/2")
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.get("/nodeInstances")
        assert response.json == [
            {
                "node_id": 0,
                "node_type": "add_int",
                "position_x" : 100,
                "position_y" : 100,
                "overwrite_kwargs": {},
            },
            {
                "node_id": 1,
                "node_type": "add_int",
                "position_x" : 100,
                "position_y" : 300,
                "overwrite_kwargs": {},
            },
            {
                "node_id": 3,
                "node_type": "remove_outliers",
                "position_x" : 700,
                "position_y" : 200,
                "overwrite_kwargs": {},
            },
        ]
        assert response.status_code == 200

        response = client.get("/nodeLinks")
        assert response.json == []


def test_get_all_node_links():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.get("/nodeLinks")
        assert response.json == [
            {
                "destination_node_id": 2,
                "destination_node_input": "a",
                "origin_node_id": 0,
                "origin_node_output": None,
            },
            {
                "destination_node_id": 2,
                "destination_node_input": "b",
                "origin_node_id": 1,
                "origin_node_output": None,
            },
            {
                "destination_node_id": 3,
                "destination_node_input": "sd_limit",
                "origin_node_id": 2,
                "origin_node_output": None,
            },
        ]


def test_get_node_link():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.get("/nodeLinks/0")
        assert response.json == [
            {
                "origin_node_id": 0,
                "destination_node_input": "a",
                "destination_node_id": 2,
                "origin_node_output": None,
            }
        ]
        assert response.status_code == 200


def test_get_missing_node_link():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.get("/nodeLinks/10")
        assert response.data == b"Node instance with node_id=10 not found"
        assert response.status_code == 404


def test_create_node_link():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.post(
            "/nodeLinks",
            json={
                "origin_node_id": 0,
                "origin_node_output": None,
                "destination_node_id": 3,
                "destination_node_input": "a",
            },
        )
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.get("nodeLinks/0")
        assert response.json == [
            {
                "origin_node_id": 0,
                "origin_node_output": None,
                "destination_node_id": 2,
                "destination_node_input": "a",
            },
            {
                "origin_node_id": 0,
                "origin_node_output": None,
                "destination_node_id": 3,
                "destination_node_input": "a",
            },
        ]
        assert response.status_code == 200


def test_delete_node_link():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.delete(
            "/nodeLinks",
            json={
                "origin_node_id": 1,
                "origin_node_output": None,
                "destination_node_id": 2,
                "destination_node_input": "b",
            },
        )
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.get("/nodeLinks/1")
        assert response.json == []
        assert response.status_code == 200
