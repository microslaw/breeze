from backend.controller import create_api_server
from flask import Flask
import backend.repository as repository
from importlib import reload
import backend.tests.default
from backend import NodeType

def initialize_server() -> Flask:
    api_server = create_api_server()

    NodeType.clear_udns()
    reload(backend.tests.default)

    repository.init_db()
    repository.from_csv("backend/tests/default/nodeInstances.csv", "nodeInstances")
    repository.from_csv("backend/tests/default/nodeLinks.csv", "nodeLinks")


    return api_server

    # for some reason server is already running before this command
    # api_server.run('0.0.0.0', 5000, threaded=True)


def test_all_node_types():
    api_server = initialize_server()

    with api_server.test_client() as client:
        response = client.get("/nodeTypes")

        assert response.json == ["add_int", "remove_outliers"]
        assert response.status_code == 200


def test_node_type():
    api_server = initialize_server()

    with api_server.test_client() as client:

        response = client.get("/nodeTypes/add_int")
        assert response.json == {
            "name": "add_int",
            "arg_names": ["a", "b"],
            "arg_types": {"b": "int"},
            "return_type": "int",
        }
        assert response.status_code == 200

        response = client.get("/nodeTypes/nonexistent_func")
        assert response.data == b"Node type nonexistent_func not found"
        assert response.status_code == 404


def test_all_node_instances():
    api_server = initialize_server()

    with api_server.test_client() as client:
        response = client.get("/nodeInstances")

        assert response.json == [0, 1, 2, 3]
        assert response.status_code == 200


def test_create_node_instance():
    api_server = initialize_server()

    with api_server.test_client() as client:
        response = client.post(
            "/nodeInstances",
            json={
                "node_type": "add_int",
            },
        )
        assert response.json == {"node_id": 4}
        assert response.status_code == 200

        response = client.get("/nodeInstances")
        assert response.json == [0, 1, 2, 3, 4]
        assert response.status_code == 200


def test_delete_node_instance():
    api_server = initialize_server()

    with api_server.test_client() as client:

        response = client.delete("/nodeInstances/0")
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.get("/nodeInstances")
        assert response.json == [1, 2, 3]
        assert response.status_code == 200


def test_get_node_link():
    api_server = initialize_server()

    with api_server.test_client() as client:
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


def test_create_node_link():
    api_server = initialize_server()

    with api_server.test_client() as client:
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
    api_server = initialize_server()

    with api_server.test_client() as client:
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
