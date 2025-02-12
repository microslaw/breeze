from flask import Flask, request
from NodeType import NodeType
from NodeInstance import NodeInstance
from NodeLink import NodeLink
import repository
repository.init_db()

# importing this initializes the mock data
import mock.nodeInstances

app = Flask(__name__)

node_type_map = {node.get_name(): node.toJSON() for node in NodeType.all_udn}


@app.route("/nodeTypes", methods=["GET"])
def main_page():
    return list(node_type_map.keys())


@app.route("/nodeTypes/<node_type>", methods=["GET"])
def node_type_page(node_type):
    return node_type_map[node_type]


@app.route("/nodeInstances", methods=["GET"])
def node_instances_page():
    return repository.get_all_node_instance_ids()


@app.route("/nodeInstances/<node_id>", methods=["GET"])
def node_instance_page(node_id):
    return repository.get_node_instance(node_id).toJSON()


@app.route("/nodeInstances", methods=["POST"])
def create_node_instance():
    node_instance = NodeInstance.fromJSON(request.json)
    repository.create_node_instance(node_instance)
    return "OK", 200

@app.route("/nodeInstances/<node_id>", methods=["DELETE"])
def delete_node_instance(node_id):
    repository.delete_node_instance(node_id)
    return "OK", 200

@app.route("/nodeLinks/<node_id>", methods=["GET"])
def node_link_page(node_id):
    """
    Returns all links originating from the node with the given id
    """
    node_links = repository.get_links_by_origin_node_id(node_id)
    return [link.toJSON() for link in node_links]


@app.route("/nodeLinks", methods=["POST"])
def create_node_link():
    node_link = NodeLink.fromJSON(request.json)
    repository.create_node_link(node_link)
    return "OK", 200


@app.route("/nodeLinks", methods=["DELETE"])
def delete_node_link():
    node_link = NodeLink.fromJSON(request.json)
    repository.delete_node_link(node_link)
    return "OK", 200


app.run(debug=True)
