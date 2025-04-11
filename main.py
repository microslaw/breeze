from breeze import BreezeApp, NodeType
import backend.prefabs.testing.default

br = BreezeApp()
br.load_test_preset("default")

br.start()
