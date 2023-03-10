from parachute import Parachute


class ConicalRibbon(Parachute):

    def __init__(self):
        super().__init__(self)
        self.cD = 0.5

    def compute_ev(self):
        self.geometry()



