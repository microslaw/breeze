from flask import Flask, request
from flask_cors import CORS
from backend.datatypes import NodeInstance, NodeLink
from backend.repository import Repository
from backend.repository import ObjectAlreadyInDBException
from backend.repository import ObjectNotInDBException
from backend.processor import Processor, ProcessingException
from backend.formatting import format_for_display


class Controller:
    def __init__ (self, repository: Repository = None, processor: Processor = None):
        self.flask_server = Flask(__name__)
        CORS(self.flask_server, origins=["http://localhost:5173"])

        self.repository = repository if repository is not None else Repository()
        self.processor = processor if processor is not None else Processor(self.repository)


        @self.flask_server.errorhandler(ObjectNotInDBException)
        def server_error(err):
            return str(err), 404

        @self.flask_server.errorhandler(ObjectAlreadyInDBException)
        def server_error(err):
            return str(err), 409

        @self.flask_server.errorhandler(ProcessingException)
        def server_error(err: ProcessingException):
            return err.toJson(), 422

        @self.flask_server.route("/nodeTypes", methods=["GET"])
        def get_all_node_types():
            return self.repository.get_all_node_types()

        @self.flask_server.route("/nodeTypes/<node_type_name>", methods=["GET"])
        def get_node_type(node_type_name):
            return self.repository.get_node_type(node_type_name).toJSON()

        @self.flask_server.route("/nodeInstances", methods=["GET"])
        def get_all_node_instances():
            return [node.toJSON() for node in self.repository.get_all_node_instances()]

        @self.flask_server.route("/nodeInstances/<node_id>", methods=["GET"])
        def get_node_instance(node_id):
            return self.repository.get_node_instance(node_id).toJSON()

        @self.flask_server.route("/nodeInstances", methods=["POST"])
        def create_node_instance():
            node_instance = NodeInstance.fromJSON(request.json)
            node_id = self.repository.create_node_instance(node_instance)
            response = {"node_id": node_id}
            return response, 200

        @self.flask_server.route("/nodeInstances/<node_id>", methods=["DELETE"])
        def delete_node_instance(node_id):
            self.repository.delete_node_instance(node_id)
            return "OK", 200

        @self.flask_server.route("/nodeLinks/<node_id>", methods=["GET"])
        def get_node_link(node_id):
            """
            Returns all links originating from the node with the given id
            """
            node_links = self.repository.get_links_by_origin_node_id(node_id)
            return [link.toJSON() for link in node_links]

        @self.flask_server.route("/nodeLinks", methods=["GET"])
        def get_all_node_links():
            """
            Returns all links
            """
            node_links = self.repository.get_all_links()
            return [link.toJSON() for link in node_links]

        @self.flask_server.route("/nodeLinks", methods=["POST"])
        def create_node_link():
            node_link = NodeLink.fromJSON(request.json)
            self.repository.create_node_link(node_link)
            return "OK", 200

        @self.flask_server.route("/nodeLinks", methods=["DELETE"])
        def delete_node_link():
            node_link = NodeLink.fromJSON(request.json)
            self.repository.delete_node_link(node_link)
            return "OK", 200

        @self.flask_server.route("/queueProcessing", methods=["POST"])
        def queue_processing():
            nodeToProcess = NodeInstance.fromJSON(request.json)
            self.processor.update_processing_schedule(nodeToProcess.node_id)
            return "OK", 200

        @self.flask_server.route("/queueProcessing", methods=["GET"])
        def check_processing_queue():
            return self.processor.get_processing_schedule()

        @self.flask_server.route("/processingResult/<node_id>", methods=["GET"])
        def get_processing_result(node_id):
            return format_for_display(self.repository.read_object(node_id))

    def test_client(self, **kwargs):
        return self.flask_server.test_client(**kwargs)

    def run(self, **kwargs):
        return self.flask_server.run(**kwargs)
