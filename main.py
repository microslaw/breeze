from breeze import BreezeApp, prefabs

prefabs.testing.load_default()

br = BreezeApp()
br.repository.load_workflow("backend/tests/workflows/default")
br.start()
