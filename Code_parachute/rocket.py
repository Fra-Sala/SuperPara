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



# 0.00 0.548 0.476
# 0.20 0.518 0.458
# 0.40 0.503 0.444
# 0.60 0.496 0.435
# 0.70 0.498 0.434
# 0.75 0.500 0.434
# 0.80 0.508 0.434
# 0.85 0.517 0.442
# 0.90 0.536 0.460
# 0.95 0.570 0.488
# 1.00 0.632 0.516
# 1.07 0.727 0.551
# 1.10 0.743 0.556
# 1.15 0.733 0.556
# 1.20 0.718 0.550
# 1.30 0.693 0.535
# 1.50 0.661 0.510
# 1.75 0.624 0.488
# 2.20 0.563 0.452
# 2.50 0.528 0.433
# 3.00 0.475 0.407
# 3.50 0.432 0.388
# 4.00 0.405 0.374
# 4.50 0.385 0.365
# 5.00 0.375 0.36
# 8.00 0.35