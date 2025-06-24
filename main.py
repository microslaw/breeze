from breeze import BreezeApp, prefabs

prefabs.load_pandas()

br = BreezeApp()

br.repository.load_workflow("backend/tests/workflows/pandas")

br.start()
