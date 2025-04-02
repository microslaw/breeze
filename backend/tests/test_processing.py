from backend.datatypes import NodeType
from importlib import reload
from backend import Repository
from backend import Processor
import backend.tests.processing
import backend.tests.processing.nodeTypes
import threading
import time


def initialize_processor() -> Processor:
    repository = Repository()
    processor = Processor(repository)

    NodeType.clear_udns()
    reload(backend.tests.processing.nodeTypes)

    repository.from_csv("backend/tests/processing/nodeInstances.csv", "nodeInstances")
    repository.from_csv("backend/tests/processing/nodeLinks.csv", "nodeLinks")

    return processor


def test_initialization():
    processor = initialize_processor()
    assert processor.repository.get_all_node_types() == [
        "add_int",
        "const_1",
        "const_2",
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
