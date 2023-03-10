import numpy as np
from in_param import InParam
class Interface:

    def __init__(self):
        self.inparameters = InParam()

    def getVelocity(self):
        self.inparameters.geometry = float(input("Please enter an initial velocity: \n"))
