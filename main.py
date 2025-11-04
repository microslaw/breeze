from breeze import BreezeApp, prefabs, NodeType, formatting, Repository
import numpy as np

prefabs.load_pandas()
prefabs.load_plotly()
prefabs.load_scikit()

N = 10_000


formatting.add_display_format(
    np.ndarray,
    lambda x: f"np.ndarray(shape={x.shape}, dtype={x.dtype})",
)

repo = Repository(db_folder_path="backend/data_scikit", purge=False)
br = BreezeApp(repo)


br.start()
