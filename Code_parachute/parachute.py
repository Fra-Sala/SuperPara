import numpy as np
from pyatmos import coesa76
from constants import *


class Drogue:
    """Class Drogue. It contains all the parameters that characterize the preliminary design of the drouge parachute"""

    def __init__(self, cd0_drogue, z_deploy, s_chute, lambda_t):

        """Constuctor for object drogue"""

        self.drag_area = 0.0
        self.cd0 = cd0_drogue
        self.cd = 0.0
        self.t_infl = 0.0  # The following parameters describe the inflation process
        self.delta_t_infl = 1.0
        self.slope_infl = 1.0
        self.z_deploy = z_deploy
        self.lambda_t = lambda_t  # total porosity. In Knacke's book there are plots with suggested values
        self.surface = s_chute
        self.flag_infl = 0  # it allows to check whether the inflation has taken place or not yet
        self.x1_factor = 0.95   # based on reasonable value suggested by Kancke  (see 7.39)
        self.cx_factor = 1.25   #  based on reasonable value suggested by Kancke (see 7.39)
        self.opening_force = 0.0

    def compute_cd_drogue(self, mach):

        """ This function returns a plausible value of the drag coefficient for a hemisflo drogue parachute
                operating at M >> 0.3 (compressibility effects not negligible). The implemented law
                 is taken from the plot in "drogue recovery systems design manual", Section 5"""

        if mach < 1.9:
            self.cd = 0.35
        else:
            self.cd = -1 / 9 * mach + 0.561  # data from Pepper 1986

    def compute_delta_t_infl(self, v):
        """ This method compute the delta of time required for full inflation. The empirical formula is taken from
            Knacke's book """
        self.delta_t_infl = (8 * np.sqrt(4 * self.surface / np.pi) / (np.abs(v) ** 0.9))

    def compute_dragArea_chute(self, t, z, v, mach):

        """ This method computes the product cD*S of the parachute during the inflation and after it"""

        self.compute_cd_drogue(mach)

        if z <= self.z_deploy:  # if we have reached the altitude of deployment

            if self.flag_infl == 0:
                # If the inflation has not occurred yet, then it is taking place at this precise instant t
                self.flag_infl = 1
                self.t_infl = t
                self.compute_delta_t_infl(v)
                self.compute_opening_load(self.t_infl,z,v,mach)
                self.slope_infl = (self.cd) * (self.surface) / self.delta_t_infl

            if (t - self.t_infl) <= self.delta_t_infl:  # if the chute is inflating
                self.drag_area = self.slope_infl * (t - self.t_infl)
            else:
                self.drag_area = self.cd * self.surface

    def compute_opening_load(self, t, z, v, mach):

        rho = coesa76(z / 1000).rho
        self.opening_force = self.cd * self.surface * (
                    1 / 2 * rho * v**2) * self.cx_factor * self.x1_factor

