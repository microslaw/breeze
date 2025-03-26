# TODO: turn this file into __init__
from backend import create_api_server
from backend import Repository

repository = Repository()

def start():
    api_server = create_api_server(repository)
    api_server.run(debug=True)
