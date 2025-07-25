from backend.datatypes import NodeInstance
from backend.repository import Repository
from backend.formatting import format_for_display
from collections import deque
import threading
import traceback
from typing import Optional


class Processor:
    def __init__(self, repository: Repository):
        self.processing_queue: deque[int] = deque()
        self.repository = repository
        self.running = False
        self.cached_exception = None
        self.processing_daemon = None

    def get_all_prerequisite_node_ids(self, node_id: int) -> list[int]:
        queue_appendix: list[int] = []
        to_add = [node_id]

        while len(to_add) > 0:
            node_id = to_add.pop()
            required_node_ids = self.repository.get_prerequisite_node_ids(node_id)

            required_unprocessed_node_ids = [
                node_id
                for node_id in required_node_ids
                if not self.repository.does_output_exist(node_id)
            ]
            to_add.extend(required_unprocessed_node_ids)
            queue_appendix.append(node_id)
        queue_appendix.reverse()

        return queue_appendix

    def get_processing_schedule(self) -> list[int]:
        if self.cached_exception is None:
            return list(self.processing_queue)
        else:
            raise self.cached_exception from self.cached_exception.cause

    def update_processing_schedule(
        self, node_id: int, start_processing: bool = True
    ) -> None:
        queue_appendix = self.get_all_prerequisite_node_ids(node_id)

        for item in queue_appendix:
            if item not in self.processing_queue:
                self.processing_queue.append(item)

        if start_processing:
            self.start_processing()

    def start_processing(self):
        self.running = True
        self.processing_daemon = threading.Thread(
            target=self.processing_daemon_loop, daemon=True
        )
        self.processing_daemon.start()

    def processing_daemon_loop(self):
        while self.running and len(self.processing_queue) > 0:
            node_id = self.processing_queue.popleft()
            self.process(node_id)
        self.processing_daemon = None

    def stop_processing_daemon(self):
        self.running = False

    def reset_processing_queue(self) -> None:
        self.processing_queue = deque()
        self.cached_exception = None

    def wait_till_finished(self, timeout: Optional[float] = None):
        if self.processing_daemon is None:
            return

        self.processing_daemon.join(timeout)

    def combine_kwargs(
        self,
        default_kwargs: dict[str, object],
        overwrite_kwargs: dict[str, object],
        prerequisite_kwargs: dict[str, object],
    ) -> dict[str, object]:
        return default_kwargs | overwrite_kwargs | prerequisite_kwargs

    def get_kwargs_details(self, processed_node_instance: NodeInstance):
        """
        Similar get_kwargs, but provides more detail for frontend display
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
            if self.repository.does_output_exist(
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
        processed_node_instance = self.repository.get_node_instance(node_id)
        processed_node_type = self.repository.get_node_type_from_name(
            processed_node_instance.node_type_name
        )

        kwargs = self.get_kwargs(processed_node_instance)

        try:
            output = processed_node_type(**kwargs)
            self.repository.write_output(output, node_id)
        except Exception as e:
            self.stop_processing_daemon()
            self.cached_exception = ProcessingException(
                e,
                processed_node_instance,
                traceback.format_exception(e),
                kwargs,
                list(self.processing_queue),
            )


class ProcessingException(Exception):
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
        """

        pruned_traceback = traceback[0]
        pruned_traceback += "".join(trace_file for trace_file in traceback[3:])

        return pruned_traceback

    def toJson(self) -> dict[str, object]:
        return {
            "origin": self.origin.toNameDict(),
            "traceback_str": self.traceback_str,
            "cancelled_nodes": self.cancelled_nodes,
            "input_args": {
                name: format_for_display(value)
                for name, value in self.input_args.items()
            },
        }
