import numpy as np
from pyatmos import coesa76
class InParam:

    def __init__(self):
        self.initialVelocity = 0.0
        self.finalDescentRate = 0.0
        self.payloadMass = 0.0
        self.design = 0
        self.objAltitude = coesa76(0.0)
    def __init__(self, in_velocity, descent_rate, mass, design_selection, altitude):
        self.initialVelocity = in_velocity
        self.finalDescentRate = descent_rate
        self.payloadMass = mass
        self.design = design_selection   # an integer
        self.objAltitude = altitude