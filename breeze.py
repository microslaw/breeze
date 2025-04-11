# TODO: turn this file into __init__
from backend import Controller
from backend import Repository
from backend import Processor

repository = Repository()


def start():
    processor = Processor(repository)
    controller = Controller(repository, processor)
    controller.run(debug=True)
