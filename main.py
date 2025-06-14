from breeze import BreezeApp, NodeType

br = BreezeApp()

# TODO remove once nodeSet imports are implemented
import backend.prefabs.testing.kwargs

br.repository.load_workflow("backend/tests/workflows/kwargs")

br.start()
