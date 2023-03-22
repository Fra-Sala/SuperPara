from parachute import Parachute
from pyatmos import coesa76
import numpy as np

class Mainpara(Parachute):
    """Class Mainpara (i.e. main parachute). It contains all the parameters that characterize the main parachute.
        This allows to properly estimate when to deploy the drogue parachute"""

    def __init__(self, cd0_parachute, z_deploy, s_chute, lambda_t, x1_factor = 0.9, cx_factor = 1.05):
        # default values for the factors are taken from Knacke's book
        Parachute.__init__(self,cd0_parachute, z_deploy, s_chute, lambda_t, x1_factor, cx_factor)

    def compute_cd(self, mach):

        """ This function returns a plausible value of the drag coefficient for a hemisflo drogue parachute
                operating at M >> 0.3 (compressibility effects not negligible). The implemented law
                 is taken from the plot in "Parachute recovery systems design manual", Section 5"""

        self.cd = self.cd0 + 0.0*mach  # The main parachute is expected to work at M < 0.3, therefore we approximate its cd as constant with the mach number

    def compute_delta_t_infl(self, v):
        """ This method computes the delta of time required for full inflation. The empirical formula is taken from
            Knacke's book, for a ribbon parachute."""
        self.delta_t_infl = (8 * np.sqrt(4 * self.surface / np.pi) / (np.abs(v) ** 0.9))

    def compute_dragArea_chute(self, t, z, v, mach):

        """ This method computes the product cD*S of the parachute during the inflation and after it.
            A linear inflation is supposed to take place."""

        self.compute_cd(mach)

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

        """This computation is based on Knacke's book. It is valid for a conical ribbon parachute"""
        rho = coesa76(z / 1000).rho
        self.opening_force = float(self.cd * self.surface * (
                    1 / 2 * rho * v**2) * self.cx_factor * self.x1_factor)

        if self.opening_force > 1e5:
            print("Warning: your main parachute would probably be in pieces!\n")

