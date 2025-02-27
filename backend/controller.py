from flask import Flask, request
from backend.datatypes import NodeInstance, NodeLink, NodeType
import backend.repository as repository
repository.init_db()

api_server = Flask(__name__)

def get_node_map():
    return {node.get_name(): node.toJSON() for node in NodeType.all_udn}

@api_server.errorhandler(repository.ObjectNotInDBException)
def server_error(err):
    return str(err), 404

@api_server.route("/nodeTypes", methods=["GET"])
def main_page():
    return list(get_node_map().keys())


@api_server.route("/nodeTypes/<node_type>", methods=["GET"])
def node_type_page(node_type):
    return get_node_map()[node_type]


@api_server.route("/nodeInstances", methods=["GET"])
def node_instances_page():
    return repository.get_all_node_instance_ids()


@api_server.route("/nodeInstances/<node_id>", methods=["GET"])
def node_instance_page(node_id):
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
def node_link_page(node_id):
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


