from flask import Flask, request
from flask_cors import CORS
from backend.datatypes import NodeInstance, NodeLink
from backend.repository import Repository
from backend.repository import ObjectAlreadyInDBException
from backend.repository import ObjectNotInDBException
from backend.processor import Processor, ProcessingException
from backend.formatting import format_for_display


def create_api_server(repository: Repository, processor: Processor):
    api_server = Flask(__name__)
    CORS(api_server, origins=["http://localhost:5173"])

    @api_server.errorhandler(ObjectNotInDBException)
    def server_error(err):
        return str(err), 404

    @api_server.errorhandler(ObjectAlreadyInDBException)
    def server_error(err):
        return str(err), 409

    @api_server.errorhandler(ProcessingException)
    def server_error(err: ProcessingException):
        return err.toJson(), 422

    @api_server.route("/nodeTypes", methods=["GET"])
    def get_all_node_types():
        return repository.get_all_node_types()

    @api_server.route("/nodeTypes/<node_type_name>", methods=["GET"])
    def get_node_type(node_type_name):
        return repository.get_node_type(node_type_name).toJSON()

    @api_server.route("/nodeInstances", methods=["GET"])
    def get_all_node_instances():
        node_instances = repository.get_all_node_instances()
        return [node.toJSON() for node in node_instances]

    @api_server.route("/nodeInstances/<node_id>", methods=["GET"])
    def get_node_instance(node_id):
        return repository.get_node_instance(node_id).toJSON()

    @api_server.route("/nodeInstances", methods=["POST"])
    def create_node_instance():
        node_instance = NodeInstance.fromJSON(request.json)
        node_id = repository.create_node_instance(node_instance)
        response = {"node_id": node_id}
        return response, 200

    @api_server.route("/nodeInstances/<node_id>", methods=["DELETE"])
    def delete_node_instance(node_id):
        repository.delete_node_instance(node_id)
        return "OK", 200

    @api_server.route("/nodeLinks/<node_id>", methods=["GET"])
    def get_node_link(node_id):
        """
        Returns all links originating from the node with the given id
        """
        node_links = repository.get_links_by_origin_node_id(node_id)
        return [link.toJSON() for link in node_links]

    @api_server.route("/nodeLinks", methods=["GET"])
    def get_all_node_links():
        """
        Returns all links
        """
        node_links = repository.get_all_links()
        return [link.toJSON() for link in node_links]

    @api_server.route("/nodeLinks", methods=["POST"])
    def create_node_link():
        node_link = NodeLink.fromJSON(request.json)
        repository.create_node_link(node_link)
        return "OK", 200

    @api_server.route("/nodeLinks", methods=["DELETE"])
    def delete_node_link():
        node_link = NodeLink.fromJSON(request.json)
        repository.delete_node_link(node_link)
        return "OK", 200

    @api_server.route("/queueProcessing", methods=["POST"])
    def queue_processing():
        nodeToProcess = NodeInstance.fromJSON(request.json)
        processor.update_processing_schedule(nodeToProcess.node_id)
        return "OK", 200

    @api_server.route("/queueProcessing", methods=["GET"])
    def check_processing_queue():
        return processor.get_processing_schedule()

    @api_server.route("/processingResult/<node_id>", methods=["GET"])
    def get_processing_result(node_id):
        return format_for_display(repository.read_object(node_id))

    return api_server
