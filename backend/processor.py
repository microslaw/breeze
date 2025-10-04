from backend.datatypes import NodeInstance
from backend.repository import Repository
from backend.formatting import format_for_display
from collections import deque
import threading
import traceback
from typing import Optional
from enum import Enum
import queue


class Processor:
    """
    Simple task scheduler
    Starts a processing_daemon when there are some tasks to do
    """

    def __init__(self, repository: Repository):
        self.processing_queue: deque[int] = deque()
        self.repository = repository
        self.running = False
        self.message_queue = queue.Queue()
        self.processing_daemon = None

    def get_all_prerequisite_node_ids(self, node_id: int) -> list[int]:
        """
        Returns ids of nodes that have to be processed to provide arguments
        for node with specified node_id

        :param node_id: ID of the node to check prerequisites for
        :return: List of node_id of prerequesite nodes.
        """
        queue_appendix: list[int] = []
        to_add = [node_id]

        while len(to_add) > 0:
            node_id = to_add.pop()
            required_node_ids = self.repository.get_prerequisite_node_ids(node_id)

            required_unprocessed_node_ids = [
                node_id
                for node_id in required_node_ids
                if not self.repository.is_output_created(node_id)
            ]
            to_add.extend(required_unprocessed_node_ids)
            queue_appendix.append(node_id)
        queue_appendix.reverse()

        return queue_appendix

    def get_processing_schedule(self) -> list[int]:
        """
        Returns processing queue

        :return: nodes left to process
        """
        return list(self.processing_queue)

    def update_processing_schedule(
        self, node_id: int, start_processing: bool = True
    ) -> None:
        """
        Appends node_id and it's prerequisite nodes to processing schedule.

        :param node_id: DataFrame containing the data to plot.
        :param start_processing: if true will start processing;
        """
        queue_appendix = self.get_all_prerequisite_node_ids(node_id)

        for item in queue_appendix:
            if item not in self.processing_queue:
                self.processing_queue.append(item)

        if start_processing:
            self.start_processing()

    def run_all(self, start_processing: bool = True):
        to_process = self.repository.get_all_final_node_ids()

        for node_id in to_process:
            self.update_processing_schedule(node_id, start_processing=False)

        if start_processing:
            self.start_processing()

    def start_processing(self):
        """
        Begins processing of nodes specified inprocessing_queue.
        Creates a separate thread that processes nodes one by one
        """
        if not self.running:
            self.running = True
            self.processing_daemon = threading.Thread(
                target=self.processing_daemon_loop, daemon=True
            )
            self.processing_daemon.start()

    def processing_daemon_loop(self):
        """
        Intended to be used within a separate thread.
        Will keep processing nodes from processing queue untill they run out
        or untill it is stopped by swiching self.running to False.
        When stopped, will try to finish currently processed node
        """
        while self.running and len(self.processing_queue) > 0:
            node_id = self.processing_queue.popleft()
            self.process(node_id)
        self.processing_daemon = None
        self.running = False

    def stop_processing_daemon(self):
        """
        Halts node processing daemon
        """
        self.running = False

    def reset_processing_queue(self) -> None:
        """
        Clears processing queue, along with any exceptions that occured
        during processing
        """
        self.processing_queue = deque()

    def wait_till_finished(self, timeout: Optional[float] = None):
        """
        Won't return untill node processing is finished.
        Intended for debugging

        :param timeout: maximum time to wait in seconds
        """
        if self.processing_daemon is None:
            return

        self.processing_daemon.join(timeout)

    def combine_kwargs(
        self,
        default_kwargs: dict[str, object],
        overwrite_kwargs: dict[str, object],
        prerequisite_kwargs: dict[str, object],
    ) -> dict[str, object]:
        """
        Specifies priorities of different kwargs and how they are combined

        :param default_kwargs: kwargs that are default for the node type and are specified in node type definition
        :param overwrite_kwargs: kwargs that are specified by user to overwrite default kwargs
        :param prerequisite_kwargs: kwargs that are provided by prerequisite nodes

        :return: combined kwargs
        """
        return default_kwargs | overwrite_kwargs | prerequisite_kwargs

    def get_kwargs_details(self, processed_node_instance: NodeInstance):
        """
        Similar to get_kwargs, but provides more detail for frontend display

        :param processed_node_instance: node instance to get kwargs for
        :return: detailed kwargs
        """
        processed_node_type = self.repository.get_node_type_from_name(
            processed_node_instance.node_type_name
        )
        prerequisite_links = self.repository.get_links_by_destination_node_id(
            processed_node_instance.node_id
        )

        default_kwargs = {
            arg_name: None for arg_name in processed_node_type.get_arg_names()
        } | processed_node_type.get_default_args()

        overwrite_kwargs = processed_node_instance.overwrite_kwargs

        prerequisite_kwargs = {
            link.destination_node_input: self.repository.read_output(
                link.origin_node_id, link.origin_node_output
            )
            for link in prerequisite_links
            if self.repository.is_output_created(
                link.origin_node_id, link.origin_node_output
            )
        }

        default_kwarg_types = processed_node_type.get_arg_types()

        default_kwargs: dict[str, object] = {
            arg_name: {
                "value": value,
                "arg_source": "default",
                "datatype": default_kwarg_types.get(arg_name, type(None)),
            }
            for arg_name, value in default_kwargs.items()
        }
        overwrite_kwargs: dict[str, object] = {
            arg_name: {
                "value": value,
                "arg_source": "overwrite",
                "datatype": type(value),
            }
            for arg_name, value in overwrite_kwargs.items()
        }
        prerequisite_kwargs: dict[str, object] = {
            arg_name: {
                "value": value,
                "arg_source": "prerequisite",
                "datatype": type(value),
            }
            for arg_name, value in prerequisite_kwargs.items()
        }

        return self.combine_kwargs(
            default_kwargs, overwrite_kwargs, prerequisite_kwargs
        )

    def get_kwargs(self, processed_node_instance: NodeInstance):
        """
        Returns all available kwargs that are needed to process processed_node_instances

        :param processed_node_instance: node instance to get kwargs for
        :return: kwargs needed to process the node instance
        """
        prerequisite_links = self.repository.get_links_by_destination_node_id(
            processed_node_instance.node_id
        )
        prerequisite_kwargs = {
            link.destination_node_input: self.repository.read_output(
                link.origin_node_id, link.origin_node_output
            )
            for link in prerequisite_links
        }

        processed_node_type = self.repository.get_node_type_from_name(
            processed_node_instance.node_type_name
        )
        default_kwargs = processed_node_type.get_default_args()

        overwrite_kwargs = processed_node_instance.overwrite_kwargs

        return self.combine_kwargs(
            default_kwargs, overwrite_kwargs, prerequisite_kwargs
        )

    def process(self, node_id: int):
        """
        Processes individual nodes. If exception occurs during processing, will cache it till
        reset_processing queue is called

        :param node_id: ID of the node to process
        """
        processed_node_instance = self.repository.get_node_instance(node_id)
        processed_node_type = self.repository.get_node_type_from_name(
            processed_node_instance.node_type_name
        )

        kwargs = self.get_kwargs(processed_node_instance)

        try:
            output = processed_node_type(**kwargs)
            self.repository.write_output(output, node_id)

            self.message_queue.put(
                {
                    "type": SseMessageTypes.finished_processing.value,
                    "content": {
                        "node_id": node_id,
                        "processing_queue": self.get_processing_schedule(),
                    },
                },
            )

        except Exception as e:
            self.stop_processing_daemon()

            exception = ProcessingException(
                e,
                processed_node_instance,
                traceback.format_exception(e),
                kwargs,
                list(self.processing_queue),
            )

            self.message_queue.put(
                {
                    "type": SseMessageTypes.processing_error.value,
                    "content": exception.toJson(),
                }
            )


