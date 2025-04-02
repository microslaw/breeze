from backend.datatypes import NodeInstance, NodeLink
from backend.repository import Repository
from collections import deque
import time
import threading


class Processor:

    def __init__(self, repository: Repository):
        self.processing_queue = deque()
        self.repository = repository
        self.running = False

    def get_all_required_node_ids(self, node_id:str) -> list[int]:
        queue_appendix = []
        to_add = [node_id]

        while len(to_add) > 0:
            node_id = to_add.pop()
            required_node_ids = self.repository.get_prerequisite_node_ids(node_id)
            to_add.extend(required_node_ids)
            queue_appendix.append(node_id)
        queue_appendix.reverse()

        return queue_appendix

    def update_processing_schedule(self, node_id:int) -> None:
        queue_appendix = self.get_all_required_node_ids(node_id)

        for item in queue_appendix:
            if item not in self.processing_queue:
                self.processing_queue.append(item)
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

        output = processed_node_type(**kwargs)
        self.repository.write_object(output, node_id)
