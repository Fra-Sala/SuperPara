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
            see documentation.
            Input:
            @:param mach: the current Mach number

            @:return
            """


        xmach = np.array([0.00, 0.2, 0.4, 0.6, 0.7, 0.75, 0.8, 0.85, 0.90, 0.95, 1.00, 1.07, 1.10, 1.15, 1.20, 1.30, 1.50, 1.75, 2.20,
                  2.50, 3.00, 3.50, 4.00, 4.50, 5.00, 8.00])
        ycd = np.array([0.548, 0.518, 0.503, 0.496, 0.498, 0.5, 0.508, 0.517, 0.536, 0.570, 0.632, 0.727, 0.743, 0.733, 0.718, 0.693,
                  0.661, 0.624, 0.563, 0.528, 0.475, 0.432, 0.405, 0.385, 0.375, 0.35])

        self.cd = np.interp(mach, xmach, ycd)

        #self.cd = (self.cd0- 0.2605) * np.exp(0.73 *mach) + 0.2605