class SseMessageTypes(Enum):
    processing_error = "processing_error"
    finished_processing = "finished_processing"


class ProcessingException(Exception):
    """
    Wrapper for exceptions that occur during node processing
    """

    def __init__(
        self,
        e: Exception,
        node_instance: NodeInstance,
        traceback: list[str],
        input_args: dict[str, object],
        cancelled_nodes: list[int],
    ):
        self.cause = e
        self.origin: NodeInstance = node_instance
        self.input_args = input_args
        self.traceback_str = ProcessingException.prune_traceback(traceback)
        self.cancelled_nodes = cancelled_nodes

        super().__init__(
            f"During processing of node {node_instance.toNameDict()} an exception occured:\n\n{self.traceback_str}"
        )

    @staticmethod
    def prune_traceback(traceback: list[str]) -> str:
        """
        Removes part of the trace caused by the breeze library

        :param traceback: full traceback as returned by traceback.format_exception
        :return: pruned traceback as a string
        """

        pruned_traceback = traceback[0]
        pruned_traceback += "".join(trace_file for trace_file in traceback[3:])

        return pruned_traceback

    def toJson(self) -> dict[str, object]:
        """
        Creates a JSON representation that can be serialized and sent to frontend

        :return: JSON representation of the exception
        """
        return {
            "origin": self.origin.toNameDict(),
            "traceback_str": self.traceback_str,
            "cancelled_nodes": self.cancelled_nodes,
            "input_args": {
                name: format_for_display(value)
                for name, value in self.input_args.items()
            },
        }
