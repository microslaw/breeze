from flask import Flask
from NodeType import NodeType
import mock.userDefinedNodes

app = Flask(__name__)

@app.route('/app', methods=['GET'])
def main_page():
    return [node.toJSON() for node in NodeType.all_udn]

app.run(debug = True)

