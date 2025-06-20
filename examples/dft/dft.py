
from breeze import BreezeApp, prefabs, NodeType, formatting
import numpy as np

prefabs.load_pandas()
prefabs.load_plotly()

N = 10_000



@NodeType(tags=["numpy"])
def create_sin_wave(freq:float) -> np.ndarray:
    return np.sin(np.arange(0, 20, step=20 / N) * 2 * np.pi * freq)

@NodeType
def add(a:object, b:object) -> object:
    return a+b

@NodeType(tags=["numpy"])
def create_kn_matrix() -> np.ndarray:
    n = np.arange(N)
    k = np.arange(N).reshape((N, 1))
    return -2j * np.pi * k * n / N

@NodeType(tags=["numpy"])
def numpy_exponential(arr:np.ndarray) -> np.ndarray:
    return np.exp(arr)

@NodeType(tags=["numpy"])
def dot_product(arr1:np.ndarray, arr2:np.ndarray) -> np.ndarray:
    return np.dot(arr1, arr2)

@NodeType(tags=["numpy"])
def numpy_imag(arr:np.ndarray) -> np.ndarray:
    return np.imag(arr)

@NodeType(tags=["numpy"])
def numpy_real(arr:np.ndarray) -> np.ndarray:
    return np.real(arr)

@NodeType(tags=["numpy"])
def numpy_abs(arr:np.ndarray) -> np.ndarray:
    return np.abs(arr)

formatting.add_display_format(np.ndarray, lambda x: f"np.ndarray(shape={x.shape}, dtype={x.dtype})")

br = BreezeApp()
br.repository.load_workflow("backend/examples/dft/workflow")
br.start()
