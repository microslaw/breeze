from flask import Flask, request
from backend.datatypes import NodeInstance, NodeLink
import backend.repository as repository
repository.init_db()

api_server = Flask(__name__)

@api_server.errorhandler(repository.ObjectNotInDBException)
def server_error(err):
    return str(err), 404

@api_server.route("/nodeTypes", methods=["GET"])
def get_all_node_types():
    return repository.get_all_node_types()


@api_server.route("/nodeTypes/<node_type_name>", methods=["GET"])
def get_node_type(node_type_name):
    return repository.get_node_type(node_type_name).toJSON()


@api_server.route("/nodeInstances", methods=["GET"])
def get_all_node_instances():
    return repository.get_all_node_instance_ids()


@api_server.route("/nodeInstances/<node_id>", methods=["GET"])
def get_node_instance(node_id):
    return repository.get_node_instance(node_id).toJSON()


@api_server.route("/nodeInstances", methods=["POST"])
def create_node_instance():
    node_instance = NodeInstance.fromJSON(request.json)
    repository.create_node_instance(node_instance)
    return "OK", 200

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


