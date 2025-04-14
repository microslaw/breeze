from backend.datatypes import NodeType
from importlib import reload
from backend import Repository
from backend import Processor, ProcessingException
from backend import create_api_server
import backend.tests.processing
import backend.tests.processing.nodeTypes
import threading
import time
from flask import Flask


def initialize_processor() -> Processor:
    repository = Repository()
    processor = Processor(repository)

    NodeType.clear_udns()
    reload(backend.tests.processing.nodeTypes)

    repository.from_csv("backend/tests/processing/nodeInstances.csv", "nodeInstances")
    repository.from_csv("backend/tests/processing/nodeLinks.csv", "nodeLinks")

    return processor


def initalize_api_server() -> tuple[Flask, Processor]:
    processor = initialize_processor()
    api_server = create_api_server(processor.repository, processor)
    return api_server, processor


def test_initialization():
    processor = initialize_processor()
    assert processor.repository.get_all_node_types() == [
        "add_int",
        "const_1",
        "const_2",
        "const_a",
        "create_my_class",
    ]


def test_closing_threads():
    processor = initialize_processor()

    processor.update_processing_schedule(4)
    # join thread
    processor.wait_till_finished()

    assert threading.active_count() == 1


def test_self_closing_threads():
    processor = initialize_processor()

    processor.update_processing_schedule(0)
    # after finishing processign thread should close itself

    time.sleep(0.05)

    assert threading.active_count() == 1


def test_processing_results():
    processor = initialize_processor()
    processor.update_processing_schedule(0)
    processor.wait_till_finished()
    assert processor.repository.read_object(0) == 1


def test_processing_scheduling():
    processor = initialize_processor()
    assert processor.get_all_required_node_ids(4) == [0, 1, 2, 3, 4]


# Processor-reliant api tests


def test_check_processing_queue():
    api_server, processor = initalize_api_server()
    processor.update_processing_schedule(4, start_processing=False)

    with api_server.test_client() as client:
        response = client.get("/queueProcessing")

        assert response.json == [0, 1, 2, 3, 4]
        assert response.status_code == 200


def test_processing_exception():
    api_server, processor = initalize_api_server()

    with api_server.test_client() as client:
        client.post(
            "/queueProcessing",
            json={"node_id": 8},
        )
        processor.wait_till_finished()

        response = client.get("/queueProcessing")

        assert response.json == {
            "cancelled_nodes": [8],
            "input_args": {
                "a": "1",
                "b": "a",
            },
            "origin": {
                "node_id": 7,
                "node_type": "add_int",
            },
            "traceback_str": "Traceback (most recent call last):\n"
            f'  File "{backend.tests.processing.nodeTypes.__file__}", '
            f"line {backend.tests.processing.nodeTypes.add_int.func.__code__.co_firstlineno + 2}, in add_int\n"
            "    return a + b\n"
            "           ~~^~~\n"
            "TypeError: unsupported operand type(s) for +: 'int' and 'str'\n",
        }
        assert response.status_code == 422


def test_get_processing_result():
    api_server, processor = initalize_api_server()

    with api_server.test_client() as client:
        client.post(
            "/queueProcessing",
            json={"node_id": 4},
        )
        processor.wait_till_finished()

        response = client.get("/processingResult/4")

        assert response.status_code == 200
        assert response.data == b"4"


def test_custom_format_for_display():
    api_server, processor = initalize_api_server()

    with api_server.test_client() as client:
        client.post(
            "/queueProcessing",
            json={"node_id": 9},
        )
        processor.wait_till_finished()

        response = client.get("/processingResult/9")

        assert response.status_code == 200
        assert response.data == b"MyClass named a class"
