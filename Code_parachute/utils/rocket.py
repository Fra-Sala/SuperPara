import numpy as np


class Rocket:

    def __init__(self, cd0, mass, cross_section):
        """Constructor for object Rocket"""

        self.cd0 = cd0
        self.cd = cd0
        self.mass = mass
        self.cross_section = cross_section

    def compute_cd_rocket(self,mach):
        """This function computes cD_rocket as a function of Mach number. For details,
            see documentation"""

        self.cd = (self.cd0- 0.2605) * np.exp(0.73 *mach) + 0.2605
