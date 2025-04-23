from backend.datatypes import NodeType
from backend.repository import Repository
from backend.processor import Processor
from backend.controller import Controller


class BreezeApp:
    def __init__(self):
        self.repository = Repository()
        self.processor = Processor(self.repository)
        self.controller = Controller(self.repository, self.processor)

    def start(self):
        self.controller.run(debug=True)
