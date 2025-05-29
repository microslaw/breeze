from flask import Flask, request
from flask_cors import CORS
from backend.datatypes import NodeInstance, NodeLink
from backend.repository import Repository
from backend.repository import ObjectAlreadyInDBException
from backend.repository import ObjectNotInDBException
from backend.processor import Processor, ProcessingException
from backend.formatting import format_for_display, format_from_input


class BadRequestException(Exception):
    pass


class Controller:
    def __init__(self, repository: Repository, processor: Processor):
        self.flask_server = Flask(__name__)
        CORS(self.flask_server, origins=["http://localhost:5173"])

        self.repository = repository
        self.processor = processor

        @self.flask_server.errorhandler(ObjectNotInDBException)
        def server_error(err):
            return str(err), 404

        @self.flask_server.errorhandler(ObjectAlreadyInDBException)
        def server_error(err):
            return str(err), 409

        @self.flask_server.errorhandler(ProcessingException)
        def server_error(err: ProcessingException):
            return err.toJson(), 422

        @self.flask_server.errorhandler(BadRequestException)
        def server_error(err: BadRequestException):
            return err.toJson(), 400

        @self.flask_server.route("/nodeTypes", methods=["GET"])
        def get_all_node_types():
            return self.repository.get_all_node_types()

        @self.flask_server.route("/nodeTypes/<node_type_name>", methods=["GET"])
        def get_node_type(node_type_name):
            return self.repository.get_node_type(node_type_name).toJSON()

        @self.flask_server.route("/nodeInstances", methods=["GET"])
        def get_all_node_instances():
            return [
                node.toNameDict() for node in self.repository.get_all_node_instances()
            ]

        @self.flask_server.route("/nodeInstances/<node_id>", methods=["GET"])
        def get_node_instance(node_id):
            return self.repository.get_node_instance(node_id).toNameDict()

        @self.flask_server.route("/nodeInstances", methods=["POST"])
        def create_node_instance():
            node_instance = NodeInstance.fromNameDict(request.json)
            node_id = self.repository.create_node_instance(node_instance)
            response = {"node_id": node_id}
            return response, 200

        @self.flask_server.route("/nodeInstances/<node_id>", methods=["DELETE"])
        def delete_node_instance(node_id):
            self.repository.delete_node_instance(node_id)
            return "OK", 200

        @self.flask_server.route("/nodeLinks/<node_link_id>", methods=["GET"])
        def get_node_link(node_link_id):
            return self.repository.get_node_link(node_link_id).toNameDict()

        @self.flask_server.route("/nodeLinks", methods=["GET"])
        def get_all_node_links():
            """
            Returns all links. Has option to filter by origin or destination node
            """

            node_links = self.repository.get_all_links(
                origin_node_id=request.args.get("origin_node_id"),
                destination_node_id=request.args.get("destination_node_id"),
            )

            return [link.toNameDict() for link in node_links]

        @self.flask_server.route("/nodeLinks", methods=["POST"])
        def create_node_link():
            node_link = NodeLink.fromNameDict(request.json)
            node_link_id = self.repository.create_node_link(node_link)
            response = {"node_link_id": node_link_id}
            return response, 200

        @self.flask_server.route("/nodeLinks/<node_link_id>", methods=["PATCH"])
        def patch_node_link(node_link_id):

            if "node_link_id" in request.json:
                raise BadRequestException("Field node_link_id cannot be patched")

            node_link_update = NodeLink.fromNameDict(request.json)
            self.repository.update_node_link(node_link_update, node_link_id)

            return "OK", 200

        @self.flask_server.route("/nodeLinks/<node_link_id>", methods=["DELETE"])
        def delete_node_link(node_link_id):
            self.repository.delete_node_link(node_link_id)
            return "OK", 200

        @self.flask_server.route("/queueProcessing", methods=["POST"])
        def queue_processing():
            nodeToProcess = NodeInstance.fromNameDict(request.json)
            self.processor.update_processing_schedule(nodeToProcess.node_id)
            return "OK", 200

        @self.flask_server.route("/queueProcessing", methods=["GET"])
        def check_processing_queue():
            return self.processor.get_processing_schedule()

        @self.flask_server.route("/processingResult/<node_id>", methods=["GET"])
        def get_processing_result(node_id):
            return format_for_display(self.repository.read_output(node_id))

        @self.flask_server.route(
            "/nodeInstances/<node_id>/kwargs/<kwarg_name>", methods=["GET"]
        )
        def get_kwarg(node_id, kwarg_name):
            return format_for_display(repository.read_kwarg(node_id, kwarg_name))

        @self.flask_server.route(
            "/nodeInstances/<node_id>/kwargs/<kwarg_name>", methods=["PUT"]
        )
        def put_node_kwarg(node_id, kwarg_name):
            node_type_name = repository.get_node_instance_type_name(node_id)
            arg_type = repository.get_arg_type(node_type_name, kwarg_name)
            repository.write_kwarg(
                format_from_input(request.data, arg_type), node_id, kwarg_name
            )
            return "OK", 200

    def test_client(self, **kwargs):
        return self.flask_server.test_client(**kwargs)

    def run(self, **kwargs):
        return self.flask_server.run(**kwargs)
