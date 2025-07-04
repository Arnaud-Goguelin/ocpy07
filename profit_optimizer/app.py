from .models import Data

class Application:

    def __init__(self):
        self.data = Data()
        self.data.load()

    def run(self):
        pass
