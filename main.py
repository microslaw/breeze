from backend import create_api_server
from backend.datatypes import NodeType, NodeInstance, NodeLink
import backend.repository as repository
import pandas as pd

import backend.tests.default.nodeTypes

repository.init_db()
repository.from_csv("backend/tests/processing/nodeInstances.csv", "nodeInstances")
repository.from_csv("backend/tests/processing/nodeLinks.csv", "nodeLinks")

api_server = create_api_server()
api_server.run(debug=True)

