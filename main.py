import breeze


# TODO remove once nodeSet imports are implemented
import backend.tests.default.nodeTypes

breeze.repository.from_csv("backend/tests/default/nodeInstances.csv", "nodeInstances")
breeze.repository.from_csv("backend/tests/default/nodeLinks.csv", "nodeLinks")

from backend.datatypes import NodeType

breeze.start()
