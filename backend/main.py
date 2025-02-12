from flask import Flask
from NodeType import NodeType
import mock.userDefinedNodes

app = Flask(__name__)

node_type_map = {
    node.get_name(): node.toJSON() for node in NodeType.all_udn
}

@app.route('/nodeTypes', methods=['GET'])
def main_page():
    return list(node_type_map.keys())

@app.route('/nodeTypes/<node_type>', methods=['GET'])
def node_type_page(node_type):
    return node_type_map[node_type]

app.run(debug = True)

