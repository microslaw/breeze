# TODO: turn this file into __init__
from backend import create_api_server
from backend import Repository
from backend import Processor

repository = Repository()


def start():
    processor = Processor(repository)
    api_server = create_api_server(repository, processor)
    api_server.run(debug=True)
