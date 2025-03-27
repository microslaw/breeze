from backend.datatypes import NodeInstance, NodeLink
from backend.repository import Repository
from collections import deque
import time
import threading


class Processor:

    def __init__(self, repository: Repository):
        self.processing_queue = deque()
        self.processing_daemon = threading.Thread(
            target=self.run_processing_daemon, daemon=True
        )
        self.processing_daemon.start()
        self.repository = repository

    def update_processing_schedule(self, node_id):
        to_add = [node_id]
        queue_appendix = []

        while len(to_add) > 0:
            node_id = to_add.pop()
            required_node_ids = self.repository.get_prerequisite_node_ids(node_id)
            to_add.extend(required_node_ids)
            queue_appendix.append(node_id)

        queue_appendix.reverse()

        for item in queue_appendix:
            if item not in self.processing_queue:
                self.processing_queue.append(item)

    def run_processing_daemon(self):
        while True:
            time.sleep(0.01)
            if len(self.processing_queue) > 0:
                node_id = self.processing_queue.popleft()
                self.process(node_id)

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
