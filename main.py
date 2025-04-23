from breeze import BreezeApp, NodeType

br = BreezeApp()

# TODO remove once nodeSet imports are implemented
import backend.tests.default.nodeTypes

br.repository.from_csv("backend/tests/default/nodeInstances.csv", "nodeInstances")
br.repository.from_csv("backend/tests/default/nodeLinks.csv", "nodeLinks")


br.start()
