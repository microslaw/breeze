from breeze import BreezeApp, prefabs

prefabs.testing.load_kwargs()

br = BreezeApp()

br.repository.load_workflow("backend/tests/workflows/kwargs")

br.start()
