from .algorithms import BrutForce
from .models import Data


class Application:

    def __init__(self):
        self.data = Data()
        self.data.load()

    def run(self):
        brut_force = BrutForce(self.data.actions)
        brut_force.run()
