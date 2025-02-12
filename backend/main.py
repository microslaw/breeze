from flask import Flask
from NodeType import NodeType
import mock.userDefinedNodes
import mock.nodeInstances
import repository

app = Flask(__name__)

node_type_map = {node.get_name(): node.toJSON() for node in NodeType.all_udn}


@app.route("/nodeTypes", methods=["GET"])
def main_page():
    return list(node_type_map.keys())


@app.route("/nodeTypes/<node_type>", methods=["GET"])
def node_type_page(node_type):
    return node_type_map[node_type]


@app.route("/node", methods=["GET"])
def node_instances_page():
    return repository.get_all_node_instances()


@app.route("/node/<node_id>", methods=["GET"])
def node_instance_page(node_id):
    return repository.get_node_instance(node_id)


app.run(debug=True)
