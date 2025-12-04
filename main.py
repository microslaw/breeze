from breeze import BreezeApp, prefabs, Repository

prefabs.load_pandas()
prefabs.load_plotly()
prefabs.load_scikit()

# prefabs.load_numpy_fft()
prefabs.load_pytorch_radar()

# repo = Repository(db_folder_path="backend/example_workflows/data_fft", purge=False)
# repo = Repository(db_folder_path="backend/example_workflows/data_scikit", purge=False)
repo = Repository(db_folder_path="backend/example_workflows/data_radar", purge=False)
br = BreezeApp(repo)


br.start()
