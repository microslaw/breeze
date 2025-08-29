from backend.repository import Repository
from backend.processor import Processor
from backend.controller import Controller


class BreezeApp:
    """
    Composition of all elements required for breeze workflows
    """

    def __init__(self):
        self.repository = Repository()
        self.processor = Processor(self.repository)
        self.controller = Controller(self.repository, self.processor)

    def start(self):
        """
        Starts the application
        """
        self.controller.run(debug=True)
