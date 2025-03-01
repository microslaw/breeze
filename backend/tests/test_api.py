from backend.controller import create_api_server
from backend.datatypes import NodeInstance, NodeLink, NodeType
import pandas as pd
from flask import Flask, request
from pytest import fixture
import backend.repository as repository


def initialize_server() -> Flask:
    api_server = create_api_server()

    # this file creates a following workflow:
    # +--+
    # |n1|->\
    # +--+   \     +--+
    #         +--> |n3|->\
    # +--+   /     +--+   \   +--+
    # |n2|->/              \->|n4|
    # +--+                    +--+

    repository.init_db()
    repository.create_node_link(NodeLink(1, None, 3, "a"))
    repository.create_node_link(NodeLink(2, None, 3, "b"))
    repository.create_node_link(NodeLink(3, None, 4, "sd_limit"))

    repository.create_node_instance(NodeInstance(1, "add_int"))
    repository.create_node_instance(NodeInstance(2, "add_int"))
    repository.create_node_instance(NodeInstance(3, "add_int"))
    repository.create_node_instance(NodeInstance(4, "remove_outliers"))

    @NodeType
    def add_int(a, b: int) -> int:
        return a + b

    @NodeType
    def remove_outliers(
        df: pd.DataFrame, colname: str, sd_limit: float
    ) -> pd.DataFrame:
        df = df.copy()
        df["z_score"] = (df[colname] - df[colname].mean()) / df[colname].std()
        df = df[df["z_score"].abs() < sd_limit]
        return df

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

        assert response.json == [1, 2, 3, 4]
        assert response.status_code == 200


def test_create_node_instance():
    api_server = initialize_server()

    with api_server.test_client() as client:
        response = client.post(
            "/nodeInstances",
            json={
                "node_type": "add_int",
                "node_id": 5,
            },
        )
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.get("/nodeInstances")
        assert response.json == [1, 2, 3, 4, 5]
        assert response.status_code == 200


def test_delete_node_instance():
    api_server = initialize_server()

    with api_server.test_client() as client:

        response = client.delete("/nodeInstances/1")
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.get("/nodeInstances")
        assert response.json == [2, 3, 4]
        assert response.status_code == 200


def test_get_node_links():
    api_server = initialize_server()

    with api_server.test_client() as client:
        response = client.get("/nodeLinks/1")
        assert response.json == [
            {
                "origin_node_id": 1,
                "destination_node_input": "a",
                "destination_node_id": 3,
                "origin_node_output": "None",
            }
        ]
        assert response.status_code == 200


def test_create_node_link():
    api_server = initialize_server()

    with api_server.test_client() as client:
        response = client.post(
            "/nodeLinks",
            json={
                "origin_node_id": 1,
                "origin_node_output": None,
                "destination_node_id": 4,
                "destination_node_input": "a",
            },
        )
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.get("nodeLinks/1")
        assert response.json == [
            {
                "destination_node_id": 3,
                "destination_node_input": "a",
                "origin_node_id": 1,
                "origin_node_output": "None",
            },
            {
                "destination_node_id": 4,
                "destination_node_input": "a",
                "origin_node_id": 1,
                "origin_node_output": "None",
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
                "destination_node_id": 3,
                "destination_node_input": "a",
            },
        )
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.get("/nodeLinks/1")
        assert response.json == []
        assert response.status_code == 200
