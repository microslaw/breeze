import backend.prefabs.basic_pandas
from backend import Repository, Processor, Controller

def initialize_server():
    repository = Repository()
    processor = Processor(repository)
    controller = Controller(repository, processor)


