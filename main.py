from breeze import BreezeApp, NodeType

br = BreezeApp()

# TODO remove once nodeSet imports are implemented
import backend.prefabs.testing.default

br.repository.load_workflow("backend/tests/workflows/default")

br.start()
