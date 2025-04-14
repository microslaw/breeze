from backend.datatypes import NodeInstance, NodeLink
from backend.repository import Repository
from backend.formatting import format_for_display
from collections import deque
import threading
import traceback


class Processor:

    def __init__(self, repository: Repository):
        self.processing_queue = deque()
        self.repository = repository
        self.running = False
        self.cached_exception = None

    def get_all_required_node_ids(self, node_id: str) -> list[int]:
        queue_appendix = []
        to_add = [node_id]

        while len(to_add) > 0:
            node_id = to_add.pop()
            required_node_ids = self.repository.get_prerequisite_node_ids(node_id)
            to_add.extend(required_node_ids)
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
        queue_appendix = self.get_all_required_node_ids(node_id)

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

    def wait_till_finished(self, timeout=None):
        if self.processing_daemon is None:
            return

        self.processing_daemon.join(None)

    def process(self, node_id):
        processed_node_instance = self.repository.get_node_instance(node_id)
        processed_node_type = self.repository.get_node_type(
            processed_node_instance.node_type
        )

        prerequisite_links = self.repository.get_links_by_destination_node_id(node_id)
        input_arg_to_producer_link_map = {
            link.destination_node_input: link for link in prerequisite_links
        }

        kwargs = {}
        for input_arg_name in processed_node_type.get_arg_names():
            input_arg_link: NodeLink = input_arg_to_producer_link_map[input_arg_name]

            kwargs[input_arg_name] = self.repository.read_object(
                input_arg_link.origin_node_id, input_arg_link.origin_node_output
            )

        try:
            output = processed_node_type(**kwargs)
            self.repository.write_object(output, node_id)
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
        traceback: str,
        input_args: dict[str, object],
        cancelled_nodes: list[int],
    ):
        self.cause = e
        self.origin: NodeInstance = node_instance
        self.input_args = input_args
        self.traceback_str = ProcessingException.prune_traceback(traceback)
        self.cancelled_nodes = cancelled_nodes

        super().__init__(
            f"During processing of node {node_instance.toJSON()} an exception occured:\n\n{self.traceback_str}"
        )

    def prune_traceback(traceback: list[str]) -> str:
        """
        Removes part of the trace caused by the breeze library
        """

        pruned_traceback = traceback[0]
        pruned_traceback += "".join(trace_file for trace_file in traceback[3:])

        return pruned_traceback

    def toJson(self):
        return {
            "origin": self.origin.toJSON(),
            "traceback_str": self.traceback_str,
            "cancelled_nodes": self.cancelled_nodes,
            "input_args": {
                name: format_for_display(value)
                for name, value in self.input_args.items()
            },
        }
