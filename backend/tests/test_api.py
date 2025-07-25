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
            "position_x": 100,
            "position_y": 100,
            "overwrite_kwargs": {},
            "instance_name": "n0",
        },
        {
            "node_id": 1,
            "node_type": "add_int",
            "position_x": 100,
            "position_y": 300,
            "overwrite_kwargs": {},
            "instance_name": "n1",
        },
        {
            "node_id": 2,
            "node_type": "add_int",
            "position_x": 400,
            "position_y": 200,
            "overwrite_kwargs": {},
            "instance_name": "n2",
        },
        {
            "node_id": 3,
            "node_type": "remove_outliers",
            "position_x": 700,
            "position_y": 200,
            "overwrite_kwargs": {},
            "instance_name": "n3",
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
            "position_x": 100,
            "position_y": 100,
            "overwrite_kwargs": {},
            "instance_name": "n0",
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
            json={"node_type": "add_int", "position_x": 100, "position_y": 100},
        )
        assert response.json == {"node_id": 4}
        assert response.status_code == 200

        response = client.get("/nodeInstances")
        assert response.json == [
            {
                "node_id": 0,
                "node_type": "add_int",
                "position_x": 100,
                "position_y": 100,
                "overwrite_kwargs": {},
                "instance_name": "n0",
            },
            {
                "node_id": 1,
                "node_type": "add_int",
                "position_x": 100,
                "position_y": 300,
                "overwrite_kwargs": {},
                "instance_name": "n1",
            },
            {
                "node_id": 2,
                "node_type": "add_int",
                "position_x": 400,
                "position_y": 200,
                "overwrite_kwargs": {},
                "instance_name": "n2",
            },
            {
                "node_id": 3,
                "node_type": "remove_outliers",
                "position_x": 700,
                "position_y": 200,
                "overwrite_kwargs": {},
                "instance_name": "n3",
            },
            {
                "node_id": 4,
                "node_type": "add_int",
                "position_x": 100,
                "position_y": 100,
                "overwrite_kwargs": {},
                "instance_name": None,
            },
        ]
        assert response.status_code == 200


def test_update_node_instance():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.patch(
            "/nodeInstances/0",
            json={
                "instance_name": "a1",
                "position_x": 101,
                "position_y": 150,
            },
        )
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.get("nodeInstances/0")
        assert response.json == {
            "instance_name": "a1",
            "node_id": 0,
            "node_type": "add_int",
            "overwrite_kwargs": {},
            "position_x": 101,
            "position_y": 150,
        }
        assert response.status_code == 200


def test_invalid_args_update_node_instance():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.patch(
            "/nodeInstances/0",
            json={
                "node_id": 0,
            },
        )
        assert response.data == b"Field node_id cannot be patched"
        assert response.status_code == 400


def test_invalid_instance_update_node_instance():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.get("nodeInstances/10")
        assert response.data == b"Node instance with node_id=10 not found"
        assert response.status_code == 404


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
                "position_x": 100,
                "position_y": 100,
                "overwrite_kwargs": {},
                "instance_name": "n0",
            },
            {
                "node_id": 1,
                "node_type": "add_int",
                "position_x": 100,
                "position_y": 300,
                "overwrite_kwargs": {},
                "instance_name": "n1",
            },
            {
                "node_id": 3,
                "node_type": "remove_outliers",
                "position_x": 700,
                "position_y": 200,
                "overwrite_kwargs": {},
                "instance_name": "n3",
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
                "node_link_id": 0,
                "origin_node_id": 0,
                "origin_node_output": None,
            },
            {
                "destination_node_id": 2,
                "destination_node_input": "b",
                "node_link_id": 1,
                "origin_node_id": 1,
                "origin_node_output": None,
            },
            {
                "destination_node_id": 3,
                "destination_node_input": "sd_limit",
                "node_link_id": 2,
                "origin_node_id": 2,
                "origin_node_output": None,
            },
        ]


def test_get_node_link():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.get("/nodeLinks/0")
        assert response.json == {
            "origin_node_id": 0,
            "destination_node_input": "a",
            "node_link_id": 0,
            "destination_node_id": 2,
            "origin_node_output": None,
        }

        assert response.status_code == 200


def test_get_missing_node_link():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.get("/nodeLinks/10")
        assert response.data == b"Node link with node_link_id=10 not found"
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
        assert response.json == {"node_link_id": 3}
        assert response.status_code == 200

        response = client.get("nodeLinks/3")
        assert response.json == {
            "origin_node_id": 0,
            "origin_node_output": None,
            "node_link_id": 3,
            "destination_node_id": 3,
            "destination_node_input": "a",
        }
        assert response.status_code == 200


def test_update_node_link():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.patch(
            "/nodeLinks/0",
            json={
                "destination_node_id": 3,
                "destination_node_input": "b",
                "origin_node_id": 0,
            },
        )
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.get("nodeLinks/0")
        assert response.json == {
            "origin_node_id": 0,
            "origin_node_output": None,
            "node_link_id": 0,
            "destination_node_id": 3,
            "destination_node_input": "b",
        }
        assert response.status_code == 200


def test_invalid_args_update_node_links():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.patch(
            "/nodeLinks/0",
            json={
                "node_link_id": 0,
            },
        )
        assert response.data == b"Field node_link_id cannot be patched"
        assert response.status_code == 400


def test_invalid_link_update_node_links():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.get("nodeLinks/10")
        assert response.data == b"Node link with node_link_id=10 not found"
        assert response.status_code == 404


def test_delete_node_link():
    controller = initialize_server()
    with controller.test_client() as client:
        response = client.delete("/nodeLinks/1")
        assert response.data == b"OK"
        assert response.status_code == 200

        response = client.get("/nodeLinks/1")
        assert response.data == b"Node link with node_link_id=1 not found"
        assert response.status_code == 404


def test_get_node_links_filtered_by_origin():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.get("/nodeLinks?origin_node_id=0")
        assert response.json == [
            {
                "destination_node_id": 2,
                "destination_node_input": "a",
                "node_link_id": 0,
                "origin_node_id": 0,
                "origin_node_output": None,
            },
        ]


def test_get_node_links_filtered_by_destination():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.get("/nodeLinks?destination_node_id=2")
        assert response.json == [
            {
                "destination_node_id": 2,
                "destination_node_input": "a",
                "node_link_id": 0,
                "origin_node_id": 0,
                "origin_node_output": None,
            },
            {
                "destination_node_id": 2,
                "destination_node_input": "b",
                "node_link_id": 1,
                "origin_node_id": 1,
                "origin_node_output": None,
            },
        ]


def test_get_node_links_filtered_by_origin_and_destination():
    controller = initialize_server()

    with controller.test_client() as client:
        response = client.get("/nodeLinks?origin_node_id=2&destination_node_id=3")
        assert response.json == [
            {
                "destination_node_id": 3,
                "destination_node_input": "sd_limit",
                "node_link_id": 2,
                "origin_node_id": 2,
                "origin_node_output": None,
            },
        ]
